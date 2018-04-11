# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.encoding import python_2_unicode_compatible

# Create your models here.
@python_2_unicode_compatible  # only if you need to support Python 2
class ComprehensionJob(models.Model):
  job_id = models.CharField(max_length=1000, blank=True, null=True)
  image = models.CharField(max_length=1000, blank=True, null=True)
  expression = models.CharField(max_length=1000, blank=True, null=True, default="")
  pred_lang_image = models.CharField(max_length=1000, blank=True, null=True)
  pred_comp_image = models.CharField(max_length=1000, blank=True, null=True) 
  pred_segm_image = models.CharField(max_length=1000, blank=True, null=True) 
  createdAt = models.DateTimeField("Time", null=True, auto_now_add=True)

  def __str__(self):
    return self.job_id