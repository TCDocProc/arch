from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.core.files import File
from django.core.files.base import ContentFile
from django.conf import settings
from core.models import Pathway
from django.views.decorators.csrf import csrf_exempt
import requests, json

# Create your views here.
@csrf_exempt
def sign_up(request):
    context = RequestContext(request, {
        "login_url": ""
     })

    if request.method == "POST":
         context["failed"] = True

    if request.user.is_authenticated():
        return HttpResponseRedirect("/")

    if request.method == "POST" and 'username' in request.POST and 'password' in request.POST:
        url = settings.OPENEMR_ENDPOINT

        username = request.POST['username']
        password = request.POST['password']
        payload = {'username': username, 'password': password}

        # POST with form-encoded data
        r = requests.post(url, data=payload)

        response = None
        try:
            # Response, status etc
            response = json.loads(r.text)
        except:
            context["openemr_error"] = True
            context["failed"] = False
            return HttpResponse(loader.get_template('signup.html').render(context))

        if response['login_success']:
            try:
                user_prof = User.objects.get(username=username)
            except User.DoesNotExist:
                user_prof = User.objects.create_user(username, '', password)
                user_prof.save()

            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                doc = Pathway()
                doc.user_id = user_prof
                doc.pathway_xml.save(username+".xml", ContentFile(response['xml']), save=True)
                doc.save()
                return HttpResponseRedirect("/") 

    return HttpResponse(loader.get_template('signup.html').render(context))
