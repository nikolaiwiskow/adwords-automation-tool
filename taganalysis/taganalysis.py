import openpyxl
import os
from walle.settings import BASE_DIR

from adwords_reports.report import AdwordsReport
from pprint import pprint


class tagAnalysis(object):

	def __init__(self):
		# where all data goes, unfiltered. Is set by self.getData()
		self.rawData = None
		# filterd raw data by device/tag etc. Is set by self.clusterRowsPerTag()
		self.rawDataCluster = []
		# final output data for display. Is set by self.clusterRowsPerTag()
		self.clusteredData = {}


	def getData(self, client, time_range):
		# gets the raw data via the API 
		query = ("SELECT AdGroupName, Criteria, Impressions, Clicks, Conversions, Cost, AveragePosition, QualityScore "
				"FROM KEYWORDS_PERFORMANCE_REPORT "
				"WHERE Impressions > 0 "
				"DURING " + time_range)

		self.rawData = AdwordsReport(query, client).returnDataAsListOfDicts()
		for row in self.rawData:
			row["tags"] = self.getTagsFromAgName(row["AdGroupName"])
			row["device"] = self.getDeviceFromAgName(row["AdGroupName"])
			row["matchtype"] = self.getMatchTypeFromAgName(row["AdGroupName"])


	def getTagsFromAgName(self, str_ag_name):
		# derives tags from AG name
		tags = str_ag_name.split("  ")[1]
		tags = tags.replace("[", "")
		tags = tags.split("]")
		return tags

	def getDeviceFromAgName(self, str_ag_name):
		# derives device from Ag name
		devices = { "[m]": "MOBILE",
					"[d]": "DESKTOP", 
					"[t]": "TABLET" }

		dev_code = str_ag_name[:3]
		return devices[dev_code]

	def getMatchTypeFromAgName(self, str_ag_name):
		# derices matchtype from Ag name
		matchtypes = {	"[e]": "EXACT", 
						"[b]": "PLUS", 
						"[w]": "BROAD", 
						"[p]": "PHRASE"	}

		mt_code = str_ag_name[3:6]
		return matchtypes[mt_code]


	def clusterRowsPerTag(self, list_filter_tags=None, str_filter_device=None, str_filter_matchtype=None):
		# apply device and matchtype filters
		if str_filter_device and str_filter_matchtype:
			filtered_data = [row for row in self.rawData if row["device"] == str_filter_device and row["matchtype"] == str_filter_matchtype]
		elif str_filter_matchtype:
			filtered_data = [row for row in self.rawData if row["matchtype"] == str_filter_matchtype]
		elif str_filter_device:
			filtered_data = [row for row in self.rawData if row["device"] == str_filter_device]
		else:
			filtered_data = self.rawData


		#filter rows for filter tags, if provided
		if list_filter_tags:
			list_filter_tags.sort()

			further_drilldown = False

			for row in filtered_data:
				lft = set(list_filter_tags)
				rt = set(row["tags"])
				#check if filter tags are in tags
				if lft.issubset(rt):
					if len(lft) < len(rt):
						further_drilldown = True
					self.rawDataCluster.append(row)

			if further_drilldown:
				#iterate over tag-filtered data
				for row in self.rawDataCluster:
					additional_tags = [tag for tag in row["tags"] if tag not in list_filter_tags]

					if additional_tags:
						for tag in additional_tags:
							key = "".join(list_filter_tags) + tag
							self.addUpClusteredData(key, row)
					else:
						self.addUpClusteredData("".join(list_filter_tags), row)

			else:
				for row in self.rawDataCluster:
					self.addUpClusteredData(row["AdGroupName"], row)


		# if there are no tags to filter for
		else:
			self.rawDataCluster = filtered_data
			for row in self.rawDataCluster:
				for tag in row["tags"]:
					self.addUpClusteredData(tag, row)

		self.addCalculatedMetrics(self.clusteredData)
		return self.clusteredData


	def clusterRowsPerAgName(self, list_filter_tags=None, str_filter_device=None, str_filter_matchtype=None):
		if str_filter_device and str_filter_matchtype:
			filtered_data = [row for row in self.rawData if row["device"] == str_filter_device and row["matchtype"] == str_filter_matchtype]
		elif str_filter_matchtype:
			filtered_data = [row for row in self.rawData if row["matchtype"] == str_filter_matchtype]
		elif str_filter_device:
			filtered_data = [row for row in self.rawData if row["device"] == str_filter_device]
		else:
			filtered_data = self.rawData

		if list_filter_tags:
			list_filter_tags.sort()

			for row in filtered_data:
				lft = set(list_filter_tags)
				rt = set(row["tags"])
				# check if filter tags are in tags and tag amount is the same
				if lft.issubset(rt) and len(lft) == len(rt):
					self.rawDataCluster.append(row)

			for row in self.rawDataCluster:
				self.addUpClusteredData(row["AdGroupName"], row)

			self.addCalculatedMetrics(self.clusteredData)

		else:
			for row in filtered_data:
				self.addUpClusteredData(row["AdGroupName"], row)
			self.addCalculatedMetrics(self.clusteredData)

		return self.clusteredData




	def addUpClusteredData(self, str_key, dict_row_data):
		#helper function to add up each rows data to the appropriate aggregation cluster
		if str_key not in self.clusteredData:
			self.clusteredData[str_key] = {	"Impressions": 0,
											"Clicks": 0,
											"Conversions": 0.0, 
											"Cost": 0,
											"AvgPos": 0,
											"QS": 0	}

		self.clusteredData[str_key]["Impressions"] += int(dict_row_data["Impressions"])
		self.clusteredData[str_key]["Clicks"] += int(dict_row_data["Clicks"])
		self.clusteredData[str_key]["Conversions"] += float(dict_row_data["Conversions"])
		self.clusteredData[str_key]["Cost"] += (float(dict_row_data["Cost"]) / 1000000)
		self.clusteredData[str_key]["AvgPos"] += float(dict_row_data["AveragePosition"]) * int(dict_row_data["Impressions"])
		if dict_row_data["QualityScore"] == " --":
			dict_row_data["QualityScore"] = 0
		self.clusteredData[str_key]["QS"] += int(dict_row_data["QualityScore"]) * int(dict_row_data["Impressions"])



	def addCalculatedMetrics(self, data):
		#add calculated metrics to row-dicts
		for key in data:
			line = data[key]
			
			line["CTR"] = "{:.2%}".format(line["Clicks"] / line["Impressions"])

			if line["Conversions"] > 0:
				line["CPL"] = "{:.2f}".format(line["Cost"] / int(line["Conversions"]))
			else:
				line["CPL"] = "{:.2f}".format(line["Cost"])

			if line["Clicks"] > 0:
				line["CR"] = "{:.2%}".format(int(line["Conversions"]) / line["Clicks"])
				line["CPC"] = "{:.2f}".format(line["Cost"] / line["Clicks"])
			else:
				line["CR"] = "{:.2%}".format(0)
				line["CPC"] = 0

			line["Cost"] = "{:.2f}".format(line["Cost"])
			line["AvgPos"] = "{:.2f}".format(line["AvgPos"] / line["Impressions"])
			line["QS"] = "{:.2f}".format(line["QS"] / line["Impressions"])

		return


	def outputToXlsx(self):
		wb = openpyxl.Workbook()
		sheet = wb.active

		# check if rawData is actual raw data, or already clustered from filtering
		if "AdGroupName" in list(self.rawData)[0]:
			# header
			sheet.append(["Adgroup", "Keyword", "Impressions", "Clicks", "Conversions", "Cost", "Avg. Pos", "QS"])
			# data
			for row in self.rawData:
				sheet.append([row["AdGroupName"], row["Criteria"], int(row["Impressions"]), int(row["Clicks"]), float(row["Conversions"]), float(row["Cost"])/1000000, float(row["AveragePosition"]), int(row["QualityScore"])])

		else:
			# header
			sheet.append(["Tag", "Impressions", "Clicks", "CTR", "CPC", "Conversions", "CPL", "CR", "Cost", "Avg. Pos", "QS"])
			# data
			for key in self.rawData:
				a = self.rawData[key]
				#type conversions
				ctr = a["CTR"].replace("%", "")
				cr = a["CR"].replace("%", "")
				sheet.append([key, int(a["Impressions"]), int(a["Clicks"]), float(ctr)/100, float(a["CPC"]), float(a["Conversions"]), float(a["CPL"]), float(cr)/100, float(a["Cost"]), float(a["AvgPos"]), float(a["QS"])])

		dest_filename = os.path.join(BASE_DIR, "taganalysis/media/output.xlsx")
		wb.save(filename=dest_filename)

		return "taganalysis/media/output.xlsx"

