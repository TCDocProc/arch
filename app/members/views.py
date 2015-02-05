from django.template import RequestContext, loader
from django.http import HttpResponse


def index(request):
    template = loader.get_template('members/templates/index.html')
    return HttpResponse(template.render())
