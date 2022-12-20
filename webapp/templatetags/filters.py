'''
    Generic template filers go into this file.
    Read the comments below to understand in detail.
    or contact niranjan@glynk.com
'''

from django import template
from django.template.defaultfilters import stringfilter
import time
from BeautifulSoup import BeautifulSoup
import re
from urlparse import urlparse
from webapp.models import *
# from webapp.dbplatform import *
from django import template
from django.template.defaultfilters import stringfilter
from django.utils.safestring import mark_safe
from django.utils.html import urlize as urlize_impl
from datetime import date
from django import template
from datetime import date, datetime, timedelta
from colorthief import ColorThief
import sys
from webapp.cache import *
from bs4 import BeautifulSoup
from webapp.controllers.tasks.email_task import send_mail_to_tech

if sys.version_info < (3, 0):
    from urllib2 import urlopen
else:
    from urllib.request import urlopen

import io


register = template.Library()
'''
    Converts the argument to lower case
'''
@register.filter
@stringfilter
def lower(value):
    return value.lower()


'''
    Converts the argument to upper case
'''
@register.filter
@stringfilter
def upper(value):
    return value.upper()


'''
    Converts the argument to camel case
'''
@register.filter
@stringfilter
def camelCase(value):
    return value.title()


'''
    Splits the first given argument with second given argument.
    In case second argument does not exist, it splits with spaces.
'''
@register.filter
@stringfilter
def split(value, args):
    value = str(value)
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(',')]
    if len(arg_list) == 1:
        return value.split(arg_list[0])
    return value.split(arg_list[0])[int(arg_list[1])]


'''
    Replaces the first given argument with second given argument.
    In case second argument does not exist, it replaces with "empty".
    In case second argument is empty, it replaces with space.
'''
@register.filter
@stringfilter
def replace(value, args):
    if args is None:
        return False
    arg_list = [arg.strip() for arg in args.split(',')]
    if len(arg_list) == 1:
        return value.replace(arg_list[0], '')
    if arg_list[1] == '':
        return value.replace(arg_list[0], ' ')
    return value.replace(arg_list[0], arg_list[1])


@register.filter(name='get_item')
def get_item(dictionary, key):
    return dictionary.get(key)


@register.filter(name='convert_time_to_epoch')
def convert_time_to_epoch(template_time):
    d = template_time
    return time.mktime(d.timetuple())


@register.filter(name='convert_dt_to_time')
def convert_dt_to_time(template_time):
    return template_time.date()


@register.filter(name='convert_dt_to_day')
def convert_dt_to_day(template_time):
    diff = datetime.now().replace(tzinfo=None) - template_time.replace(tzinfo=None)

    if diff.seconds < 60:
        return "Just now"
    elif diff.total_seconds() > 60 and diff.total_seconds() / 60 < 60:
        return str(int(diff.total_seconds()) / 60) + "m"
    elif diff.total_seconds() / 60 > 60 and diff.total_seconds() / 3600 < 24:
        return str(int(diff.total_seconds()) / 3600) + "h"
    elif diff.total_seconds() / 3600 > 24 and diff.days < 30:
        return str(diff.days) + "d"
    elif diff.days > 30:
        return template_time


@register.filter(name='convert_dt_to_day_reverse')
def convert_dt_to_day_reverse(template_time):
    diff = template_time.replace(tzinfo=None) - \
                                 datetime.now().replace(tzinfo=None)
    if diff.days == 0:
        return '<span class="expiry-time" style="font-size: 14px;color: #05c1ab;" > today </span>'
    else:
        return ' <span class="expiry-time" > in </span> <span class="expiry-time" style="font-size: 14px;color: #05c1ab;" >' + str(diff.days) + '</span> <span class="expiry-time" >days</span> '


@register.filter(name='get_date')
def get_date(template_datetime):
    return template_datetime.strftime('%d %B')


@register.filter(name='get_time')
def get_time(template_datetime):
    return template_datetime.strftime('%H:%M')


# Old
# urls = re.compile(r"((https?://)+[\w\d:#@%/;$()~_?\+-=\\\.&]*)", re.MULTILINE|re.UNICODE)

# New
urls = re.compile(ur'(?i)\b((?:https?://|www\d{0,3}[.]|[a-z0-9.\-]+[.][a-z]{2,4}/)(?:[^\s()<>]+|\(([^\s()<>]+|(\([^\s()<>]+\)))*\))+(?:\(([^\s()<>]+|(\([^\s()<>]+\)))*\)|[^\s`!()\[\]{};:\'".,<>?\xab\xbb\u201c\u201d\u2018\u2019]))')


@register.filter("urlize_html")
def urlize_html(text, url_max_char_count=40):
    try:
        text = urls.sub(r'<a href="\1" >' + str(r'\1') + '</a>', text)
        soup = BeautifulSoup(text.decode('utf-8', 'ignore'))
        anchors = soup.findAll('a')
    except:
        # In any kind of exception just return the text. We don't want this
        # function to fail as it is being used in all the critical places.
        # Issues here will clearly be visible in the feed/post details/events pages.

        return text

    for a in anchors:
        try:
            org_text = a.contents[0]
            if len(org_text) > url_max_char_count:
                url_text = org_text[:url_max_char_count] + '...'
            else:
                url_text = org_text

            a.string.replaceWith(url_text)
        except Exception as e:
            a.contents.append(text)

    return str(soup)


@register.filter(name='urlize_target_blank')
def urlize_target_blank(text):
    return text.replace('<a ', '<a target="_blank" ')


@register.filter(name='get_image_300')
def get_image_300(image):
    try:
        # return image.get_300_url()
        filename_base, filename_ext = os.path.splitext(str(image))
        return filename_base + '_300' + filename_ext
    except:
        return image


@register.filter("get_image_height_300")
def get_image_height_300(image):
    try:
        return image.height_300
    except:
        return image.height


@register.filter("get_image_width_300")
def get_image_width_300(image):
    try:
        return settings.IMAGE_BASE_WIDTH
    except:
        return 300


@register.filter("get_image_height")
def get_image_height(image):
    try:
        return image.height
    except:
        return 0


@register.filter("get_google_analytics_code")
def get_google_analytics_code(request):
    this_site = get_domain_site(request.get_host())
    try:
        exclude_list = map(
            int, this_site[0].analytics_blacklist_user_ids.split(','))
    except Exception:
        exclude_list = []
    if this_site:
        if request.user.is_authenticated() and request.user.id not in exclude_list:
            return this_site[0].google_analytics_code
        elif not request.user.is_authenticated():
            return this_site[0].google_analytics_code
        else:
            return ""
    else:
        return ""


@register.filter("is_blacklist")
def is_blacklist(user):
    if user.is_authenticated():
        if user.is_superuser or user.email in settings.BLACKLIST_ANALYTICS:
            return True
        else:
            return False
    else:
        return False


@register.filter("get_post_commenter_profile_picture")
def get_post_commenter_profile_picture(comment):
    try:
        return comment.created_by.get_profile_picture()
    except:
        return ''


@register.filter("get_post_image")
def get_post_image(post):
    try:
        return post.get_image()
    except:
        return ''


@register.filter(name='calculate_percent')
def calculate_percent(votes, total):
    try:
        return (float(votes)/float(total))*100
    except ZeroDivisionError:
        return 0


@register.filter(name='get_age')
def get_age(user):
    if not user.birthday:
        return ''

    born = user.birthday
    today = date.today()
    return today.year - born.year - ((today.month, today.day) < (born.month, born.day))


@register.filter(name='get_fb_share_content')
def get_fb_share_content(share_content, type):

    if settings.DEBUG:
        url_prefix = 'http://dev001.glynk.com'
    else:
        url_prefix = 'https://getmilo.app'

    defaults = {
        'IMAGE': 'http://d267x6x6dh1ejh.cloudfront.net/posts/045b430e-7aa5-468e-9f32-597a21aa034a.png',
        'TITLE': 'Milo',
        'DESCRIPTION': 'Know Your Neighbour',
        'URL': url_prefix
    }

    if not share_content:
        return defaults[type]

    if str(ContentType.objects.get_for_model(share_content)) == 'post':
        if type == 'IMAGE':
            if share_content.web_image:
                return share_content.web_image
            else:
                return defaults[type]

        if type == 'TITLE':
            if share_content.title:
                return share_content.title

            if share_content.text:
                return share_content.text

        if type == 'DESCRIPTION':
            community_name = share_content.community.all()[0].name
            return share_content.created_by.first_name + "'s post in " + community_name

        if type == 'URL':
            return url_prefix + '/post/' + share_content.unique_url + '?p_id='+str(share_content.id)

    elif str(ContentType.objects.get_for_model(share_content)) == 'meetup':
        if type == 'IMAGE':
            if share_content.web_image:
                # print "1"
                # print share_content.web_image
                return share_content.web_image
            else:
                # print "2"
                # print defaults[type]
                return defaults[type]

        if type == 'TITLE':
            # print share_content.title
            return share_content.title

        if type == 'DESCRIPTION':
            community_name = share_content.community.all()[0].name
            return share_content.created_by.first_name + "'s meetup in " + community_name

        if type == 'URL':
            # print url_prefix + '/meetup/' + share_content.unique_url + '?m_id='+str(share_content.id)
            return url_prefix + '/meetup/' + share_content.unique_url + '?m_id='+str(share_content.id)

    # If any cases are missed then send out the default.
    return defaults[type]


@register.filter("replace_br_tag_with_newline")
def replace_br_tag_with_newline(value):
    if value:
        return value.replace('<br/>','\n')
    else:
        return ""

@register.filter(name='get_default_order_no')
def get_default_order_no(order_no_list):
    # this method is used to show the position of newly added article /video
    if order_no_list:
        default_no = max(order_no_list)
        return default_no+1
    else:
        return 1

@register.filter(name="upto")
@stringfilter
def upto(value):
    if "year" in value:
        value = value.split('e')[0]
        return "".join(value.split())
    elif "month" in value:
        value = value.split('t')[0]
        return "".join(value.split())
    elif "week" in value:
        value = value.split('e')[0]
        return "".join(value.split())
    elif "day" in value:
        value = value.split('a')[0]
        return "".join(value.split())
    elif "hour" in value:
        value = value.split('o')[0]
        value = value.replace("&nbsp", "")
        return "".join(value.split())
    elif "min" in value:
        value = value.split('i')[0]
        value = value.replace("&nbsp", "")
        return "".join(value.split())
    elif "sec" in value:
        value = value.split('e')[0]
        value = value.replace("&nbsp", "")
        return "".join(value.split())
upto.is_safe = True

@register.filter(name='date_to_string_format')
def date_to_string_format(value, args):
    value = str(value)[:-6] # removing trailing +00:00
    return datetime.strptime(value, args) + timedelta(hours=5, minutes=30)

@register.filter(name='get_nth_string_from_url')
def get_nth_string_from_url(value, index, key="/"):
    value = str(value)
    index = int(index)
    return value.split(key)[index]

@register.filter(name='get_nth_string')
def get_nth_string(value, index, key="|"):
    value = str(value)
    index = int(index)
    return value.split(key)[index].strip()


@register.filter(name='get_loop_index')
def get_loop_index(value):
    return value - 1


@register.filter(name='get_unique_url_from_post_tuple')
def get_unique_url_from_post_tuple(value, index):
    return value[index].unique_url


@register.filter(name='get_image_from_post_tuple')
def get_image_from_post_tuple(value, index):
    return value[index].get_image()


@register.filter(name='get_label_from_post_tuple')
def get_label_from_post_tuple(value, index):

    if value[index].label:
        return value[index].label.strip()
    else:
        if value[index].people_to_meet.all().first().name:
            return value[index].people_to_meet.all().first().name.strip()
        else:
            return ''


@register.filter(name='get_title_from_post_tuple')
def get_title_from_post_tuple(value, index):
    return value[index].title.strip()


@register.filter(name='get_publish_time_from_post_tuple')
def get_publish_time_from_post_tuple(value, index):
    return value[index].published_date


@register.filter(name='get_edited_time_from_post_tuple')
def get_edited_time_from_post_tuple(value, index):
    return value[index].edited_datetime


@register.filter(name='get_id_from_post_tuple')
def get_id_from_post_tuple(value, index):
    return value[index].id


@register.filter(name='get_people_to_meet_from_post_tuple')
def get_people_to_meet_from_post_tuple(tuple, index):
    return tuple[index].people_to_meet.all()[0].url_path


@register.filter(name='generate_short_description')
def generate_short_description(text, char_count):
    if text[:char_count*4]:
        short_desc = text[:char_count * 4]
    elif text[:char_count*3]:
        short_desc = text[:char_count * 3]
    elif text[:char_count*2]:
        short_desc = text[:char_count * 2]
    elif text[:char_count * 1]:
        short_desc = text[:char_count * 1]
    else:
        short_desc = text

    if short_desc:
        short_desc = short_desc.replace("&nbsp;", " ")
        short_desc = ' '.join(short_desc.rsplit(' ')[:-1])

    if short_desc:
        short_desc = short_desc[:-1] + re.sub('[^a-zA-Z0-9 \n\.]', '', short_desc[-1])

    return short_desc


@CacheIt("image")
@register.filter(name='get_dominant_color')
def get_dominant_color(image):
    """ this method is used to get dominant color from the given input image """
    return 333333
    # try:
    #     extension = image.split(".")[-1]
    #     if extension in ['GIF', 'gif']:
    #         return 333333
    #     fd = urlopen(image)
    #     f = io.BytesIO(fd.read())
    #     color_thief = ColorThief(f)
    #     d_color=color_thief.get_color(quality=1)
    #     # converting color code from rgb to hex
    #     d_color_hex='%02x%02x%02x' % d_color
    #     return d_color_hex
    # except:
    #     return 333333

@register.filter(name='get_translated_name')
def get_translated_name(self, language_code):
    lang_ptm = LangPeopleToMeet.objects.filter(people_to_meet=self, language__language_code=language_code).first()
    if lang_ptm:
        return lang_ptm.name
    else:
        return self.name


@register.filter(name='index_divider')
def index_divider(index, value):
    try:
        return int(index / int(value))
    except:
        return False


@register.filter(name='ad_from_zeroth_index')
def ad_from_zeroth_index(ads_arr, index):
    try:
        return ads_arr[int(index) - 1]
    except:
        return False


@register.filter(name='ad_from_second_index')
def ad_from_second_index(ads_arr, index):
    try:
        return ads_arr[int(index) + 1]
    except:
        return False


@register.filter(name='arr_of_text')
def arr_of_text(post_text):
    try:
        if post_text.count('<p>') > 1:
            res_arr = post_text.split("</p>")
            if len(res_arr) > 1:
                from_sec_para = " ".join(res_arr[1:])
                text_arr = [res_arr[0], from_sec_para]
                return text_arr
            elif len(res_arr) == 1:
                return [res_arr[0], " "]

        elif post_text.count('<br>') > 1:
            first_para = post_text.find('<br>')
            from_sec_para = post_text[first_para:]
            from_sec_para = from_sec_para.replace('<br>', '', 2)
            return [post_text[:first_para], from_sec_para]

        elif post_text.count('<br') > 1:
            first_para = post_text.find('<br />')
            from_sec_para = post_text[first_para:]
            from_sec_para = from_sec_para.replace('<br />', '', 2)
            return [post_text[:first_para], from_sec_para]
        else:
            return [post_text, " "]

    except:
        return [post_text, " "]


@register.filter(name='get_indian_num_sys')
def get_indian_num_sys(input):
    try:
        input = str(input)
        Len = len(input)

        # Removing all the separators(, )
        # from the input string
        i = 0
        while (i < Len):
            if (input[i] == ","):
                input = input[:i] + input[i + 1:]
                Len -= 1
                i -= 1
            elif (input[i] == " "):
                input = input[:i] + input[i + 1:]
                Len -= 1
                i -= 1
            else:
                i += 1
        # Reverse the input string
        input = input[::-1]

        # Declaring the output string
        output = ""
        # Process the input string
        for i in range(Len):
            # Add a separator(, ) after the
            # third number
            if (i == 2):
                output += input[i]
                output += ","
            # Then add a separator(, ) after
            # every second number
            elif (i > 2 and i % 2 == 0 and
                  i + 1 < Len):
                output += input[i]
                output += ","
            else:
                output += input[i]
        # Reverse the output string
        output = output[::-1]
        # Return the output string back
        # to the main function
        return output
    except:
        return " "


@register.filter(name='get_arr_item_val')
def get_arr_item_val(arr, index):
    try:
        return arr[int(index)]
    except:
        return False


@register.filter(name='amp_validation')
def amp_validation(value):

    # replacing html tags with necessary amp tags
    value = value.replace("<iframe", "<amp-iframe  sandbox='allow-scripts allow-same-origin'")
    value = value.replace("iframe>", "amp-iframe>")
    value = value.replace('allowfullscreen="true"', "")
    value = value.replace('allowFullScreen="true"', "")
    value = value.replace("script", "amp-script")

    value = value.replace("allow-amp-scripts", "allow-scripts")

    # amp script does not support charset=utf-8 and async so removing it
    value = value.replace("charset", "")
    value = value.replace("utf-8", "")
    value = value.replace("async", "")

    # amp tags doesnot support important in css properties so removing it
    value = value.replace("!important", "")

    try:
        if "<blockquote" in value:
            # checking for twitter tag
            soup = BeautifulSoup(value, 'html.parser')
            twitter_tag = soup.find_all("blockquote", class_="twitter-tweet")

            if twitter_tag:
                # to support tweet in amp we have to use amp twitter tag when we use amp-twitter tag we need tweet id as attribute so getting id from embed link
                # twitter embed link starts with <blockquote so below condition
                value = value.replace("<blockquote","<amp-twitter  width='375' height='472'  layout='responsive'  dummy-data-tweetid> <blockquote")
                value = value.replace("</blockquote>", "</blockquote> </amp-twitter>")

                for i in range(len(twitter_tag)):
                    # getting tweet id from embed code
                    tweet_id = str(twitter_tag[i]).split('/status/')[-1]
                    tweet_id = tweet_id.split('?ref_src')[0]

                    # adding tweet id , without tweet id amp twitter tag will not show preview in UI
                    value = value.replace('dummy-data-tweetid', "data-tweetid="+tweet_id, 1)
    except Exception as e:
        send_mail_to_tech('AMP Validation for twitter tag failed', message=str(e.message))
        pass


    return value


@register.filter
def strip_double_quotes(quoted_string):
    return quoted_string.replace('"', '')

@register.filter
def check_live_tv_url_last_param(url):
    last_value_in_url = url.split("/")[-1]
    if last_value_in_url == "live-tv":
        return True
    else:
        return False

@register.filter
def check_script_tag_in_text(text):
    if "<script" in text:
        return True
    else:
        return False

@register.filter
def check_twitter_tag_in_text(text):
    soup = BeautifulSoup(text, 'html.parser')
    twitter_tag = soup.find_all("blockquote",class_="twitter-tweet")
    if twitter_tag:
        return True
    else:
        return False


@register.filter
def get_webp_format_image(image_path,image_dimension=None):
    try:
        if image_path:
            extension = str(image_path).encode('utf-8').split(".")[-1]
            if extension.lower() == 'gif':
                return 'https://'+settings.AWS_S3_CUSTOM_DOMAIN+ "/" +str(image_path)
            else:
                if image_dimension:
                    image = settings.ARGUS_IMAGE_RESIZE_CDN +'/fit-in/'+ image_dimension +"/"+ str(image_path)
                else:
                    image = settings.ARGUS_IMAGE_RESIZE_CDN + "/" + str(image_path)
                return image
        else:
            return ''
    except:
        return ''
