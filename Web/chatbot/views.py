from django.shortcuts import render
from rest_framework.views import APIView
from django.http import HttpResponse, JsonResponse
from rest_framework import permissions

# Create your views here.
class call_model(APIView):
    #permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request, format=None):
        if 't' not in request.session:
            request.session['t'] = 0
        else:
            request.session['t'] +=1
        
        username = request.user.username
        return JsonResponse( request.session['t'], safe=False)

    def post(self, request, format=None):
        if 't' not in request.session:
            request.session['t'] = 0
        else:
            request.session['t'] -=1
        return JsonResponse(request.session['t'], safe=False)
