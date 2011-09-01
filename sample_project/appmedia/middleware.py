from md5 import md5

from django.conf import settings
from django.core.cache import cache
from django.core.urlresolvers import reverse

from appmedia.BeautifulSoup import BeautifulSoup, Tag

boundary = '*#*'

class ReplaceAssets(object):
    def process_response(self, request, response):
        if response['Content-Type'].startswith('text/html') and settings.CACHE_BACKEND not in ['', None, 'dummy:///']:
            soup = BeautifulSoup(response.content)
            head = soup.head

            #[script.extract() for script in head.findAll(lambda x: x.name == 'script' and 'src' in dict(x.attrs) and x['src'].startswith(settings.MEDIA_URL) )]
            #[css.extract() for css in head.findAll(lambda x: x.name == 'link' and 'href' in dict(x.attrs) and x['href'].startswith(settings.MEDIA_URL) )]
            
            scripts = head.findAll(lambda x: x.name == 'script' and 'src' in dict(x.attrs) and x['src'].startswith(settings.MEDIA_URL) )
            css = head.findAll(lambda x: x.name == 'link' and 'href' in dict(x.attrs) and x['href'].startswith(settings.MEDIA_URL) )

            script_sources = [x['src'] for x in scripts]
            new_script = md5(boundary.join(script_sources)).hexdigest()
            cache.set(new_script, script_sources)
            [x.extract() for x in scripts]

            css_sources = [x['href'] for x in css]
            new_css = md5(boundary.join(css_sources)).hexdigest()
            cache.set(new_css, css_sources)
            [x.extract() for x in css]

            tag = Tag(soup, "script", [("type", "text/javascript"), ("src", reverse('cached_asset', kwargs={'asset':new_script+".js"}) )])
            head.insert(0, tag)
            tag = Tag(soup, "link", [("type", "text/css"), ("href", reverse('cached_asset', kwargs={'asset':new_css+".css"})), ('rel', 'stylesheet')])
            head.insert(0, tag)
            response.content = soup.prettify()
        return response