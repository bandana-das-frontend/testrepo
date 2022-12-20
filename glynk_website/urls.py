from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from webapp.sitemaps import index as sitemap_index
from webapp.sitemaps import sitemap as sub_siteamp
from webapp.sitemaps import latest_sitemap as latest_sitemap
from webapp.controllers.rss.rss_news_feed import ArgusRSSNewsFeed, ArgusRSSTopicNewsFeed, ArgusRSSTrending
from webapp.sitemaps import StaticSitemap , TopicsSitemap , LatestPostSitemap , LatestVideoSitemap
from django.views.generic import TemplateView
from django.views.generic.base import RedirectView
from django.views.decorators.cache import cache_page

sitemaps = {}
sitemaps["static-urls"] = StaticSitemap
sitemaps["topics-urls"] = TopicsSitemap
sitemaps["latest-post-urls"] = LatestPostSitemap
sitemaps["latest-video-urls"] = LatestPostSitemap


latest_sitemaps = {}
latest_sitemaps["post-urls"] = LatestPostSitemap
latest_sitemaps["video-urls"] = LatestVideoSitemap


urlpatterns = [
    # Examples:
    # url(r'^$', 'glynk_website.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin', include(admin.site.urls)),

    # sitemap.xml url
     url(r'^sitemap\.xml$', sitemap_index, {'sitemaps': sitemaps, 'sitemap_url_name': 'sitemaps','template_name': 'custom_index_sitemap.html'}),
    url(r'^sitemap-latest-(?P<section>.+)\.xml$', latest_sitemap,
        {'sitemaps': latest_sitemaps, 'template_name': 'custom_sitemap.html'}, name='django.contrib.sitemaps.views.sitemap'),
    # 30 days = 2592000 secs
    url(r'^sitemap-(?P<section>.+)\.xml$', cache_page(2592000)(sub_siteamp), {'sitemaps': sitemaps, 'template_name': 'custom_sitemap.html'}, name='sitemaps'),


    # Robots.txt
    # ToDo: make this dynamic
    url(r'^robots\.txt/$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    url(r'^rss/(?P<language_code>.+)/feed/$', ArgusRSSNewsFeed(), name='oria_rss'),
    url(r'^rss/(?P<language_code>.+)/topic/(?P<topic>.+)/', ArgusRSSTopicNewsFeed(), name='topics_rss'),
    url(r'^robots\.txt$', TemplateView.as_view(template_name="robots.txt", content_type='text/plain')),
    url(r'^rss/(?P<language_code>.+)/feed$', ArgusRSSNewsFeed(), name='oria_rss'),
    url(r'^rss/(?P<language_code>.+)/topic/(?P<topic>.+)', ArgusRSSTopicNewsFeed(), name='topics_rss'),
    url(r'^rss/(?P<language_code>.+)/trending/', ArgusRSSTrending(), name='trending_rss'),
    url(r'^rss/(?P<language_code>.+)/trending', ArgusRSSTrending(), name='trending_rss'),

    # amp pages
    url(r'^amp/(?P<language>.+)/latest-news$', 'webapp.controllers.home.home_amp.home_amp'),
    url(r'^amp/article/(?P<unique_url>.+)/$',
        'webapp.controllers.post.google_amp_details.google_amp_post_details_view'),
    url(r'^amp/article/(?P<unique_url>.+)$', 'webapp.controllers.post.google_amp_details.google_amp_post_details_view'),
    url(r'^amp/(?P<language_code>.+)/topics/(?P<topic>.+)$', 'webapp.controllers.topics.topics_amp.topics_amp'),
    url(r'^amp/(?P<language_code>.+)/trending$', 'webapp.controllers.trending.trending_amp.trending_amp'),
    url(r'^redirect_to_amp_ad_link$', 'webapp.controllers.utils.track_ads.redirect_to_amp_ad_link'),

    # home
    url(r'^$', 'webapp.controllers.home.index.home_view'),
    url(r'^(?P<language>.+)/latest-news/$', 'webapp.controllers.home.index.home_view'),
    url(r'^latest-news/$', 'webapp.controllers.home.index.home_view'),
    url(r'^or/trending/$', 'webapp.controllers.trending.trending.trending_view'),
    url(r'^en/trending/$', 'webapp.controllers.trending.trending.trending_view'),
    url(r'^(?P<language>.+)/latest-news$', 'webapp.controllers.home.index.home_view'),
    url(r'^latest-news$', 'webapp.controllers.home.index.home_view'),
    url(r'^or/trending$', 'webapp.controllers.trending.trending.trending_view'),
    url(r'^en/trending$', 'webapp.controllers.trending.trending.trending_view'),

    url(r'^page/home_posts/$', 'webapp.controllers.home.index.pagination_home_posts'),
    url(r'^page/comments/$', 'webapp.controllers.home.index.pagination_comments'),
    url(r'^page/live_tv_home/comments/$', 'webapp.controllers.home.index.pagination_comments'),
    url(r'^page/topic_posts/$', 'webapp.controllers.topics.topic.pagination_topic_posts'),
    url(r'^page/home_posts$', 'webapp.controllers.home.index.pagination_home_posts'),
    url(r'^page/comments$', 'webapp.controllers.home.index.pagination_comments'),
    url(r'^page/live_tv_home/comments$', 'webapp.controllers.home.index.pagination_comments'),
    url(r'^page/topic_posts$', 'webapp.controllers.topics.topic.pagination_topic_posts'),
    url(r'^page/topic_posts_lacation$',
        'webapp.controllers.topics.topics_location_post.pagination_topic_location_posts'),


    # post_details
    url(r'^article/(?P<topic_article>.+)/(?P<unique_url>.+)/$', 'webapp.controllers.post.post_details.post_details_view'),
    url(r'^article/(?P<unique_url>.+)/$', 'webapp.controllers.post.post_details.post_details_view'),
    url(r'^post/page/comments/$', 'webapp.controllers.post.post_details.pagination_comments'),
    url(r'^page/details_posts/$', 'webapp.controllers.post.post_details.pagination_details_posts'),
    url(r'^article/(?P<topic_article>.+)/(?P<unique_url>.+)$', 'webapp.controllers.post.post_details.post_details_view'),
    url(r'^article/(?P<unique_url>.+)$', 'webapp.controllers.post.post_details.post_details_view'),
    url(r'^post/page/comments$', 'webapp.controllers.post.post_details.pagination_comments'),
    url(r'^page/details_posts$', 'webapp.controllers.post.post_details.pagination_details_posts'),

    #profile
    url(r'^profile/(?P<username>.+)/$', 'webapp.controllers.profile.profile.profile_view'),
    url(r'^get_activities/$', 'webapp.controllers.profile.profile.activities'),
    url(r'^get_saved_stories/$', 'webapp.controllers.profile.profile.saved_stories'),
    url(r'^profile/(?P<username>.+)$', 'webapp.controllers.profile.profile.profile_view'),
    url(r'^get_activities$', 'webapp.controllers.profile.profile.activities'),
    url(r'^get_saved_stories$', 'webapp.controllers.profile.profile.saved_stories'),

    #login
    url(r'^send_otp_to_phone_number/$', 'webapp.controllers.account.otp.send_otp_to_phone_number'),
    url(r'^verify_phone_number_otp/$', 'webapp.controllers.account.verify_otp.verify_phone_number_otp'),
    url(r'^verify_email_otp/$', 'webapp.controllers.account.verify_otp.verify_email_otp'),
    url(r'^signup_with_token/$', 'webapp.controllers.account.signup.signup_with_token'),
    url(r'^logout/$', 'webapp.controllers.account.logout.logout_user'),
    url(r'^update_user_name_gender/$', 'webapp.controllers.account.common.update_user.update_name_gender'),
    url(r'^send_otp_to_phone_number$', 'webapp.controllers.account.otp.send_otp_to_phone_number'),
    url(r'^send_otp_to_email$', 'webapp.controllers.account.otp.send_otp_to_email'),
    url(r'^verify_phone_number_otp$', 'webapp.controllers.account.verify_otp.verify_phone_number_otp'),
    url(r'^signup_with_token$', 'webapp.controllers.account.signup.signup_with_token'),
    url(r'^logout$', 'webapp.controllers.account.logout.logout_user'),
    url(r'^update_user_name_gender$', 'webapp.controllers.account.common.update_user.update_name_gender'),

    #live tv
    url(r'^live-tv/$', 'webapp.controllers.live_tv.live_tv.live_tv_view'),
    url(r'^page/live_tv_videos/(?P<topic>.+)/$', 'webapp.controllers.live_tv.live_tv.pagination_live_tv'),
    url(r'^page/live_tv/comments/$', 'webapp.controllers.live_tv.live_tv.pagination_live_tv_comments'),
    url(r'^live-tv/(?P<topic>.+)/$', 'webapp.controllers.topics.topic.video_topic_view'),
    url(r'^live-tv$', 'webapp.controllers.live_tv.live_tv.live_tv_view'),
    url(r'^page/live_tv_videos/(?P<topic>.+)$', 'webapp.controllers.live_tv.live_tv.pagination_live_tv'),
    url(r'^page/live_tv/comments$', 'webapp.controllers.live_tv.live_tv.pagination_live_tv_comments'),
    url(r'^live-tv/(?P<topic>.+)$', 'webapp.controllers.topics.topic.video_topic_view'),

    # url(r'^commando-shakti/$', 'webapp.controllers.live_tv.live_tv.command_shakti_view'),
    # url(r'^commando-shakti$', 'webapp.controllers.live_tv.live_tv.command_shakti_view'),
    # url(r'^page/commando-shakti-videos/$', 'webapp.controllers.live_tv.live_tv.pagination_commando_shakti'),
    # url(r'^page/commando-shakti-videos$', 'webapp.controllers.live_tv.live_tv.pagination_commando_shakti'),

    #topics_page
    url(r'^topics/(?P<topic>.+)/$', 'webapp.controllers.topics.topic.topic_view'),
    url(r'^topics/odisha/(?P<location_string>.+)$',
        'webapp.controllers.topics.topics_location_post.topic_location_view'),
    url(r'^en/topics/odisha/(?P<location_string>.+)$',
        'webapp.controllers.topics.topics_location_post.topic_location_view'),
    url(r'^or/topics/odisha/(?P<location_string>.+)$',
        'webapp.controllers.topics.topics_location_post.topic_location_view'),
    url(r'^en/topics/(?P<topic>.+)/$', 'webapp.controllers.topics.topic.topic_view'),
    url(r'^or/topics/(?P<topic>.+)/$', 'webapp.controllers.topics.topic.topic_view'),
    url(r'^topics/(?P<topic>.+)$', 'webapp.controllers.topics.topic.topic_view'),
    url(r'^en/topics/(?P<topic>.+)$', 'webapp.controllers.topics.topic.topic_view'),
    url(r'^or/topics/(?P<topic>.+)$', 'webapp.controllers.topics.topic.topic_view'),

    #video_details
    url(r'^video/(?P<topic_video>.+)/(?P<unique_url>.+)/$', 'webapp.controllers.live_details.live_details.live_details_view'),
    url(r'^page/live_details/comments/$', 'webapp.controllers.live_details.live_details.pagination_live_details_comments'),
    url(r'^page/details_videos/$', 'webapp.controllers.live_details.live_details.pagination_details_videos'),
    url(r'^video/(?P<topic_video>.+)/(?P<unique_url>.+)$', 'webapp.controllers.live_details.live_details.live_details_view'),
    url(r'^page/live_details/comments$','webapp.controllers.live_details.live_details.pagination_live_details_comments'),
    url(r'^page/details_videos$', 'webapp.controllers.live_details.live_details.pagination_details_videos'),

    #asyncComments
    url(r'^add_comment/$', 'webapp.controllers.comments.comments_action.add_comment'),
    url(r'^add_comment$', 'webapp.controllers.comments.comments_action.add_comment'),


    #meta pages
    url(r'^contact-us/$', 'webapp.controllers.meta_pages.contact_us.contact_us'),
    url(r'^terms-of-use/$', 'webapp.controllers.meta_pages.terms_of_use.terms_of_use'),
    url(r'^privacy-policy/$', 'webapp.controllers.meta_pages.privacy_policy.privacy_policy'),
    url(r'^about-us/$', 'webapp.controllers.meta_pages.about_us.about_us'),
    url(r'^citizennews-terms/$', 'webapp.controllers.meta_pages.citizennews_terms.citizennews_terms'),
    url(r'^citizennews-guidelines/$', 'webapp.controllers.meta_pages.citizennews_guidelines.citizennews_guidelines'),
    url(r'^contact-us$', 'webapp.controllers.meta_pages.contact_us.contact_us'),
    url(r'^terms-of-use$', 'webapp.controllers.meta_pages.terms_of_use.terms_of_use'),
    url(r'^privacy-policy$', 'webapp.controllers.meta_pages.privacy_policy.privacy_policy'),
    url(r'^about-us$', 'webapp.controllers.meta_pages.about_us.about_us'),
    url(r'^citizennews-terms$', 'webapp.controllers.meta_pages.citizennews_terms.citizennews_terms'),
    url(r'^citizennews-guidelines$', 'webapp.controllers.meta_pages.citizennews_guidelines.citizennews_guidelines'),


    # Apple related
    url(r'^apple-app-site-association$', 'webapp.controllers.utils.apple_related.apple_app_site_association'),
    url(r'^\.well-known/apple-app-site-association$', 'webapp.controllers.utils.apple_related.apple_app_site_association'),

    # App download
    url(r'^app/$', 'webapp.controllers.download.download.download'),
    url(r'^download/$', 'webapp.controllers.download.download.download'),
    url(r'^app$', 'webapp.controllers.download.download.download'),
    url(r'^download$', 'webapp.controllers.download.download.download'),


    # Jobs
    url(r'^jobs/$', 'webapp.controllers.jobs.jobs.jobs_view'),
    url(r'^jobs$', 'webapp.controllers.jobs.jobs.jobs_view'),


    # Widgets
    url(r'^widget/$', 'webapp.controllers.widgets.widget.widget'),
    url(r'^widget$', 'webapp.controllers.widgets.widget.widget'),

    # article search pages
    url(r'^search-articles/(?P<search_type>.+)/$', 'webapp.controllers.article_search.article_search.get_search_articles'),
    url(r'^search-articles/(?P<search_type>.+)$', 'webapp.controllers.article_search.article_search.get_search_articles'),
    url(r'^search-articles/$', 'webapp.controllers.article_search.article_search.get_search_articles'),
    url(r'^search-articles$', 'webapp.controllers.article_search.article_search.get_search_articles'),
    url(r'^paginated-search-articles/(?P<search_type>.+)/$','webapp.controllers.article_search.article_search.pagination_search_result'),
    url(r'^paginated-search-articles/(?P<search_type>.+)$', 'webapp.controllers.article_search.article_search.pagination_search_result'),
    url(r'^paginated-search-articles/$', 'webapp.controllers.article_search.article_search.pagination_search_result'),
    url(r'^paginated-search-articles$', 'webapp.controllers.article_search.article_search.pagination_search_result'),

    url(r'^save_browser_notification_token/$', 'webapp.controllers.web_notification.save_token.save_notification_token'),
    url(r'^save_browser_notification_token$', 'webapp.controllers.web_notification.save_token.save_notification_token'),

    # Argus contest pages
    url(r'^get_contest_popup_data/$', 'webapp.controllers.news_contest.news_contest.get_contest_popup_data'),
    url(r'^get_contest_popup_data$', 'webapp.controllers.news_contest.news_contest.get_contest_popup_data'),
    url(r'^contest/(?P<unique_url>.+)/$', 'webapp.controllers.news_contest.news_contest.show_contest_form'),
    url(r'^contest/(?P<unique_url>.+)$', 'webapp.controllers.news_contest.news_contest.show_contest_form'),
    url(r'^raksha-bandhan/$', 'webapp.controllers.news_contest.raksha_bandhan.raksha_bandhan'),
    url(r'^raksha-bandhan$', 'webapp.controllers.news_contest.raksha_bandhan.raksha_bandhan'),

    # Argus newsletter subscription
    url(r'^save_subscriber_email/$', 'webapp.controllers.newsletter.save_subscriber_email.save_subscriber_email'),
    url(r'^save_subscriber_email$', 'webapp.controllers.newsletter.save_subscriber_email.save_subscriber_email'),

    # Argus News Current Compare
    url(r'^compare/$', 'webapp.controllers.news_compare.news_compare.compare_media'),
    url(r'^compare$', 'webapp.controllers.news_compare.news_compare.compare_media'),

    # Argus news shakthi redirection
    url(r'^shakti/$',  RedirectView.as_view(url='https://youtu.be/gXiZC-YTZls', permanent=False)),
    url(r'^shakti', RedirectView.as_view(url='https://youtu.be/gXiZC-YTZls', permanent=False)),

    # Argus news shakthi redirection
    url(r'^odisha-ratna/$',  RedirectView.as_view(url='https://links.argusnews.in/odisha-ratna', permanent=False)),
    url(r'^odisha-ratna', RedirectView.as_view(url='https://links.argusnews.in/odisha-ratna', permanent=False)),


    url(r'^educationnext', RedirectView.as_view(url='https://edunext.argusnews.co/register', permanent=False)),
    url(r'^educationnext/', RedirectView.as_view(url='https://edunext.argusnews.co/register', permanent=False)),

    # Argus News Current Compare
    url(r'^update_ad_click/$', 'webapp.controllers.utils.track_ads.update_ad_clicks'),
    url(r'^update_ad_click$', 'webapp.controllers.utils.track_ads.update_ad_clicks'),
    url(r'^update_ad_clicks_by_id$', 'webapp.controllers.utils.track_ads.update_ad_clicks_by_id'),
    url(r'^update_ad_impressions$', 'webapp.controllers.utils.track_ads.update_ad_impressions_from_ui'),
    url(r'^update_ad_impression_by_id$', 'webapp.controllers.utils.track_ads.update_ad_impression_by_id'),

    # Argus news branding
    url(r'^branding-recokner/$', 'webapp.controllers.branding.branding_recokner.branding_recokner'),
    url(r'^branding-recokner$', 'webapp.controllers.branding.branding_recokner.branding_recokner'),

    # Argus profile
    url(r'^argus-profile/$', 'webapp.controllers.branding.argus_profile.argus_profile'),
    url(r'^argus-profile$', 'webapp.controllers.branding.argus_profile.argus_profile'),


    # Argus iframe pages
    url(r'^chalo-dekhein-apna-desh/$', 'webapp.controllers.iframe_pages.chalo_dekhein_apna_desh.chalo_dekhein_apna_desh'),
    url(r'^chalo-dekhein-apna-desh$', 'webapp.controllers.iframe_pages.chalo_dekhein_apna_desh.chalo_dekhein_apna_desh'),

    #channel number page
    url(r'^channel_number', 'webapp.controllers.channel.channel_number.channel_number'),

    #live update
    url(r'^live-updates/(?P<unique_url>.+)$', 'webapp.controllers.live_update.live_update.live_update'),

    #ads
    url(r'^get_top_ads', 'webapp.controllers.utils.get_ads.get_top_ads'),
    url(r'^get_square_ad/', 'webapp.controllers.utils.get_ads.get_desktop_square_ad'),
    url(r'^get_main_ad', 'webapp.controllers.utils.get_ads.get_main_ad'),


    #live player
    url(r'^live_player/$', 'webapp.controllers.video_player.player.player'),



]

urlpatterns += [
    url(r'^app/static/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.STATIC_ROOT, 'show_indexes': True}),
    url('', include('social.apps.django_app.urls', namespace='social')),
    url(r'^firebase-messaging-sw.js/?$', TemplateView.as_view(template_name='firebase-messaging-sw.js', content_type="text/javascript")),
    url(r'^ahrefs_8d61e72a568053a98b4e79cbf9d510781b66824d8e5341c921d1b240deefaa2a/?$',
        TemplateView.as_view(template_name='ahrefs_8d61e72a568053a98b4e79cbf9d510781b66824d8e5341c921d1b240deefaa2a', content_type="text/html")),
    url(r'^ads.txt/?$', TemplateView.as_view(template_name='ads.txt', content_type="text/plain")),
    url(r'^app-ads.txt/?$', TemplateView.as_view(template_name='app-ads.txt', content_type="text/plain")),
    url(r'^dmjxw7mix8d7awlfj/?$', TemplateView.as_view(template_name='dmjxw7mix8d7awlfj', content_type="text/plain")),

]


# error pages
handler404 = 'webapp.controllers.errors.error_404.handle404'
handler500 = 'webapp.controllers.errors.error_500.handle500'
