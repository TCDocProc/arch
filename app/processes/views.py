from django.http import HttpResponse, HttpResponseRedirect
from django.template import RequestContext, loader, Context
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import ensure_csrf_cookie
from core.models import *
import os.path

from core.models import Pathway

import xml.etree.cElementTree as et
import requests, json, re
from website import settings

@login_required(login_url='/openemr/signup/')
@ensure_csrf_cookie
def index(request,extension):

    pathways = Pathway.objects.filter(user_id=request.user.id).order_by('-id')

    if request.method=="GET":
        if pathways:
            if os.path.isfile(settings.MEDIA_ROOT+'/'+str(pathways[0].pathway_xml)):
                xml = open(settings.MEDIA_ROOT+'/'+str(pathways[0].pathway_xml), "r").read()
                xml = et.fromstring(xml)

                response = [ _parse_process(process) for process in xml.findall("./process_table/process") ]

                if(extension=="json"):
                    return HttpResponse(json.dumps(response), content_type='application/json')

                else:
                    context = RequestContext(request, { "data": response })
                    return HttpResponse(loader.get_template('process.html').render(context))
            else:
                pathways[0].delete()
                return HttpResponseRedirect('/add_pathway/' )
        else:
            return HttpResponseRedirect( '/add_pathway/' )

    elif request.method=="DELETE":

        pathways.delete()
        return HttpResponse("", status=204)

    else:

        return HttpResponse("Method not allowed", status=405)

# Private function to parse process in index
def _parse_process(process):
    return { "id"       : process.attrib["pid"],
             "type"     : "process",
             "name"     : re.search(r'\./(.*)\.pml',process.attrib["model"]).group(1).replace("_"," "),
             "sequence" : _parse_seq(process) }

# Private recursive function to parse process table
def _parse_action(elem):
    return { "type"  : "action",
             "name"  : elem.attrib["name"].replace("_"," "),
             "info"  : re.sub(r'(\t|(<br>)|(\(null\)\n)|(\")|(\A\n))', '',elem.find("script").text),
             "state" : elem.attrib["state"]}

# Private recursive function to parse process table
def _parse_branch(elem):
    return { "type"        : "branch",
             "sequences"   : [ _parse_seq(seq) for seq in elem.findall("*")]}

# Private recursive function to parse process table
def _parse_seq(seq):
    p = []
    for elem in seq.findall("*"):

        if elem.tag == "action":
            p.append(_parse_action(elem))
        elif elem.tag == "branch":
            p.append(_parse_branch(elem))
        elif elem.tag == "iteration":
            p += _parse_seq(elem)
    return p
