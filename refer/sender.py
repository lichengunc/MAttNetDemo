from django.conf import settings
from refer.utils import log_to_terminal

import os
import pika
import sys
import json

def sender_comprehension(image_path, expression, out_dir, socketid):

  connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
  channel = connection.channel()
  channel.queue_declare(queue='comprehension_task_queue', durable=True)

  message = {'image_path': image_path, 
             'expression': expression,
             'out_dir': out_dir,
             'socketid': socketid,
             }
  log_to_terminal(socketid, {'terminal': 'Sender: publishing job to Queue.'})
  channel.basic_publish(exchange='',
                        routing_key='comprehension_task_queue',
                        body=json.dumps(message),
                        properties=pika.BasicProperties(delivery_mode = 2), # make message persistent
                        )

  print(' [x] Sent %r' % message)
  log_to_terminal(socketid, {'terminal': 'Sender: published job successfully.'})
  connection.close()
