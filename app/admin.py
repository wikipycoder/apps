from django.contrib import admin
from .models import Plan, Subscription, App

models  = [Plan, Subscription, App]

for model in models:
    admin.site.register(model)
