from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from core.models import *
import os.path

from core.models import Pathway

import xml.etree.cElementTree as et
import requests, json, re
from website import settings

@login_required(login_url='/openemr/signup/')
def index(request,extension):

    pathways = Pathway.objects.filter(user_id=request.user.id).order_by('-id')

    if pathways:
        if os.path.isfile(settings.MEDIA_ROOT+'/'+str(pathways[0].pathway_xml)):
            xml = et.fromstring(open(settings.MEDIA_ROOT+'/'+str(pathways[0].pathway_xml), "r").read())

            response = [ _parse_process(process) for process in xml.findall("./process_table/process") ]

            if(extension=="json"):
                return HttpResponse(json.dumps(response), content_type='application/json')

            else:
                context = RequestContext(request, { "data": response })
                return HttpResponse(loader.get_template('process.html').render(context))
        else:
            pathways[0].pathway_xml = "example.xml"
            pathways[0].save()
            return HttpResponseRedirect('/processes' )
    else:
        return HttpResponseRedirect( '/add_pathway/' )


def _parse_process(process):
    return { "id"       : process.attrib["pid"],
             "type"     : "process",
             "name"     : re.search(r'\./(.*)\.pml',process.attrib["model"]).group(1).replace("_"," "),
             "sequence" : _parse_seq(process) }

def _parse_action(elem):
    return { "type"  : "action",
             "name"  : elem.attrib["name"].replace("_"," "),
             "info"  : re.sub(r'(\t|(<br>)|(\(null\)\n)|(\")|(\A\n))', '',elem.find("script").text),
             "state" : elem.attrib["state"]}

def _parse_branch(elem):
    return { "type"        : "branch",
             "sequences"   : [ _parse_seq(seq) for seq in elem.findall("./sequence")]}

def _parse_seq(seq):

    p = []

    for elem in seq.findall("*"):

        if elem.tag == "action":
            p.append(_parse_action(elem))
        elif elem.tag == "branch":
            p.append(_parse_branch(elem))

    return p
