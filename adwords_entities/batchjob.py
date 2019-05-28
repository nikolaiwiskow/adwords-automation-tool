from datetime import datetime
from googleads import adwords, oauth2

import random, time, uuid, ast
import urllib.request as urllib2

MAX_POLL_ATTEMPS = 5
PENDING_STATUSES = ("ACTIVE", "AWAITING_FILE", "CANCELING")
API_VERSION = "v201702"



class BatchJob(object):

	def __init__(self, client):
		self.batchJobHelper = client.GetBatchJobHelper(version=API_VERSION)
		self.service = client.GetService("BatchJobService", version=API_VERSION)
		self.batchJob = self.addBatchJob()
		self.uploadUrl = self.batchJob["uploadUrl"]["url"]
		self.id = self.batchJob["id"]
		self.downloadUrl = None
		self.budgetOps = []
		self.campaignOps = []
		self.agOps = []
		self.kwOps = []
		self.negativeOps = []
		self.adOps = []

	# adds batch job on __init__
	def addBatchJob(self):
		"""	Input: Adwords client object
			Output: BatchJob object
		"""
		batch_job_operations = [{
			"operand": {},
			"operator": "ADD"
		}]

		return self.service.mutate(batch_job_operations)["value"][0]


	# to be called by user, once all desired operations were added
	def runBatchJob(self):
		possible_arguments = [self.budgetOps, self.campaignOps, self.agOps, self.kwOps, self.negativeOps, self.adOps]
		# only add operations to args list, if there's operations in there
		arguments_list = [entity for entity in possible_arguments if entity]
		arguments.insert(0, self.uploadUrl)

		def wrapper(func, args):
			func(args)

		# call batchJobHelper.UploadOperations() with arguments list
		wrapper(self.batchJobHelper.UploadOperations, arguments_list)

		return self.getDownloadUrlWhenReady()


	# checks if batch job is ready, and if it is, gets download url
	def getDownloadUrlWhenReady(self):
		""" Input: Adwords Client object, Int BatchJobId
			Output: String, url of batch job result
		"""
		selector = {
			"fields": ["Id", "Status", "DownloadUrl"],
			"predicates": [{
				"field": "Id",
				"operator": "EQUALS",
				"values": [self.id]
			}]
		}

		batch_job = self.service.get(selector)["entries"][0]

		poll_attempt = 0

		while (poll_attempt in range(MAX_POLL_ATTEMPS) and batch_job["status"] in PENDING_STATUSES):

			sleep_interval = (30 * (2 ** poll_attempt) + (random.randint(0, 10000) / 1000))

			print("Batch Job not ready, sleeping for %s seconds" % sleep_interval)
			time.sleep(sleep_interval)
			batch_job = self.service.get(selector)["entries"][0]
			poll_attempt += 1

			if "downloadUrl" in batch_job:
				url = batch_job["downloadUrl"]["url"]
				print("Batch Job with Id '%s', Status '%s' and DownloadUrl '%s' is ready." % (batch_job["id"], batch_job["status"], url))
				return url

		raise Exception("Batch Job not finished downloading. Try checking later.")


	def getHelperId(self):
		return self.batchJobHelper.GetId()




	""" ////////////////////////////////////////////////////////////////////////////////////////////////////////////
		OPERATION BUILDERS TO PASS TO BATCH JOB
		////////////////////////////////////////////////////////////////////////////////////////////////////////////
	"""
	def addBudgetOps(self, str_budget_id, str_budget_name, str_budget_amount):
		"""	Input: BatchJobHelper Class, List of JSON objects
			Output: List of JSON objects

			Will build a list of JSON budget operations, to pass to the batch job
		"""
		budget_operation =	{
				"xsi_type": "BudgetOperation",
				"operand": {
					"name": str_budget_name,
					"budgetId": str_budget_id,
					"amount": int(str_budget_amount),
					"deliveryMethod": "STANDARD"
				},
				"operator": "ADD"
			}

		if budget_operation not in self.budgetOps:
			self.budgetOps.append(budget_operation)


	def addCampaignOps(self, str_camp_id, str_camp_name, str_budget_id):
		"""	Input: BatchJobHelper Class, List of JSON objects
			Output: List of JSON objects
		"""

		campaign_operation = {
				"xsi_type": "CampaignOperation",
				"operand": {
					"name": str_camp_name,
					"status": "PAUSED",
					"id": str_camp_id,
					"advertisingChannelType": "SEARCH",
					"networkSetting": {
						"targetGoogleSearch": "TRUE",
						"targetSearchNetwork": "TRUE",
						"targetContentNetwork": "FALSE"
					},
					"budget": {
							"budgetId": str_budget_id
					},
					"biddingStrategyConfiguration": {
						"biddingStrategyType": "MANUAL_CPC"
					}
				},
				"operator": "ADD"
			}

		if campaign_operation not in self.campaignOps:
			self.campaignOps.append(campaign_operation)


	def addAdGroupOps(self, str_campaignId, str_agId, str_agName, str_agBid):
		"""	Input: BatchJobHelper Class, List of JSON objects
			Output: List of JSON objects
		"""
	
		adgroup_operation = {
			"xsi_type": "AdGroupOperation",
			"operand": {
				"campaignId": str_campaignId,
				"id": str_agId,
				"name": str_agName,
				"status": "ENABLED",
				"urlCustomParameters": {"parameters": [{"key": "group", "value": str_agName}]},
				"biddingStrategyConfiguration": {
					"bids": [
						{
							"xsi_type": "CpcBid",
							"bid": {"microAmount": str_agBid}
						}]
				}
			},
			"operator": "ADD",
		}

		if adgroup_operation not in self.agOps:
			self.agOps.append(adgroup_operation)




	def addKeywordOps(self, str_agId, str_query, str_matchtype, str_finalUrl):
		"""	Input: BatchJobHelper Class, List of JSON objects
			Output: List of JSON objects
		"""

		keyword_operation = {
			"xsi_type": "AdGroupCriterionOperation",
			"operand": {
				"xsi_type": "BiddableAdGroupCriterion",
				"adGroupId": str_agId,
				"criterion": {
					"xsi_type": "Keyword",
					"text": str_query,
					"matchType": str_matchtype
				},
				"finalUrls": {"urls": [str_finalUrl]}
			},
			"operator": "ADD"
		}

		if keyword_operation not in self.kwOps:
			self.kwOps.append(keyword_operation)



	def addNegativeOps(self, str_agId, str_query, str_matchtype):
		"""	Input: BatchJobHelper Class, List of JSON objects
			Output: List of JSON objects
		"""

		# don't exclude on exact match keywords
		if str_matchtype != "EXACT":

			#get rid of plusses in case of BMM query/keyword
			query_string = str_query.replace("+", "")

			keyword_operation = {
				"xsi_type": "AdGroupCriterionOperation",
				"operand": {
					"xsi_type": "NegativeAdGroupCriterion",
					"adGroupId": str_agId,
					"criterion": {
						"xsi_type": "Keyword",
						"text": query_string,
						"matchType": "EXACT"
					},
					"criterionUse": "NEGATIVE"
				},
				"operator": "ADD"
			}

			if keyword_operation not in self.negativeOps:
				self.negativeOps.append(keyword_operation)




	def addAdOps(self, str_agId, list_ads):
		"""	Input: BatchJobHelper Class, List of JSON objects
			Output: List of JSON objects
		"""
		for ad in list_ads:

			ad_operation = {
				"xsi_type": "AdGroupAdOperation",
				"operand": {
					"adGroupId": str_agId,
					"ad": {
						"xsi_type": "ExpandedTextAd",
						"headlinePart1": ad["HeadlinePart1"],
						"headlinePart2": ad["HeadlinePart2"],
						"description": ad["Description"],
						# "path1": ad["ad"]["path1"],
						# "path2": ad["ad"]["path2"],
						"finalUrls": [ad["CreativeFinalUrls"][4:][:-4]]
					},
					"status": ad["Status"]
				},
				"operator": "ADD"
			}

			if ad_operation not in self.adOps:
				self.adOps.append(ad_operation)