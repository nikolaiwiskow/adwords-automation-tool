"""	Adwords Adgroup
"""

from .campaign import Campaign

class AdGroup(Campaign):

	def __init__(self):
		# get init from Campaign
		super(AdGroup, self).__init__()
		# add AG specific stuff
		self.agId = "not set"
		self.cpcBid = "not set"
		self.campaignName = "not set"
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
		"""

	# getters
	def getId(self):
		return self.agId

	def getCpcBid(self):
		return self.cpcBid

	def getCampaignId(self):
		return self.campaignId

	def getCampaignName(self):
		return self.campaignName

	# setters
	def setId(self, str_ag_id):
		self.agId = str_ag_id

	def setCpcBid(self, str_microns):
		self.cpcBid = str_microns

	def setCampaignId(self, camp_id):
		self.campaignId = camp_id

	def setCampaignName(self, str_name):
		self.campaignName = str_name