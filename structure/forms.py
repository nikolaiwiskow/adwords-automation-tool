from django import forms
from django.forms import ModelForm

from .models import Account, TopicTag, TopicTagTrigger, CountryCode



# Initial form to select thresholds for SQR
class SqrForm(forms.Form):
	# get accounts list full of account objects from Accounts-DB
	accounts = Account.objects.values("account_id", "account_name")	

	#convert to list, to provide to choice-field
	accounts_list = []
	for account in accounts:
		accounts_list.append([account["account_id"], account["account_name"]])

	# specifying the form-fields
	account = forms.ChoiceField(label="Account", choices=accounts_list)
	time_range = forms.CharField(label="Time Range", max_length=200)
	cpl_threshold = forms.FloatField(label="Max. CPL", required=False)
	conversions_threshold = forms.IntegerField(label="Min. Conversions", required=False)
	impression_threshold = forms.IntegerField(label="Min. Impressions", required=False)
	click_threshold = forms.IntegerField(label="Min. Clicks", required=False)




# selection / deselection of queries after pulling them from adwords
class QueryApprovalForm(forms.Form):
	checkbox = forms.BooleanField(label="", initial=True, required=False)
	checkbox_negative = forms.BooleanField(label="", initial=False, required=False)
	agId = forms.CharField(label="", max_length=200, required=False, widget=forms.HiddenInput())
	campaignId = forms.CharField(label="", max_length=200, required=False, widget=forms.HiddenInput())
	name = forms.CharField(label="", max_length=200, required=False, widget=forms.TextInput(attrs={"readonly": "readonly"}))
	tags = forms.CharField(label="", max_length=200)
	finalUrl = forms.CharField(label="", max_length=200, widget=forms.HiddenInput())




# Selection in final step, which matchtypes + devices to output
class DevicesMatchtypesForm(forms.Form):
	device_list = [["mobile", "Mobile"], ["desktop", "Desktop"], ["tablet", "Tablet"]]
	matchtype_list = [["EXACT", "Exact"], ["PLUS", "Plus"], ["BROAD", "Broad"], ["PHRASE", "Phrase"]]
	outputs_list = [["excel", "Excel"], ["api", "API"]]

	devices = forms.MultipleChoiceField(label="Devices to output", choices=device_list, widget=forms.CheckboxSelectMultiple)
	matchtypes = forms.MultipleChoiceField(label="MatchTypes to output", choices=matchtype_list, widget=forms.CheckboxSelectMultiple)
	outputs = forms.ChoiceField(label="Select Output Option", choices=outputs_list, widget=forms.RadioSelect)



# Used to add tag-tigger words to DB
class AddTagForm(ModelForm):
	class Meta:
		model = TopicTagTrigger
		fields = ["country_code", "trigger_word", "tag"]


# Used to process uploaded excel file
class FileUploadForm(forms.Form):
	countries = [[entry.country_code, entry.country_name] for entry in CountryCode.objects.all()]

	device_list = [["mobile", "Mobile"], ["desktop", "Desktop"], ["tablet", "Tablet"]]
	matchtype_list = [["EXACT", "Exact"], ["PLUS", "Plus"], ["BROAD", "Broad"], ["PHRASE", "Phrase"]]


	file = forms.FileField(label="Upload a .xlsx file with keywords")
	final_url = forms.CharField(label="Final URL", max_length=200, required=False)
	country = forms.ChoiceField(label="Market", choices=countries)
	devices = forms.MultipleChoiceField(label="Devices to output", choices=device_list, widget=forms.CheckboxSelectMultiple)
	matchtypes = forms.MultipleChoiceField(label="MatchTypes to output", choices=matchtype_list, widget=forms.CheckboxSelectMultiple)

