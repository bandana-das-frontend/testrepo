from django.conf import settings
from django.http import HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from webapp.controllers.common.template_render import render_to_template
from django.template import RequestContext
from webapp.models import *
from webapp.controllers.helpers.pagination import *
from django.http import HttpResponse
import datetime


@csrf_exempt
def add_comment(request):
    if not request.user.is_authenticated():
        return HttpResponseRedirect('/')

    user = request.user
    post_id = str(request.POST['post_id'])

    # Todo: Change the logic to get community later
    community = request.community

    user_info = MyUser.objects.get(phone_number=user, community=community)
    text = str(request.POST['comment_text'])
    created_by = user_info

    if request.POST['comment_type'] == "live": 
        live = LiveNews.objects.get(id=post_id)
        program_comment = ProgramComment()

        program_comment.created_by = created_by
        program_comment.program = live
        program_comment.text = text
        program_comment.created = datetime.datetime.now()
        program_comment.modified = datetime.datetime.now()
        program_comment.is_hidden = False
        program_comment.is_video = False

        program_comment.save()
        program_comment.community.add(community)

    elif request.POST['comment_type'] == "post":
        post = Post.objects.get(id=post_id)
        post_comment = PostComment()

        post_comment.created_by = created_by
        post_comment.post = post
        post_comment.text = text
        post_comment.created = datetime.datetime.now()
        post_comment.modified = datetime.datetime.now()
        post_comment.is_hidden = False
        post_comment.is_video = False

        post_comment.save()
        post_comment.community.add(community)


    return HttpResponse('200')