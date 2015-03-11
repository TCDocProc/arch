from django.template import RequestContext, loader, Context
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from forms import UploadPathwayForm
from django.shortcuts import render
from members.models import UploadForm, Pathway
from django.http import HttpResponseRedirect
from django.core.urlresolvers import reverse
from members import models as m
def index(request):
    return HttpResponse(loader.get_template('index.html').render(Context({})))

@login_required(login_url='/accounts/signup/')
def authenticated_page(request):
    context = RequestContext(request, {})
    return HttpResponse(loader.get_template('auth.html').render(context))

#           newdoc = Pathway(pathway_xml = request.FILES['xmlfile'], user_id = request.user)

@login_required(login_url='/accounts/signup/')
def add_pathway(request):
    sc=m.Pathway.objects.filter(user_id=request.user)
    if sc.count>0:
        if request.method=="POST":
            xmlForm = UploadForm(request.POST, request.FILES)
            if xmlForm.is_valid():
                xmlForm.instance.user_id = request.user
                xmlForm.save()
                return HttpResponseRedirect(reverse('process_view', kwargs={'user_id': request.user.id,'extension':'html'}))
        else:
            xmlForm=UploadForm()
        return render(request,'upload_form.html',{'form':xmlForm})
    else:
        return HttpResponseRedirect(reverse('process_view', kwargs={'user_id': request.user.id,'extension':'html'}))