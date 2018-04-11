from django.conf import settings
import os
import os.path as osp

COCO_IMAGES_PATH = os.path.join(settings.MEDIA_ROOT, 'coco', 'val2014')


COMPREHENSION_CONFIG = {
  'image_dir': osp.join(settings.BASE_DIR, 'media', 'comprehension'),
  'splitBy': 'unc',
  'dataset': 'refcombined+genome',
  'model_id': 'mrcn_cmr_with_st_ratio0.4_subatt800_jemb800_decay14000',
}

GENERATION_CONFIG = {
  'image_dir': osp.join(settings.BASE_DIR, 'media', 'generation')
}
