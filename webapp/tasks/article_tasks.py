from celery.task import task

from webapp.models import *


@task(name='fetch_college_image')
def update_article_views(post_id):
    post = Post.objects.get(pk=post_id)
    post.views += 1
    post.save()
