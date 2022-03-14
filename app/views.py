from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND, HTTP_204_NO_CONTENT
from rest_framework.views import APIView
from .models import App, Subscription, Plan
from .serializers import AppSerializer, AppUpdateSerializer, UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly 


class UserRegisterView(APIView):

    def post(self, request):

        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)

        return Response(serializer.errors)

class UserLoginView(APIView):

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")

        if not username or not password:
            return Response("Please enter username and password")

        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return Response("login success")
        
        return Response({"login unsuccessful"})


class UserLogoutView(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):

        logout(request)
        return Response("successfully logged out")



class UserResetPasswordView(APIView):


    permission_classes = [IsAuthenticated]

    def put(self, request):
        password = request.data.get("password")

        if password:
            request.user.set_password(password)
            request.user.save()
            return Response("Password has been reset")


        return Response("Please enter a password")




class AppGetView(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        apps = App.objects.all()
        serializer = AppSerializer(apps, many=True)    
        return Response(serializer.data)
    
    def post(self, request):
        serializer = AppSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        return Response(serializer.errors)


class AppUpdateView(APIView):
    
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, id):

        try:
            app = App.objects.get(pk=id)
        except App.DoesNotExist:
            return Response("App doen't not found", status=HTTP_404_NOT_FOUND)


        serializer = AppSerializer(instance=app, many=False)
        return Response(serializer.data)


    def put(self, request, id):

        try:
            app = App.objects.get(pk=id)
        except App.DoesNotExist:
            return Response("App doen't not found", status=HTTP_404_NOT_FOUND)
        
        serializer = AppUpdateSerializer(data=request.data, instance=app, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)    

        return Response(serializer.errors, status=HTTP_404_NOT_FOUND)

    def delete(self, request, id):

        try:
            app = App.objects.get(pk=id)
        except App.DoesNotExist:
            return Response("App doen't not found", status=HTTP_404_NOT_FOUND)

        serializer = AppSerializer(instance=app, many=False)
        app.delete()
        return Response("App has been deleted successfully", status=HTTP_204_NO_CONTENT)



class CancelAppSubscription(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request, id):

        try:
            app = App.objects.get(pk=id)
        except App.DoesNotExist:
            return Response("App doen't not found", status=HTTP_404_NOT_FOUND)
            
        app.subscription.plan_type = ""
        app.subscription.active = False
        app.subscription.plan = None
        app.subscription.save()
        serializer = AppSerializer(instance=app, many=False)
        return Response(serializer.data)

        