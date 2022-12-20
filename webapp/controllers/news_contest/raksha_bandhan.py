from django.core.files.storage import default_storage
from django.views.decorators.csrf import csrf_exempt
import datetime
from django.utils.encoding import smart_str
import uuid
from webapp.models import *
from webapp.controllers.common.template_render import render_to_template
import os
import json

PASSWORD = "62043777!"

# View to add and edit contest popup
@csrf_exempt
def raksha_bandhan(request):
    base_path = 'posts/'
    community = Community.objects.filter(unique_code="THEARGUS").first()
    if request.method == "GET":
        return render_to_template('contest/raksha_bandhan.html', {"community": community}, request)

    if request.method == "POST":
        phone_number = str(request.POST["phone_number"].encode("utf8"))
        name = str(request.POST["user_name"].encode("utf8"))
        sibling_name = str(request.POST["sibling_name"].encode("utf8"))
        message = str(request.POST["message"].encode("utf8"))
        address = str(request.POST["address"].encode("utf8"))
        email = phone_number + '@' + community.email_alias

        user = None
        user = MyUser.objects.filter(community=community, email=email, is_guest_user=True).first()
        if not user:
            user = create_guest_user(community, name, email, phone_number)

        title = "Raksha Bandhan : " + name
        post_text = "Brother/Sister Name : " + sibling_name +'<br> Message : '+ message
        post_type = 'RECOMMEND'

        post = Post.objects.create(created_by=user,
                                   title=title,
                                   locations = address,
                                   label='Raksha Bandhan',
                                   text=post_text,
                                   incident_datetime=datetime.now(),
                                   is_usercreated=True,
                                   type=post_type,
                                   unique_url=get_unique_url(title, post_text),
                                   is_hidden=True,)

        if 'media_url' in request.POST:
            file_type = ''
            media_url = request.POST['media_url']
            root, extention = os.path.splitext(media_url)
            if str(extention).lower() in [".gif", ".jpg", ".jpeg", ".png"]:
                post_media = PostMedia()
                post_media.image = remove_aws_base_url(media_url)
                post_media.type = POST_MEDIA_TYPES.IMAGE
                post_media.post = post
                post_media.save()
            elif str(extention).lower() in [".mp4", ".m4v", ".avi", ".mpg"]:
                post_media = PostMedia()

                file_name = media_url.split('/')[-1]
                # Store the s3 bucket folder path of the file, videos are stored in 'posts/' folder
                post_media.video = 'posts/' + file_name

                post_media.type = POST_MEDIA_TYPES.VIDEO
                post_media.post = post
                post_media.save()
                generate_video_thumbnail(post_media.id)

        people_to_meet = PeopleToMeet.objects.get(unique_id='THEARGUS_Citizen_News')

        if people_to_meet:
            post.people_to_meet.add(people_to_meet)

        post.layout_type = POST_LAYOUT_TYPE().NEWS
        post.submission_status = SUBMISSION_STATUS.SUBMITTED
        post.community.add(community)
        post.save()
        return render_to_template('contest/event_submit_success.html', {"community": community}, request)

    return render_to_template('contest/raksha_bandhan.html', {community: community}, request)


# Create a guest user for web notification using fingerprint
def create_guest_user(community, name, email, phone_number):
    first_name = name
    last_name = ''
    user = MyUser.objects.create(username=email,
                                 email=email,
                                 first_name=first_name,
                                 last_name=last_name,
                                 phone_number=phone_number)
    user.set_password(PASSWORD)
    user.last_login = datetime.now()
    user.auth_type = USER_AUTH_TYPES.GUEST_LOGIN
    user.is_guest_user = True
    user.is_onboarded = True
    user.save()
    user = MyUser.objects.get(pk=user.id)
    user.community.add(community)
    return user


def get_unique_url(post_title, post_text='', preview_text='', post=None):

    if post_title.strip():
        text = post_title
    elif post_text.strip():
        text = post_text
    elif preview_text.strip():
        text = preview_text
    else:
        text = uuid.uuid4()

    url_count = 0

    title = smart_str(text)
    title = re.sub(r'[^\x00-\x7F]+', '', title)
    title.replace("\r", " ").replace("\n", " ").replace("\t", '').replace("\"", "")
    safe_str = title[:70].encode('ascii', 'ignore')
    urnique_url_title = safe_str

    while 1:
        url = re.sub('[^0-9a-zA-Z]+', '-', str(urnique_url_title))

        if url_count > 0:
            url += '-' + str(url_count)

        post_exists = Post.objects.filter(unique_url=url).first()

        if post_exists:
            # Don't increase the url_count if the existing post is the same post.
            if not post or post.id != post_exists.id:
                url_count += 1
                continue
        else:
            return url


def remove_aws_base_url(media_url):
    # media_url will have https/http, cdn domain and file path
    # we are removing aws cdn path from the media url
    S3_BASE_URL = 'https://s3.ap-southeast-1.amazonaws.com/poll.media/'
    if S3_BASE_URL in media_url:
        media_url_file = media_url.replace(S3_BASE_URL, '')
        return media_url_file
    return media_url


def generate_video_thumbnail(post_media_id):
    import subprocess
    media = PostMedia.objects.filter(pk=post_media_id).first()
    # if not media:
    #     return
    # if media.video:
    #     return
    video_url = media.get_video()
    file_path = media.video.name
    filename_base, filename_ext = splitext(file_path)
    thumbnail_filename = filename_base + '.jpeg'
    thumbnail_file = 'www/static/video_thumbnails/' + thumbnail_filename
    cmd = "ffmpeg -ss 00:0:01 -i " + video_url + " -frames:v 1 " + thumbnail_file
    subprocess.call(cmd, shell=True)
    with open(thumbnail_file, 'r') as thumbnail:
        file = default_storage.open(thumbnail_filename, 'w')
        file.write(thumbnail.read())
        file.close()
        media.image = thumbnail_filename
        media.save()
    import os
    os.remove(thumbnail_file)
