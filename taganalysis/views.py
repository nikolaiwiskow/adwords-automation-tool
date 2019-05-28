import os
import json
from walle.settings import BASE_DIR

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, QueryDict

from adwords_entities.client import AdwordsClient
from .taganalysis import tagAnalysis
from .forms import AccountSelectionForm, TagFilterForm

from pprint import pprint

# Create your views here.
def accountSelection(request):
	# handle when form has been submitted
	if request.method == "POST":
		form = AccountSelectionForm(request.POST)
		# validate form inputs. Returns true if everything's ok
		if form.is_valid():
			# get user entries from form inputs
			account_id = form.cleaned_data["account"]
			time_range = form.cleaned_data["time_range"].replace(" - ", ",")
			# get adwords client for the account and pass to sqr_matching
			client = AdwordsClient().getById(account_id)

			t = tagAnalysis()
			t.getData(client, time_range)
			request.session["all_data"] = t.rawData
			request.session["filtered_result"] = t.clusterRowsPerTag()
			
			return HttpResponseRedirect("results")

		else:
			print(form.errors)
			
	# if we're not in POST mode, form hasn't been submitted yet
	else:
		form = AccountSelectionForm()

	return render(request, "structure/sqr_input.html", {"form": form, "title": "Tag Analysis", "subtitle": "Choose account"})


# Results per tag, aggreated on one tag
def results(request):
	data, hl = processData(request)
	url_values = QueryDict(request.META["QUERY_STRING"])
	ag_toggle_text = "AG View" if "ags" not in url_values else "Tag View"
		
	return render(request, "taganalysis/results.html", {"title": hl, "data": data, "ag_toggle_text": ag_toggle_text})


def charts(request):
	data, hl = processData(request)
	data_json = json.dumps(data)

	url_values = QueryDict(request.META["QUERY_STRING"])
	ag_toggle_text = "AG View" if "ags" not in url_values else "Tag View"
	
	return render(request, "taganalysis/charts.html", {"title": hl, "filtered_data": data_json, "ag_toggle_text": ag_toggle_text})


def processData(request):
	t = tagAnalysis()
	t.rawData = request.session["all_data"]

	url_values = QueryDict(request.META.get("QUERY_STRING"))

	#check for url filters
	if url_values:
		device = url_values["device"] if "device" in url_values else None
		matchtype = url_values["matchtype"] if "matchtype" in url_values else None

		if "tag" in url_values:
			tags = url_values["tag"][1:]
			tags_list = tags.split(".")
			tags = []
			for tag in tags_list:
				tags.append("." + tag)

		else:
			tags = None

		# if same url gets called twice, it's most likely a drilldown to adgroup level
		if "ags" in url_values: 
			data = data = request.session["filtered_result"] = t.clusterRowsPerAgName(tags, device, matchtype)
		else:
			data = request.session["filtered_result"] = t.clusterRowsPerTag(tags, device, matchtype)

		request.session["filtered_raw_data"] = t.rawDataCluster
		hl = buildHeadline(tags, device, matchtype)	

	else:
		data = request.session["filtered_result"] = t.clusterRowsPerTag()
		request.session["filtered_raw_data"] = t.rawDataCluster
		hl = "Results"

	return data, hl



def buildHeadline(list_tags=None, str_device=None, str_matchtype=None):
	if list_tags:
		tags_string = ""
		for tag in list_tags:
			tags_string += tag
	else:
		tags_string = "All Tags"

	l = [tags_string, str_device, str_matchtype]
	hl = ""
	for index, i in enumerate(l):
		if i and index > 0:
			hl += " - " + i.title()
		elif i: 
			hl += i
	return hl








# Download view used in build_new_account
def download(request):
	url_values = QueryDict(request.META.get("QUERY_STRING"))

	t = tagAnalysis()
	t.rawData = request.session[url_values["mode"]]
	file_path = t.outputToXlsx()

	path = os.path.join(BASE_DIR, file_path)

	if os.path.exists(path):
		with open(file_path, "rb") as fh:
			response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
			response["Content-Disposition"] = "inline; filename="+os.path.basename(path)
			return response
	raise Http404