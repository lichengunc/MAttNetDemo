from __future__ import absolute_import
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'demo.settings')

import django
django.setup()
from django.conf import settings

import pika
import time
import yaml
import json
import traceback
import re

import torch
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import argparse
import os.path as osp
import numpy as np
from scipy.misc import imread, imresize, imsave
import sys
sys.path.insert(0, 'MattNet2s/tools')
from mattnet import MAttNet

from refer.utils import log_to_terminal
from refer.models import ComprehensionJob
import refer.constants as constants

# Set up MattNet, has to put this before "import pika"
parser = argparse.ArgumentParser()
args = parser.parse_args('')
args.dataset = constants.COMPREHENSION_CONFIG['dataset']
args.splitBy = constants.COMPREHENSION_CONFIG['splitBy']
args.model_id = constants.COMPREHENSION_CONFIG['model_id']
mattnet = MAttNet(args)


# forward model
def model_forward(image_path, expression, out_dir):

  # read image
  tic = time.time()
  py_read_img = imread(image_path)
  if max(py_read_img.shape[0], py_read_img.shape[1]) > 1000:
    # if too large, make it small!
    ratio = 1000./max(py_read_img.shape[0], py_read_img.shape[1])
    py_read_img = imresize(py_read_img, ratio)
    imsave(image_path, py_read_img)
  im_time = time.time()-tic

  # forward
  tic = time.time()
  img_data = mattnet.forward_image(image_path, nms_thresh=0.3, conf_thresh=0.50, py_read_img=py_read_img)
  mrcn_time = time.time()-tic

  tic = time.time()
  entry = mattnet.comprehend(img_data, expression)
  matt_time = time.time()-tic

  # tokens to chars, without special chars
  expr = ' '.join(entry['tokens'])
  chars = re.sub('[^A-Za-z0-9]+', '', expr)

  # save images
  tic = time.time()
  ex = image_path.rfind('.')
  pred_lang_image_path = image_path[:ex]+'_lang_'+chars+'.jpg'
  pred_comp_image_path = image_path[:ex]+'_comp_'+chars+'.jpg'
  pred_segm_image_path = image_path[:ex]+'_segm_'+chars+'.jpg'
  mattnet.plot_everything(entry, image_path, 
                         pred_lang_image_path, 
                         pred_comp_image_path, 
                         pred_segm_image_path,
                         py_read_img=py_read_img)
  plot_time = time.time()-tic
  print('imread took %.2fs, mrcn took %.2fs, comprehension took %.2fs, plot took %.2fs.' % (im_time, mrcn_time, matt_time, plot_time))

  # add to result
  result = {}
  result['pred_lang_image'] = pred_lang_image_path.replace(settings.BASE_DIR, '')
  result['pred_comp_image'] = pred_comp_image_path.replace(settings.BASE_DIR, '')
  result['pred_segm_image'] = pred_segm_image_path.replace(settings.BASE_DIR, '')
  return result



# Close the database connection in order to make sure that MYSQL Timeout doesn't occur
django.db.close_old_connections()

# Receiver
connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
channel = connection.channel()
channel.queue_declare(queue='comprehension_task_queue', durable=True)
print(' [*] Waiting for messages. To exit press CTRL+C')

def callback(ch, method, properties, body):
  try:
    print(' [x] Received %r' % body)  # body is {'image_path', 'expression', 'out_dir', 'socketid'}
    body = yaml.safe_load(body) # using yaml instead of json.loads since that unicodes the string in value

    result = model_forward(body['image_path'], body['expression'], body['out_dir'])

    ComprehensionJob.objects.create(job_id=body['socketid'],
                                    image=body['image_path'].replace(settings.BASE_DIR, ''),
                                    expression=body['expression'],
                                    pred_lang_image=result['pred_lang_image'],
                                    pred_comp_image=result['pred_comp_image'],
                                    pred_segm_image=result['pred_segm_image'],
                                    )

    # Close the database connection in order to make sure that MYSQL Timeout doesn't occur
    django.db.close_old_connections()

    log_to_terminal(body['socketid'], {'result': json.dumps(result)})
    log_to_terminal(body['socketid'], {'terminal': 'Receiver: Completed the comprehension job.'})
    print('Worker: Completed the comprehension job.')

    ch.basic_ack(delivery_tag = method.delivery_tag)
  
  except Exception, err:
    log_to_terminal(body['socketid'], {"terminal": json.dumps({"Traceback": str(traceback.print_exc())})})


channel.basic_consume(callback,
                      queue='comprehension_task_queue')

channel.start_consuming()










