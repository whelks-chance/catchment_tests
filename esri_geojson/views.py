import json

from django.http import HttpResponse
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from django.views.decorators.csrf import csrf_exempt
import requests


def home(request):
    return render_to_response('home.html', {}, context_instance=RequestContext(request))


@csrf_exempt
def record_geojson(request):
    print(request.POST)

    geojson_json = {'geojson': 'No geojson in HTTP POST'}
    geojson_string = request.POST.get('geojson_str')
    # print(geojson_string)

    if geojson_string:
        geojson_json = json.loads(geojson_string)

        # print(geojson_json)

        shapefile_create_url = 'http://ogre.adc4gis.com/convertJson'

        result = requests.post(
            shapefile_create_url,
            data={
                'json': geojson_string
            }
        )

        print(result.status_code)
        # print(result.text)

        with open('shape.zip', 'wb') as fd:
            for chunk in result.iter_content(1024):
                fd.write(chunk)

        return HttpResponse(result.iter_content(1024), content_type="application/octet-stream")
    else:

        return HttpResponse(json.dumps(geojson_json), content_type="application/json")
