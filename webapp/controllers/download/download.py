from django.shortcuts import HttpResponseRedirect


def download(request):
    community = request.community
    user_agent = request.META['HTTP_USER_AGENT']

    # todo : Have to find mobile OS and redirect to that store
    # if show_preview(user_agent):
    #     return HttpResponseRedirect(community.invite_url)
    if 'iPhone' in user_agent or 'iPad' in user_agent:
        return HttpResponseRedirect(community.app_store_url)
    else:
        return HttpResponseRedirect(community.play_store_url)


def show_preview(user_agent):
    user_agent = user_agent.lower()
    if 'whatsapp' in user_agent or \
            'telegrambot' in user_agent or \
            'linkedin' in user_agent or \
            'twitter' in user_agent or \
            'facebook' in user_agent:
        return True

    return False
