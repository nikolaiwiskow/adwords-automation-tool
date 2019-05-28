""" Adwords Campaign
"""

class Campaign(object):

	def __init__(self):
		self.campaignId = "not set"
		self.budget = 0
		self.name = "not set"
		self.matchType = "not set"
		self.device = "not set"
		self.status = "PAUSED"
		self.biddingStrategy = "MANUAL_CPC"
		self.children = []
		self.labels = []

	# getters
	def getId(self):
		return self.campaignId

	def getBudget(self):
		return self.budget

	def getName(self):
		return self.name

	def getMatchType(self):
		return self.matchType

	def getDevice(self):
		return self.device

	def getStatus(self):
		return self.status

	def getBiddingStrategy(self):
		return self.biddingStrategy

	def getChildren(self):
		return self.children

	def getLabels(self):
		return self.labels

	#setters
	def setId(self, str_campaign_id):
		self.campaignId = str_campaign_id

	def setBudget(self, str_budget_microns):
		self.budget = str_budget_microns

	def setName(self, str_name):
		self.name = str_name

	def setMatchType(self, str_match_type):
		self.matchType = str_match_type

	def setStatus(self, str_status):
		self.status = str_status

	def setBiddingStrategy(self, str_bidding_strategy):
		self.biddingStrategy = str_bidding_strategy

	def setDevice(self, str_device):
		self.device = str_device


	# add 1 adgroup
	def addChild(self, class_ag):
		self.children.append(class_ag)
	# add a list of adgroups
	def addChildrenList(self, array_class_ag):
		self.children.extend(array_class_ag)
	# replace existing adgroups by new list
	def setChildrenList(self, array_class_ag):
		self.children = array_class_ag

	# add 1 label
	def addLabel(self, str_label):
		self.lables.append(str_label)
	# add a list of labels
	def adddLabelList(self, array_str_labels):
		self.labels.extend(array_str_labels)
	# replace existing labeles with new list
	def setLabelList(self, array_str_labels):
		self.labels = array_str_labels