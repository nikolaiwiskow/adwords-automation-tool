from django import forms


from structure.models import Account, MccCredential

class AccountSelectionForm(forms.Form):
	# get accounts list full of account objects from Accounts-DB
	accounts = Account.objects.values("account_id", "account_name")

	#convert to list, to provide to choice-field
	accounts_list = []
	for i in accounts:
		accounts_list.append([i["account_id"], i["account_name"]])

	# specifying the form-fields
	account = forms.ChoiceField(label="Account to clone", choices=accounts_list)
	time_range = forms.CharField(label="Time Range", max_length=200)


class TagFilterForm(forms.Form):
	tags = forms.CharField(label="Tags", max_length=200, widget=forms.Textarea)
	