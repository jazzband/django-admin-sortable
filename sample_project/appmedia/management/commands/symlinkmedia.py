from django.core.management.base import NoArgsCommand
from django.db.models import get_apps


class Command(NoArgsCommand):
    help = """
Removes all symlinks in MEDIA_ROOT and then scans all installed applications for a media folder to symlink to MEDIA_ROOT.

If installed app has a media folder, it first attempts to symlink the contents
    ie:   app/media/app_name -> MEDIA_ROOT/app_name
    
If the symlink name already exists, it assumes the media directory is not subfoldered and attempts:
    ie:  app/media -> MEDIA_ROOT/app_name"""
    
    def handle_noargs(self, **options):
        from django.conf import settings
        import os
        
        media_path = settings.MEDIA_ROOT
        print "creating symlinks for app media under %s" % media_path
        for d in os.listdir(media_path):
            path = os.path.join(media_path, d)
            if os.path.islink(path):
                os.remove(os.path.join(path))
                print " - removed %s" % path
        
        apps = get_apps()
        for app in apps:
            
            app_file = app.__file__
            if os.path.splitext(app_file)[0].endswith('/__init__'):
                # models are an folder, go one level up
                app_file = os.path.dirname(app_file)
            
            app_path = os.path.dirname(app_file)
            if 'media' in os.listdir(app_path) and os.path.isdir(os.path.join(app_path,'media')):
                module = app.__name__
                app_name = module.split('.')[-2]
                app_media = os.path.join(app_path, "media", app_name)
                if not os.path.isdir(app_media):
                    app_media = os.path.join(app_path, "media")                
                try:
                    os.symlink(app_media, os.path.join(media_path, app_name))
                    print " + added %s as %s" % (os.path.join(app_media), os.path.join(media_path, app_name))
                except OSError, e:
                    if e.errno == 17:
                        pass
                        print " o skipping %s" % app_media
                    else:
                        raise
#                    try:
#                        os.symlink(app_media, os.path.join(media_path,app.split('.')[-1]))
#                        print " + added %s as %s" % (app_media, os.path.join(media_path, app.split('.')[-1]))
