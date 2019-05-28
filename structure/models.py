from django.db import models

# Create your models here.
class MccCredential(models.Model):
	mcc_name = models.CharField(max_length=200)
	client_id = models.CharField(max_length=200)
	client_secret = models.CharField(max_length=200)
	refresh_token = models.CharField(max_length=200)
	dev_token = models.CharField(max_length=200)
	client_customer_id = models.CharField(max_length=200)
	user_agent = models.CharField(max_length=200)

	def __str__(self):
		return self.mcc_name

class Account(models.Model):
	account_name = models.CharField(max_length=200)
	account_id = models.CharField(max_length=200)
	mcc = models.ForeignKey(MccCredential, on_delete=models.CASCADE)

	def __str__(self):
		return self.account_name

class CountryCode(models.Model):
	country_code = models.CharField(max_length=200)
	country_name = models.CharField(max_length=200)

	def __str__(self):
		return self.country_code

class Negative(models.Model):
	negative = models.CharField(max_length=200)
	country_code = models.ForeignKey(CountryCode, on_delete=models.CASCADE)

	def __str__(self):
		return self.negative

class TopicTag(models.Model):
	tag = models.CharField(max_length=200)

	def __str__(self):
		return self.tag

class TopicTagTrigger(models.Model):
	country_code = models.ForeignKey(CountryCode, on_delete=models.CASCADE)
	trigger_word = models.CharField(max_length=200)
	tag = models.ForeignKey(TopicTag, on_delete=models.CASCADE)

	def __str__(self):
		return self.trigger_word

