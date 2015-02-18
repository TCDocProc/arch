from django.http import HttpResponse

import xml.etree.cElementTree as et
import requests, json, re
from website import settings

def index(request):

    r = requests.get("http://proisis.lero.ie/~jnoll/carepathways/peos.cgi")
    xml = ""
    if r.status_code == 200:
        xml = et.fromstring(r.text)
    else:
        xml = et.fromstring(open(settings.STATIC_ROOT+"/xml/pathways.xml", "r").read())

    response = [ _parse_process(process) for process in xml.findall("./process_table/process") ]

    return HttpResponse(json.dumps(response), content_type='application/json')

def _parse_process(process):
    return { "id"       : process.attrib["pid"],
             "type"     : re.search(r'\./(.*)\.pml',process.attrib["model"]).group(1),
             "sequence" : _parse_seq(process) }

def _parse_action(elem):
    return { "type"        : "action",
             "name"        : elem.attrib["name"],
             "description" : re.sub(r'(\t|(<br>)|(\n\(null\)\n)|(\")|(\A\n))', '',elem.find("script").text),
             "state"       : elem.attrib["state"]}

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
