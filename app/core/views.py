from django.template import RequestContext, loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

import time

from forms import UploadPathwayForm
from core.models import UploadForm, Pathway


def index(request):
    return HttpResponse(loader.get_template('index.html').render(Context({})))

@login_required(login_url='/openemr/signup/')
def add_pathway(request):
    pathways = Pathway.objects.filter(user_id=request.user)

    #If defaults button is clicked
    default = request.GET.get('default', '')
    if default != '':
        instance = Pathway(pathway_xml="example.xml",user_id=request.user)
        instance.save()
        return HttpResponseRedirect('/processes' )

    if not pathways:

        if request.method=="POST":

            xmlForm = UploadForm(request.POST, request.FILES)

            if xmlForm.is_valid():
                xmlForm.instance.user_id = request.user
                xmlForm.save()
                return HttpResponseRedirect('/processes' )
        else:
            xmlForm=UploadForm()

        return render(request,'upload_form.html',{'form':xmlForm})

    else:
        return HttpResponseRedirect('/processes' )

def sample_login(request):
    t = int(time.time())
    try:
        user_prof = User.objects.get(username='sample%s' % (str(t)))
    except User.DoesNotExist:
        user_prof = User.objects.create_user('sample%s' % (str(t)), '', 'sample')
        user_prof.save()

    user = authenticate(username='sample%s' % (str(t)), password='sample')
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("/") 


def integrate(request):
    context = RequestContext(request)
    context['test'] = request.GET['test']
    return HttpResponse(loader.get_template('core/integrate.html').render(context))
