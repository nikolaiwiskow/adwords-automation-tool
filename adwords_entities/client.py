from googleads import adwords, oauth2

from structure.models import Account

class AdwordsClient(object):

	def getById(self, str_acc_id):
		account_credentials = Account.objects.get(account_id=str_acc_id).mcc

		client_id = account_credentials.client_id
		client_secret = account_credentials.client_secret
		refresh_token = account_credentials.refresh_token
		developer_token =  account_credentials.dev_token
		user_agent =  account_credentials.user_agent

		oauth2_client = oauth2.GoogleRefreshTokenClient(client_id, client_secret, refresh_token)

		adwords_client = adwords.AdWordsClient(developer_token, oauth2_client, user_agent, client_customer_id=str_acc_id)
		return adwords_client