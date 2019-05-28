from django.conf.urls import url
from . import views

app_name = "structure"

urlpatterns = [
	url(r"^$", views.sqrInput, name="sqrInput"),
	url(r"approveQueries", views.approveQueries, name="approveQueries"),
	url(r"selectDevicesMatchtypes", views.selectDevicesMatchtypes, name="selectDevicesMatchtypes"),
	url(r"download", views.download, name="download"),
	url(r"success", views.success, name="success"),
	url(r"buildNewAccount", views.buildNewAccount, name="buildNewAccount"),
	url(r"addTags", views.addTags, name="addTags"),
	]