from django.conf.urls import url
from . import views

app_name = "taganalysis"

urlpatterns = [
	url(r"^$", views.accountSelection, name="accountSelection"),
	url(r"results", views.results, name="results"),
	url(r"download", views.download, name="download"),
	url(r"charts", views.charts, name="charts"),
	]