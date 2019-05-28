from unidecode import unidecode
import json
import openpyxl

from adwords_reports.report import AdwordsReport
from adwords_entities.query import Query
from structure.query_classification.query_tagger import QueryTagger
from structure.query_classification.output import Output

from .models import Negative, CountryCode

def sqrPositive(client, country_code, dict_thresholds):
	# pull query report
	r_query = buildQuery(dict_thresholds)
	sqr_data = AdwordsReport(r_query, client).returnDataAsListOfDicts()

	# get already existing exact match kws
	exact_kws_query = ("SELECT Criteria "
						"FROM KEYWORDS_PERFORMANCE_REPORT "
						"WHERE KeywordMatchType = EXACT "
						"AND Status != REMOVED "
						"AND AdGroupStatus != REMOVED")
	ex_kws_data = AdwordsReport(exact_kws_query, client).returnDataAs2dList()

	# get negative list from DB
	cc_db = CountryCode.objects.get(country_code=country_code)
	negatives_db = Negative.objects.filter(country_code=cc_db)
	negatives = [neg.negative for neg in negatives_db]

	query_strings = []
	queries = []
	
	for row in sqr_data:
		query_string = unidecode(row["Query"])

		# get rid of already booked queries, duplicate queries and queries in neg database
		if query_string not in ex_kws_data and query_string not in query_strings and query_string not in negatives:
			query = Query(query_string)
			query.setCampaignId(row["CampaignId"])
			query.setAdGroupId(row["AdGroupId"])
			query.setFinalUrl(row["FinalUrl"])
			tags = QueryTagger().getTopicTags(query_string, country_code)
			query.setTags(tags)

			queries.append(query)
			query_strings.append(query_string)

	# transform query-object to json, so django can handle it
	queries_json = [json.dumps(query.__dict__) for query in queries]
	
	return queries_json


def buildQuery(dict_thresholds):
	
	query = ("SELECT CampaignId, AdGroupId, Query, FinalUrl "
			"FROM SEARCH_QUERY_PERFORMANCE_REPORT")

	click_thres = dict_thresholds["click_thres"]
	impression_thres = dict_thresholds["impression_thres"]
	conv_thres = dict_thresholds["conv_thres"]
	cpl_thres = dict_thresholds["cpl_thres"]
	time_range = dict_thresholds["time_range"]

	report_query = ("SELECT CampaignId, AdGroupId, Query, FinalUrl "
					"FROM SEARCH_QUERY_PERFORMANCE_REPORT")

	if click_thres:
		final_query = query + " WHERE Clicks > " + str(click_thres-1)
	else:
		final_query = query + " WHERE Clicks > 0"

	if impression_thres:
		final_query = final_query + " AND Impressions > " + str(impression_thres)

	if conv_thres:
		final_query = final_query + " AND Conversions > " + str(conv_thres-1)

	if cpl_thres:
		final_query = final_query + " AND CostPerConversion < " + str(int(cpl_thres)*1000000)	 
					
	final_query = final_query + " DURING " + time_range

	return final_query




def buildInitialStructure(str_country_code, str_xlsx_file_path, str_final_url, devices, matchtypes):
	ws = openpyxl.load_workbook(str_xlsx_file_path).active
	queries = []

	for device in devices:
		for matchtype in matchtypes:
			for row in ws.rows:

				keyword = row[0].value
				query = Query(keyword)
				query.setFinalUrl(str_final_url)
				tags = QueryTagger().getTopicTags(keyword, str_country_code)
				query.setTags(tags)
				query.setMatchType(matchtype)
				query.setDevice(device)
				query.buildAdgroupName()
				queries.append(query)

	o = Output()
	o.setQueries(queries)
	return o.outputToXlsx()
