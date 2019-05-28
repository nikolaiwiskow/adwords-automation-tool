import json
import ast
import os

from walle.settings import BASE_DIR
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.forms import formset_factory

from .forms import SqrForm, QueryApprovalForm, DevicesMatchtypesForm, FileUploadForm, AddTagForm
from .models import Account, Negative, TopicTagTrigger, CountryCode

from adwords_entities.client import AdwordsClient
from adwords_entities.query import Query
from .sqr_positive import sqrPositive, buildInitialStructure
from structure.query_classification.output import Output

# Inital view to select account & thresholds
def sqrInput(request):
	# handle when form has been submitted
	if request.method == "POST":
		form = SqrForm(request.POST)
		
		# validate form inputs. Returns true if everything's ok
		if form.is_valid():

			account_id = form.cleaned_data["account"]

			query_params = {
								"cpl_thres": form.cleaned_data["cpl_threshold"],
								"time_range":  form.cleaned_data["time_range"].replace(" - ", ","), 
								"conv_thres":  form.cleaned_data["conversions_threshold"],
								"impression_thres":  form.cleaned_data["impression_threshold"],
								"click_thres": form.cleaned_data["click_threshold"]
			}

			# get adwords client for the account and pass to sqr_matching
			client = AdwordsClient().getById(account_id)

			# determine country-code
			account_name = Account.objects.get(account_id=account_id).account_name
			country_code = account_name[:2].lower()

			# "queries" will be coming in JSON string format, so we can save it in the session
			request.session["queries"] = sqrPositive(client, country_code, query_params)
			request.session["accountId"] = account_id
			request.session["countryCode"] = country_code
	
			# redirect to next step			
			return HttpResponseRedirect("approveQueries")

		else:
			print(form.errors)
			
	# if we're not in POST mode, form hasn't been submitted yet
	else:
		form = SqrForm()

	return render(request, "structure/sqr_input.html", {"form": form, "title": "SQR+ Beta", "subtitle": "Choose account & options"})




def approveQueries(request):
	# parsing objects from JSON
	queries = [json.loads(query) for query in request.session["queries"]]

	# if there are no queries, don't bother doing all the rest
	if len(queries) == 0:
		return render(request, "structure/success.html", {	"title": "Done :)", 
															"subtitle": "All caught up! No queries to add...", 
															"link_text": "Don't click!",
															"back_link": "/structure"})

	#initiate formset
	query_formset = formset_factory(QueryApprovalForm, extra=0)

	if request.method == "POST":
		formset = query_formset(request.POST)

		if formset.is_valid():

			output = []

			# agId, campaignId, finalUrl are passed as hidden form-fields. 
			for form in formset:
				cd = form.cleaned_data
				checkbox = cd.get("checkbox")
				checkbox_negative = cd.get("checkbox_negative")
				query = cd.get("name")
				ag_id = cd.get("agId")
				camp_id = cd.get("campaignId")
				tags = cd.get("tags")
				final_url = cd.get("finalUrl")

				if checkbox and not checkbox_negative:
					# save in JSON format to session
					output.append(json.dumps({"queryString": query, "agId": ag_id, "campaignId": camp_id, "tags": tags, "finalUrl": final_url}))

				if checkbox_negative:
					cc = CountryCode.objects.get(country_code=request.session["countryCode"])
					neg = Negative(negative=query, country_code=cc)
					neg.save()

			request.session["queries"] = output

			return HttpResponseRedirect("selectDevicesMatchtypes")

		else:
			print(formset.errors)
	else:
		formset = query_formset(initial=queries)

	return render(request, "structure/query_approval.html", {	"formset": formset, 
																"title": "Query approval", 
																"subtitle": "Deselect queries you don't want or that are tagged wrongly"})




# Final form to decide matchtype, devices & output mode
def selectDevicesMatchtypes(request):
	# Devices # Matchtypes Form
	if request.method == "POST":
		form = DevicesMatchtypesForm(request.POST)

		if form.is_valid():
			devices = form.cleaned_data["devices"]
			matchtypes = form.cleaned_data["matchtypes"]
			output = form.cleaned_data["outputs"]

			# queries coming in JSON format
			queries = [json.loads(entry) for entry in request.session["queries"]]
			client = AdwordsClient().getById(request.session["accountId"])

			queries_output = []

			# build final query list with matchtypes and devices
			for query in queries: 
				for device in devices:
					for matchtype in matchtypes:
						q = Query(query["queryString"])
						q.setAdGroupId(query["agId"])
						q.setTags(ast.literal_eval(query["tags"]))
						q.setFinalUrl(query["finalUrl"])
						q.setMatchType(matchtype)
						q.setDevice(device)
						q.buildAdgroupName()
						queries_output.append(q)


			# Output
			o = Output()
			o.setClient(client)
			o.setQueries(queries_output)

			if output == "excel":
				request.session["file_path"] = o.outputToXlsx()
				return HttpResponseRedirect("download")
			else:
				request.session["file_path"] = o.sendToApi()
				return HttpResponseRedirect("success")
			
		else:
			print(form.errors)

	else:
		form = DevicesMatchtypesForm()

	return render(request, "structure/final_step.html", {"form": form, "title": "Options", "subtitle":"Select devices and matchtypes"})



# General success view after a procedure
def success(request):
	return render(request, "structure/success.html", {	"title": "Done :)", 
														"subtitle": "Looks like everything went fine. Check the result your change-history in Adwords, or the link below.",
														"link_text": "Batch Job Results (XML)",
														"back_link": "/procreate/approve_queries",
														"batch_job_url": request.session["file_path"]})







# Upload view for excel file to be processed
def buildNewAccount(request):
	if request.method == "POST":
		form = FileUploadForm(request.POST, request.FILES)

		if form.is_valid():
			country_code = form.cleaned_data["country"]
			devices = form.cleaned_data["devices"]
			matchtypes = form.cleaned_data["matchtypes"]
			final_url = form.cleaned_data["final_url"]

			request.session["file_path"] = buildInitialStructure(country_code, request.FILES["file"], final_url, devices, matchtypes)
			return HttpResponseRedirect("download")

	else:
		form = FileUploadForm()

	return render(request, "structure/file_upload.html", {	"form": form, 
															"title": "Create new structure from .xlsx keyword list", 
															"subtitle": "Format: .xlsx, single column with the keywords. No headers."})



# Download view used in build_new_account
def download(request):
	file_path = request.session["file_path"]
	path = os.path.join(BASE_DIR, file_path)

	if os.path.exists(path):
		with open(file_path, "rb") as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response["Content-Disposition"] = "inline; filename="+os.path.basename(path)
			return response
	raise Http404



def addTags(request):
	if request.method == "POST":
		form = AddTagForm(request.POST)

		if form.is_valid():
			country_code = form.cleaned_data["country_code"]
			trigger = form.cleaned_data["trigger_word"]
			tag = form.cleaned_data["tag"]

			new_trigger = TopicTagTrigger(country_code=country_code, trigger_word=trigger, tag=tag)
			new_trigger.save()

			return HttpResponseRedirect("/structure")
		else:
			print(form.errors)

	else:
		form = AddTagForm()

	return render(request, "structure/final_step.html", {"form": form, "title": "Add a new tag", "subtitle": "palaver"})