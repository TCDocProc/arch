from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context

# Create your views here.

def sign_up(request):
    if request.method == "GET":
        context = RequestContext(request, {
            "login_url": ""
         })
        return HttpResponse(loader.get_template('signup.html').render(context))
