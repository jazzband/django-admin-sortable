import os, os.path as osp

from django.conf import settings
from django.views.static import serve as django_serve
from django.views.decorators.cache import cache_page
from django.db.models import get_apps
from django.core.cache import cache
from django.http import Http404, HttpResponse

def serve(request, app, path, show_indexes=True):
    if request.method == 'GET':
        apps = get_apps()
        for x in apps:
            app_dir = osp.dirname(x.__file__)
            module = x.__name__
            if app == module.split('.')[-2]: #we get the models module here
                if app_dir.endswith("models"):
                    # this can happen only in case when models are an directory
                    app_dir = osp.split(app_dir)[0]
                media_dir = osp.join(app_dir, "media", app)
                if not osp.isdir(media_dir):
                    media_dir = osp.join(app_dir, "media")
                asset = osp.join(media_dir, path)
                if osp.exists(asset):
                    return django_serve(request, path, document_root=media_dir, show_indexes=show_indexes)
                #continue
        return django_serve(request, app+"/"+path, document_root=settings.MEDIA_ROOT, show_indexes=show_indexes)
    elif request.method == 'POST':
        data = request.POST.get("data", "")
        apps = get_apps()
        for x in apps:
            app_dir = osp.dirname(x.__file__)
            module = x.__name__
            if app == module.split('.')[-2]: #we get the models module here
                media_dir = osp.join(app_dir, "media")
                asset = osp.join(media_dir, path)
                if osp.exists(asset):
                    f = file(asset, 'w')
                    for line in data.split('\n'):
                        line.strip()
                        line = line[:-1]
                        if line:
                            selector, datap = line.split('{')
                            print >>f, selector, '{'
                            datap.strip()
                            lines = datap.split(';')
                            if lines:
                                print >>f, "    "+";\n    ".join(lines)
                            print >>f, '}\n'
                    f.close()

                    return django_serve(request, path, document_root=media_dir, show_indexes=show_indexes)
                continue


def get_file(path):
    app = path.split('/')[2]
    path = "/".join(path.split('/')[3:])
    apps = get_apps()
    for x in apps:
        app_dir = osp.dirname(x.__file__)
        module = x.__name__
        if app == module.split('.')[-2]: #we get the models module here
            media_dir = osp.join(app_dir, "media")
            asset = osp.join(media_dir, path)
            if osp.exists(asset):
                print osp.join(media_dir, path)
                return osp.join(media_dir, path)
    return osp.join(settings.MEDIA_ROOT, app+"/"+path)

@cache_page(24*60*60)
def serve_cached_asset(request, asset):
    name, ext = asset.split('.')
    files = cache.get(name)
    if ext == 'js':
        response = HttpResponse("\n".join([file(get_file(path)).read() for path in files]), mimetype="text/javascript")
        return response
    elif ext == 'css':
        response = HttpResponse("\n".join([file(get_file(path)).read() for path in files]), mimetype="text/css")
        return response
    raise Http404()