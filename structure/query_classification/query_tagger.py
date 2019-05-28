from structure.models import CountryCode, TopicTagTrigger


class QueryTagger(object):

	def __init__(self):
		self.masterList = None


	def getTopicTags(self, str_query, country_code="US"):
		self.setMasterList(country_code)
		topic_tags = []

		query_length = len(str_query) - str_query.count(" ")

		hits = []
		for row in self.masterList:
			tag = row[0]
			trigger = row[1]
			trigger_length = len(trigger) - trigger.count(" ")

			if trigger_length > query_length:
				break

			match_index = str_query.find(trigger)

			if match_index >= 0:
				match = {	"trigger": trigger,
							"tag": tag,
							"charIndexes": range(match_index, (match_index+trigger_length)),
							"length": trigger_length,
							"leftoverSpots": query_length - trigger_length	
						}
				hits.append(match)

		if hits:
			best_hit = hits[-1]
			final_hits = [best_hit]

			for hit in reversed(hits):
				if hit["length"] <= best_hit["leftoverSpots"] and not set(hit["charIndexes"]).intersection(best_hit["charIndexes"]) and hit != best_hit:
					final_hits.append(hit)
			return self.createListFromDeterminedTags(final_hits)

		else:
			return ["noTag"]


	def createListFromDeterminedTags(self, list_hits):
		""" Input: List of objects
			Output: List of strings
		"""
		tag_list = []
		for hit in list_hits:
			tag = hit["tag"]

			if tag not in tag_list and tag != "negative" and tag != "algo":
				tag_list.append(tag)

		tag_list.sort()
		return tag_list


	def wordCount(self, str_query):
		return len(str_query.split(" "))


	def setMasterList(self, str_country_code):
		cc = CountryCode.objects.get(country_code=str_country_code)
		triggers = TopicTagTrigger.objects.filter(country_code=cc)

		trigger_list = [[str(trigger.tag), str(trigger.trigger_word)] for trigger in triggers]
		self.masterList = sorted(trigger_list, key=lambda x: (len(x[1]) - x[1].count(" ")))