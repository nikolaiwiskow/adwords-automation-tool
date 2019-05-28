from django.contrib import admin

from .models import MccCredential, Account, CountryCode, TopicTag, TopicTagTrigger, Negative

# Register your models here.
admin.site.register(MccCredential)
admin.site.register(Account)
admin.site.register(CountryCode)
admin.site.register(TopicTag)
admin.site.register(TopicTagTrigger)
admin.site.register(Negative)