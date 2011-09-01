import os, os.path as osp

from django.conf import settings
from django.db.models import get_apps

def get_app_resource(app, path):
    apps = get_apps()
    for x in apps:
        app_dir = osp.dirname(x.__file__)
        if app == x.__name__.split('.')[-2]:
            resource_dir = osp.join(app_dir, "resources")
            asset = osp.join(resource_dir, path)
            if osp.exists(asset):
                return asset
            continue