# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.urls import reverse
from django.conf import settings

from channels import Group
import uuid
import os
import os.path as osp
import random
import requests
from urlparse import urlparse
import urllib2
import traceback

from refer.utils import log_to_terminal
import refer.constants as constants
from refer.sender import sender_comprehension

# Create your views here.
def index(request, template_name='index.html'):
  return render(request, 'index.html')

def generation(request, template_name='generation.html'):
  return render(request, 'generation.html')

def comprehension(request, template_name='comprehension.html'):
  socketid = uuid.uuid4()
  if request.method == "POST":
    try:
      img_path = request.POST.get('img_path')
      img_path = urllib2.unquote(img_path)
      expression = request.POST.get('expression')
      socketid = request.POST.get('socketid')

      # abs_image_path = os.path.join(settings.BASE_DIR, str(img_path))
      abs_image_path = settings.BASE_DIR + str(img_path)
      out_dir = osp.dirname(abs_image_path)

      # run the comprehension wrapper
      log_to_terminal(socketid, {'terminal': 'Starting Comprehension job...'})
      response = sender_comprehension(str(abs_image_path), str(expression), str(out_dir), socketid)
    except:
      log_to_terminal(socketid, {'terminal': traceback.print_exc()})
  return render(request, template_name, {'socketid': socketid})


def upload_image_using_url(request):
  if request.method == "POST":
    try:
      socketid = request.POST.get('socketid', None)
      image_url = request.POST.get('src', None)
      demo_type = request.POST.get('type')

      if demo_type == "comprehension":
        dir_type = constants.COMPREHENSION_CONFIG['image_dir']
      elif demo_type == "generation":
        dir_type = constants.GENERATION_CONFIG['image_dir']

      img_name =  os.path.basename(urlparse(image_url).path)
      response = requests.get(image_url, stream=True)

      if response.status_code == 200:
        random_uuid = uuid.uuid1()
        output_dir = os.path.join(dir_type, str(random_uuid))

        if not os.path.exists(output_dir):
          os.makedirs(output_dir)

        img_path = os.path.join(output_dir, str(img_name))

        with open(os.path.join(output_dir, img_name), 'wb+') as f:
          f.write(response.content)

        img_path =  "/" + "/".join(img_path.split('/')[-4:])
         
        return JsonResponse({"file_path": img_path})
      else:
        return HttpResponse("Please Enter the Correct URL.")
    except:
      return HttpResponse("No images matching this url.")
  else:
    return HttpResponse("Invalid request method.")


def file_upload(request):
  if request.method == "POST":
    image = request.FILES['file']
    demo_type = request.POST.get("type")

    if demo_type == "comprehension":
      dir_type = constants.COMPREHENSION_CONFIG['image_dir']
    elif demo_type == "generation":
      dir_type = constants.GENERATION_CONFIG['image_dir']

    random_uuid = uuid.uuid1()
    # handle image upload
    output_dir = os.path.join(dir_type, str(random_uuid))

    if not os.path.exists(output_dir):
      os.makedirs(output_dir)

    img_path = os.path.join(output_dir, str(image))
    handle_uploaded_file(image, img_path)

    img_path =  "/" + "/".join(img_path.split('/')[-4:])
    return JsonResponse({"file_path": img_path})
  else:
    pass

def handle_uploaded_file(f, path):
  with open(path, 'wb+') as destination:
    for chunk in f.chunks():
      destination.write(chunk)


