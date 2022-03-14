from django.db import models


class Plan(models.Model):

    name = models.CharField(max_length=255, default="Free")
    price = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Subscription(models.Model):

    plan = models.OneToOneField(Plan, on_delete=models.CASCADE, null=True)
    plan_type = models.CharField(default="Free", max_length=255)
    active = models.BooleanField(default=True)

    def __str__(self):

        return self.plan_type
        

class App(models.Model):

    name = models.CharField(max_length=255)
    description = models.TextField()
    subscription = models.OneToOneField(Subscription, on_delete=models.CASCADE)

    def __str__(self):
        return self.name






