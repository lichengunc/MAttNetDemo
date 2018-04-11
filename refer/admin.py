# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from refer.models import ComprehensionJob

# Register your models here.
class ComprehensionJobAdmin(admin.ModelAdmin):
  list_display = ('job_id', 'image_url', 'expression', 
                  'pred_segm_image_url', 'pred_lang_image_url', 'createdAt')

  def image_url(self, obj):
    return '<img src="%s" alt="%s" height="150px">' % (obj.image, obj.image)
  image_url.allow_tags = True

  def pred_segm_image_url(self, obj):
    return '<img src="%s" alt="%s" height="150px">' % (obj.pred_segm_image, obj.pred_segm_image)
  pred_segm_image_url.allow_tags = True

  def pred_lang_image_url(self, obj):
    return '<img src="%s" alt="%s" height="150px">' % (obj.pred_lang_image, obj.pred_lang_image)
  pred_lang_image_url.allow_tags = True


admin.site.register(ComprehensionJob, ComprehensionJobAdmin)
# admin.site.register()


