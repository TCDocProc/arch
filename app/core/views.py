from django.template import RequestContext, loader, Context
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render

from forms import UploadPathwayForm
from core.models import UploadForm, Pathway


def index(request):
    return HttpResponse(loader.get_template('index.html').render(Context({})))

@login_required(login_url='/accounts/signup/')
def add_pathway(request):
    pathways = Pathway.objects.filter(user_id=request.user)

    if not pathways:

        if request.method=="POST":

            xmlForm = UploadForm(request.POST, request.FILES)

            if xmlForm.is_valid():
                xmlForm.instance.user_id = request.user
                xmlForm.save()
                return HttpResponseRedirect('/processes/user/'+str(request.user.id) )
        else:
            xmlForm=UploadForm()

        return render(request,'upload_form.html',{'form':xmlForm})

    else:
        return HttpResponseRedirect('/processes/user/'+str(request.user.id) )

def integrate(request):
    context = RequestContext(request)
    context['test'] = request.GET['test']
    return HttpResponse(loader.get_template('core/integrate.html').render(context))