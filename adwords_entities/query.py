"""	Adwords Search Query Class
"""

from .adgroup import AdGroup

class Query(AdGroup):

	def __init__(self, query_string):
		super(Query, self).__init__()
		# override
		self.name = query_string
		self.tokens = query_string.split(" ")
		self.tags = None
		self.finalUrl = "not set"
		self.queryLength = len(self.name)
		self.agName = "not set"
		self.campaignName = "not set"
		self.agName = "not set"
		self.matchTypeOutput = None
		self.ads = None
		self.agBid = None
		"""	inherits from campaign super

		self.campaignId = "not set"
		self.budget = "not set"
		self.name = "not set"
		self.matchType = "not set"
		self.device = "not set"
		self.status = "not set"
		self.biddingStrategy = "not set"
		self.children = []
		self.labels = []

			inherits from AdGroup
		self.agId = "not set"
		self.cpcBid = "not set"
		"""		

	# Getter methods
	def getQueryString(self):
		return self.name

	def getTokens(self):
		return self.tokens

	def getCampaignName(self):
		return self.campaignName

	def getCampaignId(self):
		return self.campaignId

	def getAdGroupName(self):
		return self.agName

	def getAdGroupId(self):
		return self.agId

	def getTags(self):
		return self.tags

	def getFinalUrl(self):
		return self.finalUrl

	def getAdGroupBid(self):
		return self.agBid

	def getAds(self):
		return self.ads

	def getMatchTypeOutput(self):
		return self.matchTypeOutput

	# Setter methods
	def setQueryString(self, query_string):
		self.name = query_string
		self.tokens = self.queryString.split(" ")

	def setCampaignName(self, camp_name):
		self.campaignName = camp_name

	def setCampaignId(self, camp_id):
		self.campaignId = camp_id

	def setAdGroupName(self, ag_name):
		self.agName = ag_name

	def setAdGroupId(self, ag_id):
		self.agId = ag_id

	def setTags(self, tag_list):
		self.tags = tag_list

	def setFinalUrl(self, final_url_string):
		self.finalUrl = final_url_string

	def setAds(self, list_ads):
		self.ads = list_ads

	def setMatchType(self, str_match_type):
		self.matchType = self.matchTypeOutput = str_match_type

		if str_match_type == "PLUS":
			self.name = "+"+ self.name.replace(" ", " +")
			self.matchTypeOutput = "BROAD"


	def setAdGroupBid(self, bid_string):
		if len(bid_string) < 5:
			self.agBid = "50000"
		else:
			self.agBid = bid_string



	def buildAdgroupName(self):
		"""	Build the adgroup name from matchtypes, devices and tags. Need to set those before calling this
		"""
		devices = {"mobile": ".m-", "tablet": ".t-", "desktop": ".d-"}
		matchtypes = {"EXACT": ".ex-", "PLUS": ".pl-", "BROAD": ".br-", "PHRASE": ".ph-"}

		ag_name = devices[self.device] + matchtypes[self.matchType] + "--"

		for tag in self.tags:
			ag_name += "." + tag + "-"

		self.agName =  ag_name + "--" + self.name.replace(" ", "_").replace("+", "")


	def __str__(self):
		print("Text: " + self.queryString)
		print("Tags: " + str(self.tags))
		print("Final Url: " + self.finalUrl)
		print("ParentName: " + self.parent.getName())
		print("ParentId: " + self.parent.getId())
		return