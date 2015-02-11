from django.template import RequestContext, loader, Context
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

@login_required(login_url='/')
def authenticated_page(request):
	return HttpResponse(loader.get_template('auth.html').render(Context({})))