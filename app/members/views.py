from django.template import RequestContext, loader, Context
from django.http import HttpResponse


def index(request):
    return HttpResponse(loader.get_template('index.html').render(Context({})))
    # return HttpResponse("Test")
