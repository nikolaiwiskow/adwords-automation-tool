from googleads import adwords, oauth2

API_VERSION = "v201809"

class AdwordsReport(object):

	def __init__(self, report_query, client):
		self.report_service = client.GetReportDownloader(version=API_VERSION)
		self.report = self.report_service.DownloadReportAsStringWithAwql(report_query, "CSV", skip_report_header=True, skip_column_header=True, skip_report_summary=True)
		self.rows = self.report.splitlines()
		self.columns = self.getColumnNames(report_query)
		self.rowCount = len(self.rows)


	def getColumnNames(self, report_query):
		cutoff = report_query.find(" FROM")
		# get string between SELECT ... FROM in report query
		headers = report_query[6:cutoff].split(",")
		headers = [header.replace(" ", "") for header in headers]
		return headers

	def rowCount(self):
		return self.rowCount


	def returnDataAs2dList(self):
		data_2d_list = []

		for row in self.rows:
			row_list = row.split(",")
			data_2d_list.append(row_list)

		return data_2d_list


	def returnDataAsListOfDicts(self):
		data = []

		for row in self.rows:
			row_list = row.split(",")
			row_dict = {}

			for index,value in enumerate(row_list):
				row_dict[self.columns[index]] = value

			data.append(row_dict)

		return data


