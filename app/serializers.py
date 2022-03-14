from rest_framework.serializers import ModelSerializer
from rest_framework import serializers
from .models import App, Subscription, Plan
from collections import OrderedDict
from django.contrib.auth.models import User



class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["first_name", "last_name", "email", "username", "password"]
        extra_fields = {
           "password": {"write_only": True}
        }

    
    def create(self, validated_data):
        
        user = User(**validated_data)
        user.is_superuser = False
        user.is_staff = False
        user.is_admin = False
        user.save()
        user.set_password(validated_data.get('password'))
        user.save()
        return user


class PlanSerializer(ModelSerializer):

    class Meta:
        model = Plan
        fields = ["name", "price"]



class SubscriptionSerializer(ModelSerializer):
    
    plan = PlanSerializer(many=False, read_only=True)
    class Meta:
        model = Subscription
        fields = ["plan_type", "active", "plan"]


class AppSerializer(ModelSerializer):
    subscription = SubscriptionSerializer(many=False, read_only=True)
    class Meta:
        model = App
        fields = ["id", "name", "description", "subscription"]


    def create(self, validated_data):
        print(validated_data, "in create")
        plan = Plan(name="Free", price=0)
        plan.save()
        subscription = Subscription(plan_type="Free", plan=plan)
        subscription.save()
        app = App(**validated_data, subscription=subscription)
        app.save()
        print("print the data of the app ->", app)
        return app



class AppUpdateSerializer(serializers.Serializer):

    name = serializers.CharField(max_length=255, required=False)
    description = serializers.CharField(max_length=255, required=False)
    subscription = SubscriptionSerializer(required=False)
    plan = PlanSerializer(required=False)

    def update(self, instance, validated_data):

        instance.name = validated_data.pop("name", instance.name)
        instance.description = validated_data.pop("description", instance.description)
        subscription =  validated_data.pop("subscription", instance.subscription)
        plan = validated_data.pop("plan", instance.subscription.plan)

        if (type(subscription) == OrderedDict) or (type(plan) == OrderedDict):
            if type(subscription) == OrderedDict:
                instance.subscription.plan = subscription.get("plan", instance.subscription.plan)
                instance.subscription.plan_type = subscription.get("plan_type", instance.subscription.plan_type)
                instance.subscription.active = subscription.get("active", instance.subscription.active)
                instance.save()

            if type(plan) == OrderedDict:
                instance.subscription.plan.name = plan.get("name", instance.subscription.plan.name)
                instance.subscription.plan.price = plan.get("price", instance.subscription.plan.price)

        else:
            instance.subscription =  subscription
            instance.subscription.plan = plan
        instance.save()
        return instance












