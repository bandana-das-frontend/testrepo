from webapp.models import *


class CommunityObjectMiddleware(object):
    def process_request(sefl, request):
        request.community = Community.objects.filter(unique_code='THEARGUS').first()
        request.cache_time = 600
        if request.session.get('lang_code') is None:
            request.session['lang_code'] = 'or'

        http_host = None
        if 'HTTP_HOST' in request.META:
            http_host = request.META['HTTP_HOST']

        if request.META['HTTP_HOST'] in ['127.0.0.1:8000', 'argustv-dev.glynk.com', 'dev001-webapp.glynk.com',
                                         'dev001-webapp1.glynk.com', 'dev001-webapp3.glynk.com', 'dev001-webapp4.glynk.com',
                                         'dev001-webapp5.glynk.com', 'localhost:8000',
                                         'beta.argusnews.in', 'argusnews.in', 'qa-argus.glynk.com',
                                         'www.theargus.in', 'theargus.in', 'qa-argus.getmilo.app']:
            request.community = Community.objects.filter(unique_code='THEARGUS').first()
            # Adding cache_time attribute with a value of 10 min (60*10) to request object
            request.cache_time = 600

            # handling language from url
            try:
                url_path_list = request.get_full_path().split('/')
                if 'en' in url_path_list:
                    request.session['lang_code'] = 'en'
                elif 'or' in url_path_list:
                    request.session['lang_code'] = 'or'
            except Exception as e:
                pass

            if request.session.get('lang_code') is None:
                request.session['lang_code'] = 'or'

        elif request.META['HTTP_HOST'] in ['dev001-webapp2.glynk.com', 'newdoor-dev.glynk.com']:
            request.community = Community.objects.filter(unique_code='NEWDOOR').first()
            if request.session.get('lang_code') is None:
                request.session['lang_code'] = 'en'

        if http_host == 'en.argusnews.in':
            request.session['lang_code'] = 'en'