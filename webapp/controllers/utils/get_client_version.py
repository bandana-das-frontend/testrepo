
def get_client_version(request):
    version = 0
    client = 'android'

    if 'HTTP_CLIENT_VERSION' in request.META and int(request.META['HTTP_CLIENT_VERSION']):
        version = int(request.META['HTTP_CLIENT_VERSION'])

    if 'HTTP_CLIENT_TYPE' in request.META:
        client = request.META['HTTP_CLIENT_TYPE']

    if 'HTTP_SDK_VERSION' in request.META:
        is_sdk = True
    else:
        is_sdk = False

    return version, client, is_sdk


def get_sdk_version(request):
    version = 0

    if 'HTTP_SDK_VERSION' in request.META:
        version = int(request.META['HTTP_SDK_VERSION'])

    return version


def get_client_community(request):
    from webapp import Community

    community = None

    if 'HTTP_COMMUNITY_CODE' in request.META:
        community_code = str(request.META['HTTP_COMMUNITY_CODE'])
        community = Community.objects.filter(unique_code=community_code).first()

    return community


def get_client_package(request):
    client_package = ''
    if 'HTTP_CLIENT_PACKAGE' in request.META:
        client_package = str(request.META['HTTP_CLIENT_PACKAGE'])

    return client_package


def is_coworking_app(request):
    if get_client_package(request) == 'com.glynk.thecoworkingapp':
        return True
    return False


def is_coliving_app(request):
    if get_client_package(request) == 'com.glynk.thecolivingapp':
        return True
    return False


def is_workplace_app(request):
    if get_client_package(request) == 'com.glynk.workplace':
        return True
    return False


def is_alumni_app(request):
    if get_client_package(request) == 'com.glynk.alumni':
        return True
    return False