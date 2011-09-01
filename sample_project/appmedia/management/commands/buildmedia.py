from django.core.management.base import LabelCommand, CommandError
from django.db.models import get_apps
import os, os.path as osp
import shutil

class Command(LabelCommand):
    args = ''
    label = 'directory'

    def handle(self, *labels, **options):
        if not labels or len(labels) > 1:
            raise CommandError('Enter one directory name.')

        label = labels[0]
        final_dest = osp.join(os.getcwd(), label)
        if osp.exists(final_dest):
            raise CommandError('Directory already exists')

        os.mkdir(final_dest)
        
        apps = get_apps()
        for x in apps:
            app_dir = osp.dirname(x.__file__)
            module = x.__name__
            app = module.split('.')[-2]

            if app == 'admin': continue

        
            media_dir = osp.join(app_dir, "media", app)
            if not osp.isdir(media_dir):
                media_dir = osp.join(app_dir, "media")
            if osp.exists(media_dir):
                print "copy", media_dir, '->', osp.join(final_dest, app)
                shutil.copytree(media_dir, osp.join(final_dest, app))