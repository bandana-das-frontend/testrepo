#!/usr/bin/python
# -*- coding: utf-8 -*-
from functools import wraps
from django.contrib.sites.shortcuts import get_current_site
from django.core import urlresolvers
from django.contrib.sitemaps import Sitemap, GenericSitemap
from webapp.models import Post, Community, LiveNews, PeopleToMeet, CommunityConfigurations, LangPeopleToMeet
from datetime import datetime, date, timedelta
from django.core.paginator import EmptyPage, PageNotAnInteger
from django.http import Http404
from django.template.response import TemplateResponse
from django.utils import six
from django.utils.http import http_date
from calendar import timegm


class StaticSitemap(Sitemap):
    changefreq = "hourly"
    priority = 1

    def items(self):
        """
            This method fetches all the static URLs of the site for SEO
        """
        return ['', 'or/latest-news', 'en/latest-news', 'live-tv', 'or/trending', 'en/trending', 'about-us',
                'privacy-policy', 'terms-of-use', 'contact-us', 'jobs']

    def location(self, item):
        """
            This method sets the <loc> tag
        """
        static_url = "/" + str(item)
        return static_url


class TopicsSitemap(Sitemap):
    changefreq = "daily"
    priority = 1
    def items(self):
        community = Community.objects.filter(unique_code="THEARGUS").first()

        community_languages=['LANGUAGE_OR', 'LANGUAGE_EN']
        people_to_meet_list = []

        for language in community_languages:

            community_config_view = CommunityConfigurations.objects.filter(community=community, filter_parameter=language).first()
            community_admin_interests_ids = community_config_view.get_community_admin_interests()

            for people_to_meet_id in community_admin_interests_ids:
                people_to_meet = PeopleToMeet.objects.filter(pk=people_to_meet_id).first()
                if people_to_meet:
                    if language == 'LANGUAGE_OR':
                        people_to_meet_list.append("/or/topics/"+str(people_to_meet.url_path))
                    else:
                        people_to_meet_list.append("/en/topics/"+str(people_to_meet.url_path))
        return people_to_meet_list

    def location(self, item):
        """
            This method sets the <loc> tag
        """
        static_url = str(item)
        return static_url


class LatestPostSitemap(Sitemap):
    changefreq = "daily"
    priority = 1
    # post_start_date = date(2019, 1, 1)
    # video_start_date = date(2020, 7, 1)

    def items(self):
        posts=[]
        today_date = datetime.utcnow().date()
        post_start_date = today_date - timedelta(hours=48)
        post_end_date = today_date + timedelta(days=1)

        community = Community.objects.filter(unique_code="THEARGUS").first()
        # for start_date_obj in daterange(post_start_date, post_end_date):
        start_date_str = post_start_date.strftime('%Y-%m-%d')
        end_date_str = post_end_date.strftime('%Y-%m-%d')
        latest_posts = Post.objects.filter(community=community, is_story=False, is_hidden=False, edited_datetime__range=[start_date_str, end_date_str]).order_by(
            "-edited_datetime")
        for post in latest_posts:
            if post:
                posts.append(str(post.get_absolute_url().encode('utf-8')))

        return posts

    def location(self, item):
        """
            This method sets the <loc> tag
        """
        static_url = str(item)
        return static_url


class LatestVideoSitemap(Sitemap):
    changefreq = "daily"
    priority = 1

    def items(self):
        videos = []
        today_date = datetime.utcnow().date()
        video_start_date = today_date - timedelta(hours=48)
        video_end_date = today_date + timedelta(days=1)

        community = Community.objects.filter(unique_code="THEARGUS").first()
        # for start_date_obj in daterange(post_start_date, post_end_date):
        start_date_str = video_start_date.strftime('%Y-%m-%d')
        end_date_str = video_end_date.strftime('%Y-%m-%d')
        latest_videos = LiveNews.objects.filter(community=community, is_hidden=False, edited_datetime__range=[start_date_str, end_date_str]).order_by(
            "-edited_datetime")
        for video in latest_videos:
            if video:
                videos.append(str(video.get_absolute_url().encode('utf-8')))
        return videos

    def location(self, item):
        """
            This method sets the <loc> tag
        """
        static_url = str(item)
        return static_url


def daterange(start_date, end_date):
    for n in range(int((end_date - start_date).days) + 1):
        yield start_date + timedelta(n)


# Function to get the sitemap dictionary with queryset as value and datestring as key
def get_post_video_sitemap():
    post_start_date = date(2019, 1, 1)
    video_start_date = date(2020, 7, 1)
    end_date = datetime.utcnow().date()
    end_date = end_date + timedelta(days=1)
    sitemaps = {}
    community = Community.objects.filter(unique_code="THEARGUS").first()

    # Loop through the unique date generated from get_dates_str function, add sitemap item to "sitemaps" dictionary
    for start_date_obj in daterange(post_start_date, end_date):
        start_date_str = start_date_obj.strftime('%Y-%m-%d')
        end_date_str = (start_date_obj + timedelta(days=1)).strftime('%Y-%m-%d')
        curr_day_posts = Post.objects.filter(community=community, is_story=False, is_hidden=False, edited_datetime__range=[start_date_str, end_date_str]).order_by("-edited_datetime")
        sitemaps[str(start_date_str) + "-posts"] = GenericSitemap({'queryset': curr_day_posts, 'date_field': 'edited_datetime'}, 0.9, "hourly")

    for start_date_obj in daterange(video_start_date, end_date):
        start_date_str = start_date_obj.strftime('%Y-%m-%d')
        end_date_str = (start_date_obj + timedelta(days=1)).strftime('%Y-%m-%d')
        curr_day_videos = LiveNews.objects.filter(community=community, is_hidden=False, edited_datetime__range=[start_date_str, end_date_str]).order_by("-edited_datetime")
        sitemaps[str(start_date_str) + "-videos"] = GenericSitemap({'queryset': curr_day_videos, 'date_field': "edited_datetime"}, 0.5, "hourly")
    return sitemaps


# Decorator used to avoid getting index sitemap getting indexed OR to avoid showing a cached link in search results
def x_robots_tag(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        response = func(request, *args, **kwargs)
        response['X-Robots-Tag'] = 'noindex, noodp, noarchive'
        return response
    return inner


# Index function which render index sitemap template with corresponding sitemap URLs and last edited datetime
@x_robots_tag
def index(request, sitemaps,
          template_name='sitemap_index.xml', content_type='application/xml',
          sitemap_url_name='django.contrib.sitemaps.views.sitemap'):
    req_protocol = request.scheme
    req_site = get_current_site(request)
    post_video_sitemaps = get_post_video_sitemap()
    sitemaps.update(post_video_sitemaps)
    sites = []
    # Loop through the sorted dictionary based on key of the dictionary (section)
    # Using the sitemaps query get the edited datetime and append it to the edited_dates list.
    # Generate sitemap url from the section name and append the url to sites list

    for section, site in sorted(sitemaps.items(), reverse=True):
        if callable(site):
            site = site()
        protocol = req_protocol if site.protocol is None else site.protocol
        sitemap_url = urlresolvers.reverse(
            sitemap_url_name, kwargs={'section': section})
        absolute_url = '%s://%s%s' % (protocol, req_site.domain, sitemap_url)
        sites.append(absolute_url)

    return TemplateResponse(request, template_name, {'sites': sites}, content_type=content_type)


@x_robots_tag
def sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml'):

    req_protocol = request.scheme
    req_site = get_current_site(request)
    post_video_sitemaps = get_post_video_sitemap()
    sitemaps.update(post_video_sitemaps)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = list(six.itervalues(sitemaps))
    page = request.GET.get("p", 1)

    urls = []
    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    response = TemplateResponse(request, template_name, {'urlset': urls},
                                content_type=content_type)
    if hasattr(site, 'latest_lastmod'):
        # if latest_lastmod is defined for site, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        lastmod = site.latest_lastmod
        response['Last-Modified'] = http_date(
            timegm(
                lastmod.utctimetuple() if isinstance(lastmod, datetime)
                else lastmod.timetuple()
            )
        )
    return response



@x_robots_tag
def latest_sitemap(request, sitemaps, section=None,
            template_name='sitemap.xml', content_type='application/xml'):

    req_protocol = request.scheme
    req_site = get_current_site(request)

    if section is not None:
        if section not in sitemaps:
            raise Http404("No sitemap available for section: %r" % section)
        maps = [sitemaps[section]]
    else:
        maps = list(six.itervalues(sitemaps))
    page = request.GET.get("p", 1)

    urls = []
    for site in maps:
        try:
            if callable(site):
                site = site()
            urls.extend(site.get_urls(page=page, site=req_site,
                                      protocol=req_protocol))
        except EmptyPage:
            raise Http404("Page %s empty" % page)
        except PageNotAnInteger:
            raise Http404("No page '%s'" % page)
    response = TemplateResponse(request, template_name, {'urlset': urls},
                                content_type=content_type)
    if hasattr(site, 'latest_lastmod'):
        # if latest_lastmod is defined for site, set header so as
        # ConditionalGetMiddleware is able to send 304 NOT MODIFIED
        lastmod = site.latest_lastmod
        response['Last-Modified'] = http_date(
            timegm(
                lastmod.utctimetuple() if isinstance(lastmod, datetime)
                else lastmod.timetuple()
            )
        )
    return response