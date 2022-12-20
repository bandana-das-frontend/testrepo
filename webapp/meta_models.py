import os
import uuid


def get_file_path(instance, filename):
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid.uuid4(), ext)
    return os.path.join('polls', filename)


def upload_live_updates_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'live_updates/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )

def upload_posts_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'posts/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )


def upload_questions_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'questions/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )


def upload_users_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'profile_pictures/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )


def upload_topics_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'topics/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )


def upload_events_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'events/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )


def upload_places_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'places/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )


def upload_advertisements_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'advertisements/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )


def upload_misc_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'misc/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )


def upload_external_videos_to(instance, filename):
    filename_base, filename_ext = os.path.splitext(filename)
    return 'external_content_videos/%s%s' % (
        str(uuid.uuid4()),
        filename_ext.lower(),
    )


class CHOICES(object):

    def for_each_non_callable_attr(self, callback):
        for attr in dir(self):
            if attr.startswith("__"):
                return

            value = getattr(self, attr)
            if not callable(value):
                callback(attr, value)

    def convert_to_tuple(self):
        t = []
        self.for_each_non_callable_attr(lambda attr, value: t.append((attr, value)))
        return tuple(t)

    def convert_to_list(self):
        t = []
        self.for_each_non_callable_attr(lambda attr, value: t.append(value))
        return t

    def get_str_list(self):
        list = self.convert_to_list()
        t = ''
        for value in list:
            t += value + ','
        return t


PRIVACY_TYPE_CHOICES = (
    ('ME', 'Me'),
    ('ALL', 'All'),
    ('FRIENDS', 'Friends'),
    ('FRIENDS_OF_FRIENDS', 'Friends Of Friends'),
    ('COLLEGE_STUDENT', 'College Student'),
)

FRIENDSHIP_TYPE_CHOICES = (
    ('FRIEND', 'Friend'),
    ('FOLLOW', 'Follow'),
    ('NONE', 'None'),
)

ADMIN_APPROVAL = (
    ('PENDING', 'Pending'),
    ('REJECTED', 'Rejected'),
    ('APPROVED', 'Approved'),
)
# ACTIVITY_TYPE_CHOICES = (
#     ('CREATE_POST', 'Create Post'), #0
#     ('LIKE_POST', 'Like Post'), #1
#     ('COMMENT_POST', 'Comment Post'), #2
#     ('LIKE_POST_COMMENT', 'Like Post Comment'), #3
#     ('SPAM_POST', 'Report Post as spam'), #4
#     ('SPAM_POST_COMMENT', 'Report Post Comment as spam'), #5
#     ('CREATE_EVENT', 'Create event'), #6
#     ('GOING_TO_EVENT', 'Going to event'), #7
#     ('COMMENT_EVENT', 'Comment on event'), #8
#     ('LIKE_COMMENT_EVENT', 'Like comment on event'), #9
#     ('NOT_GOING_TO_EVENT', 'Not going to event'), #10
#     ('SPAM_EVENT', 'Report event as spam'), #11
#     ('SPAM_EVENT_COMMENT', 'Report event comment as spam'), #12
#     ('CHECKIN', 'Check-in'), #13
#     ('CHECKOUT', 'Check-out'), #14
#     ('CREATE_MEETUP', 'Create Meetup'), #15
#     ('JOIN_MEETUP', 'Join Meetup'), #16
#     ('LIKE_MEETUP_COMMENT', 'Like meetup comment'), #17
#     ('POLL_COMMENT', 'Poll Comment'), #18
#     ('VIEW_EMAIL', 'View Email'), #19
# )


class ActivityType(CHOICES):
    CREATE_POST = 'CREATE_POST'
    LIKE_POST = 'LIKE_POST'
    COMMENT_POST = 'COMMENT_POST'
    LIKE_POST_COMMENT = 'LIKE_POST_COMMENT'
    SPAM_POST = 'SPAM_POST'
    SPAM_POST_COMMENT = 'SPAM_POST_COMMENT'
    CREATE_EVENT = 'CREATE_EVENT'
    GOING_TO_EVENT = 'GOING_TO_EVENT'
    COMMENT_EVENT = 'COMMENT_EVENT'
    LIKE_COMMENT_EVENT = 'LIKE_COMMENT_EVENT'
    NOT_GOING_TO_EVENT = 'NOT_GOING_TO_EVENT'
    SPAM_EVENT = 'SPAM_EVENT'
    SPAM_EVENT_COMMENT = 'SPAM_EVENT_COMMENT'
    CHECKIN = 'CHECKIN'
    CHECKOUT = 'CHECKOUT'
    CREATE_MEETUP = 'CREATE_MEETUP'
    JOIN_MEETUP = 'JOIN_MEETUP'
    LIKE_MEETUP_COMMENT = 'LIKE_MEETUP_COMMENT'
    POLL_COMMENT = 'POLL_COMMENT'
    VIEW_EMAIL = 'VIEW_EMAIL'
    LIKE_PROGRAM = 'LIKE_PROGRAM'
    LIKE_PROGRAM_COMMENT = 'LIKE_PROGRAM_COMMENT'
    SAVE_POST = 'SAVE_POST'
    SAVE_PROGRAM = 'SAVE_PROGRAM'


    def get_choices(self):
        return self.convert_to_tuple()


class ObjectType(CHOICES):
    POLL = 'POLL'
    USER = 'USER'
    TOPIC = 'TOPIC'
    POST = 'POST'
    POST_COMMENT = 'POST_COMMENT'
    EVENT = 'EVENT'
    EVENT_COMMENT = 'EVENT_COMMENT'
    POLL_COMMENT = 'POLL_COMMENT'
    PROGRAM = 'PROGRAM'
    PROGRAM_COMMENT = 'PROGRAM_COMMENT'

    def get_choices(self):
        return self.convert_to_tuple()

# OBJECT_TYPE_CHOICES = (
#     ('POLL', 'Poll'),
#     ('USER', 'User'),
#     ('TOPIC', 'Topic'),
#     ('POST', 'Post'),
#     ('POST_COMMENT', 'Post Comment'),
#     ('EVENT', 'Event'),
#     ('EVENT_COMMENT', 'Event Comment'),
#     ('POLL_COMMENT', 'Poll Comment'),
# )

INVITE_REQUEST_STATUS = [
    ('RECEIVED', 'Received'),
    ('SENT', 'Sent'),
    ('SEEN', 'Seen'),
    ('REG', 'Registered'),
    ('CLOSHUR', 'Closhur'),
    ('SPAM', 'Spam'),
]

ANALYTICS_USER_STATUS = [
    ('NONE', 'None'),
    ('NEW', 'New'),
    ('RETURNING', 'Returning'),
    ('REG', 'Registered'),
    ('FAILED', 'Failed'),
]

POST_STATUS = (
    ('ACTIVE', 'Active'),
    ('DELETED', 'Deleted'),
    ('NO_TITLE', 'No Title'),
    ('NO_TITLE_POPULAR', 'No Title Popular'),
    ('FEED_FIX', 'Feed fix'),

)

POST_TYPES = (
    ('QUESTION', 'Question'),
    ('RECOMMEND', 'Recommend'),
    ('SHARE', 'Share'), # Moved to RECOMMEND
    ('DISCUSS', 'Discuss'),
    ('LOOKING_TO_MEET', 'Looking to meet'),
    ('ASK_RECOMMENDATION', 'Ask Recommendation'),
    ('POLL', 'Poll')
)


COMMENT_TYPES = (
    ('TEXT', 'text'),
    ('IMAGE', 'image'),
)


# Syntax from http://stackoverflow.com/a/3523128/780095
FEED_TYPES = [
    'FEED_POST',
    'FEED_MEETUPS',
    'RECOMM_POST',
    'RECOMM_PEOPLE',
    'RECOMM_POLL',
    'SHOW_RATE_US'
]


class FeedTypes(object):
    FEED_POST = 'FEED_POST'
    FEED_MEETUP = 'FEED_MEETUP' # signle meetup object on meetup list
    FEED_MEETUPS = 'FEED_MEETUPS' #many meetups on post list
    FAR_AWAY_MEETUPS_SEPARATOR = 'FAR_AWAY_MEETUPS_SEPARATOR'
    RECOMM_POST = 'RECOMM_POST'
    RECOMM_PEOPLE = 'RECOMM_PEOPLE'
    RECOMM_POLL = 'RECOMM_POLL'
    SHOW_RATE_US = 'SHOW_RATE_US'


class FeedContentType(CHOICES):
    ALL = 'ALL'
    CITY = 'CITY'
    AREA = 'AREA'
    BRANCH = 'BRANCH'


COLLEGE_STATUS_CHOICES = (
    ('LOCKED', 'Locked'),
    ('UNLOCKED', 'Un-Locked'),
    ('UNVERIFIED', 'Un-Verified'),
)


EVENT_PRIVACY = (
    ('ALL', 'All'),
    ('COLLEGE_STUDENT', 'College Student'),
    ('INVITE', 'Invite'),
    ('BUSINESS', 'Business'),
)

EVENT_TYPE = (
    ('EXTERNAL_EVENT', 'External event'),
    ('NATIVE_EVENT', 'Native event'),
)


PLACE_TYPES = (
    ('CITY', 'City'),
    ('AREA', 'Area'),
    ('STATE', 'State'),
    ('COUNTRY', 'Country'),
    ('COLLEGE', 'College'),
    ('PUB', 'Pub'),
    ('BUSINESS', 'Business Place'),
    ('WORLDWIDE', 'Worldwide')
)


PLACE_CONVERSATION_TYPES = (
    ('CHECKIN', 'Check-in'),
    ('CHECKOUT', 'Check-out'),
    ('CHAT', 'Chat'),
)


FEEDBACK_TYPES = (
    ('FEEDBACK', 'Feedback'),
    ('FB_NO', 'No Facebook'),
    ('FB_NOT_SAFE', 'Not safe using FB'),
    ('FB_UNABLE_TO_LOGIN', 'Unable to login'),
    ('FB_OTHER', 'Other Facebook issue'),
    ('MCP_SEARCH_HISTORY', 'Search history'),
    ('DELETE_FEEDBACK', 'Delete feedback'),
    ('POST_CHANGE_SUGGESTION', 'Post changes suggestions'),
    ('LIKE_GLYNK_APP', 'Like the Glynk App'),
    ('SUGGEST_IMPROVEMENTS', 'Suggest improvements'),
    ('FEMALE_PRIVACY_IMPROVEMENTS', 'Female privacy improvements'),
    ('REPORT_ISSUES', 'Report issues'),
    ('DONT_LIKE_APP', 'Don\'t like the app'),
    ('IOS_DEEP_LINK', 'iOS Deep Url Data'),
    ('CRASH', 'Crash :(')
)


ACTIVITY_MESSAGING_TYPES = (
    ('MEETUP', 'Meet up'),
    ('POST', 'Post'),
    ('Activity', 'Activity'),
)

ANALYTICS_TYPE = (
    ('DEFAULT', 'Default'),
    ('MCP', 'MCP'),
    ('LOGIN', 'Login'),
)

QUERY_ANALYTICS_TYPE = (
    ('DISCOVERY', 'Discovery page'),
)


class NotificationType(object):
    FIRST_NOTIF = 'FIRST_NOTIF'
    MESSAGE = 'MESSAGE'
    MESSAGE_REQUEST = 'MESSAGE_REQUEST'
    MESSAGE_APPROVE = 'MESSAGE_APPROVE'
    FOLLOW = 'FOLLOW'
    INVITE_OPINION_MATCH = 'INVITE_OPINION_MATCH'
    ACCEPT_OPINION_MATCH = 'ACCEPT_OPINION_MATCH'
    FB_FRIEND_JOINED = 'FB_FRIEND_JOINED'
    SAME_DESIGNATION_USERS = 'SAME_DESIGNATION_USERS'
    FRIEND_CREATED_POST = 'FRIEND_CREATED_POST'
    COMMENT_ON_POST = 'COMMENT_ON_POST'
    LIKE_POST_COMMENT = 'LIKE_POST_COMMENT'
    FOLLOW_POST = 'FOLLOW_POST'
    REFERRED_POST_NOTIF = 'REFERRED_POST_NOTIF'
    INVITEE_NOTIF = 'INVITEE_NOTIF'
    FB_EXISTING_FRIENDS = 'FB_EXISTING_FRIENDS'
    COLLEGE_UNLOCKED = 'COLLEGE_UNLOCKED'
    RSVP_EVENT = 'EVENT_RSVP'
    INVITED_TO_EVENT = 'EVENT_INVITE'
    COMMENT_ON_EVENT = 'COMMENT_ON_EVENT'
    LIKE_EVENT_COMMENT = 'LIKE_EVENT_COMMENT'
    UPLOAD_EVENT_IMAGE = 'UPLOAD_EVENT_IMAGE'
    MCP_ADD_DESC = 'MCP_ADD_DESC'
    MEETUP_JOIN = 'MEETUP_JOIN'
    MEETUP_JOIN_REQUEST = 'MEETUP_JOIN_REQUEST'
    MEETUP_JOIN_APPROVE = 'MEETUP_JOIN_APPROVE'
    MEETUP_COMMENT = 'MEETUP_COMMENT'
    MEETUP_INVITE = 'MEETUP_INVITE'
    MEETUP_EDIT = 'MEETUP_EDIT'
    MEETUP_NO_ONE_JOINED = 'MEETUP_NO_ONE_JOINED'
    GLYNK_POST = 'GLYNK_POST'
    GLYNK_MEETUP = 'GLYNK_MEETUP'
    GLYNK_POLL = 'GLYNK_POLL'
    DISCOVERY_TAB = 'DISCOVERY_TAB'
    RECOS_FOR_YOU = 'RECOS_FOR_YOU'
    SET_BIO = 'SET_BIO'
    USER_MILESTONE = 'USER_MILESTONE'
    CREATE_POST_RECO = 'CREATE_POST_RECO'
    UPLOAD_MEETUP_IMAGE = 'UPLOAD_MEETUP_IMAGE'
    FAVOURITE = 'FAVOURITE'
    REQUEST_TO_POST = 'REQUEST_TO_POST'
    USER_MENTIONS_IN_POST = 'USER_MENTIONS_IN_POST'
    USER_MENTIONS_IN_COMMENT = 'USER_MENTIONS_IN_COMMENT'
    USER_MENTIONS_IN_MEETUP = 'USER_MENTIONS_IN_MEETUP'
    USER_MENTIONS_IN_MEETUP_COMMENT = 'USER_MENTIONS_IN_MEETUP_COMMENT'
    SIGNUP_REQUEST = 'SIGNUP_REQUEST'
    ONBOARDING_USER_RECOMMENDATION = 'ONBOARDING_USER_RECOMMENDATION'
    RECENTLY_JOINED_USERS = 'RECENTLY_JOINED_USERS'
    USER_JOIN = 'USER_JOIN'
    USER_FROM_COLLEGE_JOINED = 'USER_FROM_COLLEGE_JOINED'
    USER_FROM_WORKPLACE_JOINED = 'USER_FROM_WORKPLACE_JOINED'
    USER_FROM_HOMETOWN_JOINED = 'USER_FROM_HOMETOWN_JOINED'
    EMAIL_VERIFIED = 'EMAIL_VERIFIED'
    LIKE_GROUP_CHAT_MESSAGE = 'LIKE_GROUP_CHAT_MESSAGE'
    POST_FOR_MODERATION = 'POST_FOR_MODERATION'
    GROUP_CHAT_MESSAGE = 'GROUP_CHAT_MESSAGE'


MCP_ANALYTICS_STATUS_TYPES = [
    'ALICIA',
    'INTEREST',
    'INTEREST_SELECTED',
    'RECOMMENDING',
    'RECOMMENDED',
    'DESCRIBED',
    'SUBMITTED',
    'SKIPPED',
]

MEETUP_STATUS = (
    ('EXPIRED', 'Expired'),
    ('LIVE', 'Live'),
    ('FUTURE', 'Future'),
)

class MeetupStatus(object):
    EXPIRED = "EXPIRED"
    LIVE = "LIVE"
    FUTURE = "FUTURE"

MEETUP_GOING_STATUS = (
    ('REQUESTED', 'Requested'),
    ('ENTERED', 'Entered'),
    ('APPROVED', 'Approved'),
    ('REVOKED', 'Revoked'),
    ('REJECT', 'Reject'),
    ('LEFT', 'Left'),
)

MEETUP_COMMENT_SYSTEM_MESSAGE_TYPE = (
    ('USER_JOINED', 'User Joined'),
    ('USER_EDITED', 'User Edited'),
    ('USER_LEFT', 'User left'),
    ('USER_CREATED', 'User created'),
    ('ICE_BREAKER', 'Ice Breaker')
)


class MeetupCommentSystemMessageType(object):
    USER_JOINED = 'USER_JOINED'
    USER_EDITED = 'USER_EDITED'
    USER_LEFT = 'USER_LEFT'
    USER_CREATED = 'USER_CREATED'
    ICE_BREAKER = 'ICE_BREAKER'


class MeetupGoingStatus(object):
    REQUESTED = 'REQUESTED'
    ENTERED = 'ENTERED'
    APPROVED = 'APPROVED'
    REVOKED = 'REVOKED'
    REJECT = 'REJECT'
    LEFT = 'LEFT'


class MatchMeetupStatus(object):
    NEW_MEETUP_CREATED = 'NEW_MEETUP_CREATED'
    YOU_ALREADY_ON_MEETUP = 'YOU_ALREADY_ON_MEETUP'
    JOINED_IN_MEETUP = 'JOINED_IN_MEETUP'
    HOUSE_FULL = 'HOUSE_FULL'
    NO_MATCHING_MEETUP = 'NO_MATCHING_MEETUP'


CHAT_REQUEST_STATUS = (
    ('REQUESTED', 'Requested'),
    ('APPROVED', 'Approved'),
    ('REJECT', 'Reject'),
    ('BLANK', 'Blank'),
)


class ChatRequestStatus(object):
    REQUESTED = 'REQUESTED'
    APPROVED = 'APPROVED'
    REJECT = 'REJECT'
    BLANK = 'BLANK'


class USER_AUTH_TYPES(object):
    EMAIL = 'EMAIL'
    PHONE_NUMBER = 'PHONE_NUMBER'
    FACEBOOK = 'FACEBOOK'
    FB_ANONYMOUS = 'FB_ANONYMOUS'

    ACCOUNT_KIT = 'ACCOUNT_KIT'
    FIREBASE_SMS = 'FIREBASE_SMS'
    CUSTOM_SMS = 'CUSTOM_SMS'
    CUSTOM_EMAIL = 'CUSTOM_EMAIL'
    GUEST_LOGIN = 'GUEST_LOGIN'


class CommunityNames(object):
    Runwal = 'Runwal Greens'
    Hobit = 'Hobit'
    Nestaway = 'Nestaway'


class ShakeEntryPoint(object):
    shake_from_inside_app = 'shake_from_inside_app'
    shake_from_outside_app = 'shake_from_outside_app'


# ['entry_point'] = 'post_from_fb'
# ['entry_point'] = 'comment_from_fb'

WORK_DESIGNATIONS = [
    'Advertiser',
    'Air Hostess',
    'Analyst',
    'Architect',
    'Artist',
    'Auditor',
    'Banker',
    'Business Owner',
    'Chartered Accountant',
    'Chef',
    'Civil Lawyer',
    'Civil Servant',
    'Criminal Lawyer',
    'Consultant',
    'Content Writer',
    'Communication Designer',
    'Community Manager',
    'Corporate Lawyer',
    'Customer Support',
    'CXO',
    'Data Scientist',
    'Doctor',
    'Engineer',
    'Entrepreneur',
    'Event Planner',
    'Fashion Designer',
    'Filmmaker',
    'Founder',
    'Freelancer',
    'General Manager',
    'Graphic Designer',
    'Government Servant',
    'Hardware Engineer',
    'Human Resource',
    'Industrial designer',
    'Investment Professional',
    'Judge',
    'Media Professional',
    'Military Personnel',
    'Partner',
    'Pilot',
    'Planning & Strategy',
    'Politician',
    'Product Manager',
    'Professor',
    'Proprietor',
    'Public Relations',
    'QA Engineer',
    'Recruiter',
    'Sales & BD',
    'Scientist',
    'Social Worker',
    'Software Architect',
    'Software Developer',
    'Sportsperson',
    'Supply chain',
    'Teacher',
    'Tech Support',
    'Trainer',
    'UX Designer',
    'Writer',
    'Others'
]


GENDER_PRIVACY = (
    ('w_m', 'All'),
    ('w', 'Women'),
    ('m', 'Men')
)


BRANCH_CATEGORIES = (
    ('Engineering', 'Engineering'),
    ('Management', 'Management'),
    ('Medical', 'Medical'),
    ('Science', 'Science'),
    ('Arts', 'Arts'),
    ('Commerce', 'Commerce'),
    ('Information', 'Information'),
    ('Law', 'Law'),
    ('Architecture', 'Architecture'),
    ('Others', 'Others'),
)



class CommunityType(CHOICES):
    TECH_PARK = 'TECH_PARK'
    OFFICE = 'OFFICE'
    APARTMENT = 'APARTMENT'
    VIRTUAL = 'VIRTUAL'
    COLLEGE = 'COLLEGE'
    SPIRITUAL = 'SPIRITUAL'
    CO_WORKING = 'CO_WORKING'
    VC_FIRM = 'VC_FIRM'
    CLUB = 'CLUB'
    CO_LIVING = 'CO_LIVING'
    ALUMNI = 'ALUMNI'
    WORKPLACE = 'WORKPLACE'
    STARTUP = 'STARTUP'

    def get_choices(self):
        return self.convert_to_tuple()


class PhoneAuth(CHOICES):
    ACCOUNT_KIT = 'ACCOUNT_KIT'
    FIREBASE_SMS = 'FIREBASE_SMS'
    CUSTOM_SMS = 'CUSTOM_SMS'

    def get_choices(self):
        return PhoneAuth().convert_to_tuple()


class DefaultTab(CHOICES):
    MEETUP = 'MEETUP'
    INTERACT = 'INTERACT'
    FRIENDS = 'FRIENDS'
    PROFILE = 'PROFILE'

    def get_choices(self):
        return DefaultTab().convert_to_tuple()


class GROUP_CHAT_TYPE(CHOICES):
    COMMUNITY = 'COMMUNITY'
    INTEREST = 'INTEREST'
    WORK_PLACE = 'WORKPLACE'
    WORKPLACE_LOCATION = 'WORKPLACE_LOCATION'
    WORK_DESIGNATION = 'WORK_DESIGNATION'
    AREA = 'AREA'
    CURRENT_CITY = 'CURRENT_CITY'
    HOME_TOWN = 'HOME_TOWN'
    HOME_STATE = 'HOME_STATE'
    COLLEGE = 'COLLEGE'
    COLLEGE_BRANCH_JOIN_YEAR = 'COLLEGE_BRANCH_JOIN_YEAR'
    COLLEGE_JOIN_YEAR = 'COLLEGE_JOIN_YEAR'
    MARKETING = 'MARKETING'
    TOWER = 'TOWER'
    ROOMATES = 'ROOMATES'
    COLLEGE_ALUMNI = 'COLLEGE_ALUMNI'
    COLLEGE_ADMIN = 'COLLEGE_ADMIN'
    USER_CREATED = 'USER_CREATED'
    COMMUNITY_BRANCH = 'COMMUNITY_BRANCH'
    NEW_MEMBERS = 'NEW_MEMBERS'
    SCHOOL = 'SCHOOL'
    CUSTOM = 'CUSTOM'
    PARAMETER_BASED = 'PARAMETER_BASED'

    def get_choices(self):
        return GROUP_CHAT_TYPE().convert_to_tuple()


class GROUP_CHAT_ACCESS(CHOICES):
    ALL = 'ALL'
    ADMIN_ONLY = 'ADMIN_ONLY'

    def get_choices(self):
        return GROUP_CHAT_ACCESS().convert_to_tuple()

class POST_CTA(CHOICES):
    CREATE_POST = 'CREATE_POST'
    CREATE_MEETUP = 'CREATE_MEETUP'
    CREATE_GROUP = 'CREATE_GROUP'
    OPEN_LINK = 'OPEN_LINK'
    NONE = 'NONE'

    def get_choices(self):
        return POST_CTA().convert_to_tuple()

class COMPLAINT_STATUS(CHOICES):
    OPEN = 'OPEN'
    ASSIGNED = 'ASSIGNED'
    CLOSED = 'CLOSED'
    NONE = 'NONE'

    def get_choices(self):
        return COMPLAINT_STATUS().convert_to_tuple()

class COMPLAINT_PRIORITY(CHOICES):
    EMERGENCY = 'EMERGENCY'
    LOW = 'LOW'
    NONE = 'NONE'

    def get_choices(self):
        return COMPLAINT_PRIORITY().convert_to_tuple()

class COLLEGE_USER_RELATION(CHOICES):
    STUDENT = 'STUDENT'
    ALUMNI = 'ALUMNI'
    ADMIN = 'ADMIN'
    NONE = 'NONE'

    def get_choices(self):
        return COLLEGE_USER_RELATION().convert_to_tuple()


class REWARD_TYPE(CHOICES):
    COUPONS = 'COUPONS'
    PAYTM = 'PAYTM'
    CASH = 'CASH'

    def get_choices(self):
        return REWARD_TYPE().convert_to_tuple()


class REWARD_STATUS(CHOICES):
    ACTIVE = 'ACTIVE'
    INACTIVE = 'INACTIVE'

    def get_choices(self):
        return REWARD_STATUS().convert_to_tuple()


class REWARD_TRANSACTIONS_STATUS(CHOICES):
    FAILED = 'FAILED'
    PENDING = 'PENDING'
    REDEEMED = 'REDEEMED'
    REJECTED = 'REJECTED'
    PAYMENT_ISSUE = 'PAYMENT_ISSUE'

    def get_choices(self):
        return REWARD_TRANSACTIONS_STATUS().convert_to_tuple()


class PRIVACY_VISIBLE_TO(CHOICES):
    ALL_MEMBERS = 'ALL_MEMBERS'
    ONLY_ME = 'ONLY_ME'

    def get_choices(self):
        return self.convert_to_tuple()


class NotificationChannels(object):
    ACTIVITY_NOTIFICATION = {"id": 1, "name": 'Activity notifications'}
    NEW_MEMBER_NOTIFICATION = {"id": 2, "name": 'New member notification'}
    GROUP_NOTIFICATION = {"id": 3, "name": 'Community Group Notifications'}


class POST_PRIVACY(CHOICES):
    ALL = 'ALL'
    LOCATION_SPECIFIC = 'LOCATION_SPECIFIC'
    MEN_ONLY = 'MEN_ONLY'
    WOMEN_ONLY = 'WOMEN_ONLY'

    def get_choices(self):
        return self.convert_to_tuple()


class GENDER(CHOICES):
    NONE = None
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

    def get_choices(self):
        return self.convert_to_tuple()

STATIC_INFO_SECTION_ANDROID_SCREEN = (
    ('com.glynk.app.features.announcements.AnnouncementActivity', 'AnnouncementActivity'),
    ('com.glynk.app.features.complaints.activities.MyComplaintsActivity', 'MyComplaintsActivity'),
    ('com.glynk.app.common.activity.BrowserActivity', 'BrowserActivity'),
    ('com.glynk.app.features.staticinfo.StaticInfoActivity', 'StaticInfoActivity'),
    ('com.glynk.app.features.paydues.PayDuesActivity', 'PayDuesActivity'),
    ('com.glynk.app.features.meetingroom.MeetingRoomActivity', 'MeetingRoomActivity'),
    ('com.glynk.app.features.dynamicinfo.DynamicInfoActivity', 'DynamicInfoActivity'),
    ('com.glynk.app.features.offers.OffersActivity', 'OffersActivity')
)

STATIC_INFO_SECTION_IOS_SCREEN = (
    ('AnnouncementVC', 'AnnouncementVC'),
    ('SafariVC', 'SafariVC'),
    ('StaticInfoFAQVC', 'StaticInfoFAQVC'),
    ('DynamicInfoVC', 'DynamicInfoVC'),
    ('PaymentVC', 'PaymentVC'),
    ('ComplaintsVC', 'ComplaintsVC'),
    ('OffersVC', 'OffersVC')
)


STATIC_INFO_SUB_SECTION = (
    ('WIFI', 'Wifi'),
    ('AGREEMENT', 'Agreement'),
    ('GATETIME', 'Gate time'),
    ('OFFER', 'Offer'),
    ('ROOMMATES', 'Roommate'),
    ('APARTMENT_NAME', 'Apartment Name'),
    ('APARTMENT_ADDRESS', 'Apartment Address'),
    ('FAQ_QUESTION_1', 'FAQ Question 1'),
    ('FAQ_QUESTION_2', 'FAQ Question 2'),
    ('FAQ_QUESTION_3', 'FAQ Question 3'),
    ('FAQ_QUESTION_4', 'FAQ Question 4'),
    ('FAQ_QUESTION_5', 'FAQ Question 5'),
    ('TEAM_MEMBER_1', 'Team Member 1'),
    ('TEAM_MEMBER_2', 'Team Member 2'),
    ('TEAM_MEMBER_3', 'Team Member 3'),
    ('TEAM_MEMBER_4', 'Team Member 4'),
    ('TEAM_MEMBER_5', 'Team Member 5'),
)


class DISCOVER_PROFILE_CARD_TYPE(CHOICES):
    SIMPLE = 'SIMPLE'
    RICH = 'RICH'

    def get_choices(self):
        return DISCOVER_PROFILE_CARD_TYPE().convert_to_tuple()


class BOOKING_TYPE(CHOICES):
    SCHEDULED = 'SCHEDULED'
    BLOCKED = 'BLOCKED'
    CANCELED = 'CANCELED'

    def get_choices(self):
        return BOOKING_TYPE().convert_to_tuple()


class POST_MEDIA_TYPES(CHOICES):
    IMAGE = 'IMAGE'
    VIDEO = 'VIDEO'
    DOCUMENT = 'DOCUMENT'

    def get_choices(self):
        return POST_MEDIA_TYPES().convert_to_tuple()


class USER_TAGS(CHOICES):
    CELEBRITY = 'CELEBRITY'
    STARTUP = 'STARTUP'
    CORPORATE = 'CORPORATE'

    def get_choices(self):
        return USER_TAGS().convert_to_tuple()


class TOPIC_TYPE_CHOICES(CHOICES):
    CATEGORY = 'CATEGORY'
    TAG = 'TAG'

    def get_choices(self):
        return TOPIC_TYPE_CHOICES().convert_to_tuple()


class INVITEE_TYPE(CHOICES):
    STARTUP = 'STARTUP'
    CORPORATE = 'CORPORATE'

    def get_choices(self):
        return INVITEE_TYPE().convert_to_tuple()


class INVITEE_STATUS(CHOICES):
    ACTIVE = 'ACTIVE'
    TRIAL = 'TRIAL'
    EXPIRED = 'EXPIRED'

    def get_choices(self):
        return INVITEE_STATUS().convert_to_tuple()


class POST_LAYOUT_TYPE(CHOICES):
    DEFAULT = 'DEFAULT'
    NEWS = 'NEWS'
    BIG_NEWS = 'BIG_NEWS'

    def get_choices(self):
        return POST_LAYOUT_TYPE().convert_to_tuple()


class OnboardingScreens(CHOICES):
    WELCOME_SCREEN = 'WELCOME_SCREEN'
    COLLECT_NAME = 'COLLECT_NAME'
    COLLECT_GENDER = 'COLLECT_GENDER'
    COLLECT_DOB = 'COLLECT_DOB'
    COLLECT_AREA = 'COLLECT_AREA'
    COLLECT_HOMETOWN = 'COLLECT_HOMETOWN'
    COLLECT_PROFILE_PIC = 'COLLECT_PROFILE_PIC'
    COLLECT_COLLEGE = 'COLLECT_COLLEGE'
    COLLECT_COLLEGE_BRANCH = 'COLLECT_COLLEGE_BRANCH'
    COLLECT_COLLEGE_RELATION = 'COLLECT_COLLEGE_RELATION'
    COLLECT_SCHOOL = 'COLLECT_SCHOOL'
    COLLECT_APARTMENT = 'COLLECT_APARTMENT'
    COLLECT_WORKPLACE = 'COLLECT_WORKPLACE'
    COLLECT_INTERESTS = 'COLLECT_INTERESTS'
    COLLECT_COMMUNITY_BRANCH = 'COLLECT_COMMUNITY_BRANCH'


# PeopleDiscoveryFilter is the list of filter types supported to filter users.
# These filter are used in click-able info links in user profile and discover card
class PeopleDiscoveryFilter(CHOICES):
    FILTER_TYPE_HOMETOWN = 'FILTER_TYPE_HOMETOWN'
    FILTER_TYPE_HOME_STATE = 'FILTER_TYPE_HOME_STATE'
    FILTER_TYPE_COLLEGE = 'FILTER_TYPE_COLLEGE'
    FILTER_TYPE_WORKPLACE = 'FILTER_TYPE_WORKPLACE'
    FILTER_TYPE_NOT_WORKING_CURRENTLY = 'FILTER_TYPE_NOT_WORKING_CURRENTLY'
    FILTER_TYPE_DESIGNATION = 'FILTER_TYPE_DESIGNATION'
    FILTER_TYPE_USER_METADATA = 'FILTER_TYPE_USER_METADATA'
    FILTER_TYPE_COLLEGE_BRANCH = 'FILTER_TYPE_COLLEGE_BRANCH'
    FILTER_TYPE_COLLEGE_JOIN_YEAR = 'FILTER_TYPE_COLLEGE_JOIN_YEAR'
    FILTER_TYPE_AREA = 'FILTER_TYPE_AREA'
    FILTER_TYPE_CURRENT_CITY = 'FILTER_TYPE_CURRENT_CITY'
    FILTER_TYPE_TOWER = 'FILTER_TYPE_TOWER'
    FILTER_TYPE_GENDER = 'FILTER_TYPE_GENDER'
    FILTER_TYPE_COLLEGE_LOCATION = 'FILTER_TYPE_COLLEGE_LOCATION'
    FILTER_TYPE_BRANCH = 'FILTER_TYPE_BRANCH'
    FILTER_TYPE_SKILL = 'FILTER_TYPE_SKILL'
    FILTER_TYPE_SCHOOL = 'FILTER_TYPE_SCHOOL'
    FILTER_TYPE_USER_TAG = 'FILTER_TYPE_USER_TAG'
    FILTER_TYPE_HEADQUARTERS = 'FILTER_TYPE_HEADQUARTERS'


# ProfileInfo is the list of user profile information to be shown in 'User profile -About section' and 'Discover card'
# For each community user profile info and discover profile info list is configured in community record to define
# what information should be show in 'User profile -About section' and 'Discover card' respectively.
# ProfileInfo are also used to define, how the text is formatted to show the information.
class ProfileInfo(CHOICES):
    INFO_CURRENT_CITY = 'INFO_CURRENT_CITY'
    INFO_HOME_TOWN = 'INFO_HOME_TOWN'
    INFO_EDUCATION = 'INFO_EDUCATION'
    INFO_COLLEGE_BRANCH = 'INFO_COLLEGE_BRANCH'
    INFO_COLLEGE_ADMIS_YEAR = 'INFO_COLLEGE_ADMIS_YEAR'
    INFO_WORKPLACE = 'INFO_WORKPLACE'
    INFO_COMMUNITY_BRANCH = 'INFO_COMMUNITY_BRANCH'
    INFO_SCHOOL = 'INFO_SCHOOL'
    INFO_HEAD_QUARTERS = 'INFO_HEAD_QUARTERS'
    INFO_WEB_URL = 'INFO_WEB_URL'
    INFO_VIEW_EMAIL = 'INFO_VIEW_EMAIL'
    INFO_JOINED_DATE = 'INFO_JOINED_DATE'
    INFO_READ_ARTICLES = 'INFO_READ_ARTICLES'
    INFO_NUM_COMMENTS = 'INFO_NUM_COMMENTS'


class ProfileUISections(CHOICES):
    USER_MEDIA_SECTION = 'USER_MEDIA_SECTION'
    PROMPTS_SECTION = 'PROMPTS_SECTION'
    ABOUT_SECTION = 'ABOUT_SECTION'
    INTERESTS_SECTION = 'INTERESTS_SECTION'
    SKILLS_SECTION = 'SKILLS_SECTION'


class ChatSupportChannel(CHOICES):
    GLYNK = 'GLYNK'
    FRONT_APP = 'FRONT_APP'

    def get_choices(self):
        return self.convert_to_tuple()


class INSIGHTS_KEYWORD_TYPE(CHOICES):
    POST = 'POST'
    CHAT = 'CHAT'

    def get_choices(self):
        return self.convert_to_tuple()

class WIDGET_TYPES(CHOICES):
    WEATHER = 'WEATHER'
    COVID = 'COVID'
    CRICKET = 'CRICKET'
    CUSTOM = 'CUSTOM'
    NONE = 'NONE'

    def get_choices(self):
        return WIDGET_TYPES().convert_to_tuple()


# Platform select options for Ads
class AD_PLATFORMS(CHOICES):
    Mobile_web = 'Mobile_web'
    Mobile_app = 'Mobile_app'
    Desktop = 'Desktop'
    All = 'All'
    Web_all = 'Web_all'

    def get_choices(self):
        return AD_PLATFORMS().convert_to_tuple()


# Type select options for Ads
class AD_TYPES(CHOICES):
    Square = 'Square'
    Top = 'Top'
    Popup = 'Popup'
    Horizontal = 'Horizontal'

    def get_choices(self):
        return AD_TYPES().convert_to_tuple()


# Format select options for Ads
class AD_FORMATS(CHOICES):
    Image = 'Image'
    GIF = 'GIF'
    Video = 'Video'

    def get_choices(self):
        return AD_FORMATS().convert_to_tuple()


# Type select options for google Ads
class GOOGLE_AD_TYPES(CHOICES):
    SQUARE = 'SQUARE'
    TOP = 'TOP'
    HORIZONTAL = 'HORIZONTAL'

    def get_choices(self):
        return GOOGLE_AD_TYPES().convert_to_tuple()


# Platform select options for google Ads
class GOOGLE_AD_PLATFORMS(CHOICES):
    MOBILE = 'MOBILE'
    DESKTOP = 'DESKTOP'
    BOTH = 'BOTH'

    def get_choices(self):
        return GOOGLE_AD_PLATFORMS().convert_to_tuple()


# Platform select options for google Ads
class AD_VISIBILITY(CHOICES):
    ALL_ARTICLES = 'ALL_ARTICLES'
    SPECIFIC_ARTICLES = 'SPECIFIC_ARTICLES'

    def get_choices(self):
        return AD_VISIBILITY().convert_to_tuple()

class SUBMISSION_STATUS(CHOICES):
    SUBMITTED = 'SUBMITTED'
    PUBLISHED = 'PUBLISHED'
    REJECTED = 'REJECTED'
    RESUBMITTED = 'RESUBMITTED'

    def get_choices(self):
        return self.convert_to_tuple()


class POST_EDITOR_TYPE(CHOICES):
    DEFAULT = 'DEFAULT'
    RICH = 'RICH'

    def get_choices(self):
        return self.convert_to_tuple()

class EMAIL_TEMPLATE_TYPE(CHOICES):
    WELCOME_EMAIL = 'WELCOME_EMAIL'
    INVITE_EMAIL = 'INVITE_EMAIL'
    DIGEST_EMAIL = 'DIGEST_EMAIL'
    CONTENT_REPORT_EMAIL = 'CONTENT_REPORT_EMAIL'
    POST_IN_TOPICS_EMAIL = "POST_IN_TOPICS_EMAIL"
    WEEKLY_DIGEST_EMAIL = "WEEKLY_DIGEST_EMAIL"
    CHAT_UNREAD_EMAIL = "CHAT_UNREAD_EMAIL"
    COMMENT_ON_POST_POST_FOLLOWER_EMAIL = "COMMENT_ON_POST_POST_FOLLOWER_EMAIL"
    COMMENT_ON_POST_ORIGINAL_POSTER_EMAIL = "COMMENT_ON_POST_ORIGINAL_POSTER_EMAIL"
    OTP_EMAIL = "OTP_EMAIL"
    MENTIONS_EMAIL = "MENTIONS_EMAIL"
    CHAT_REQUEST_EMAIL = "CHAT_REQUEST_EMAIL"
    CHAT_APPROVE_EMAIL = "CHAT_APPROVE_EMAIL"
    FEATURED_POST_EMAIL = "FEATURED_POST_EMAIL"
    RSVP_EMAIL = "RSVP_EMAIL"
    ONBOARDING_WIZARD_REMINDER_EMAIL = "ONBOARDING_WIZARD_REMINDER_EMAIL"
    INVITE_MEMBER_EMAIL = 'INVITE_MEMBER_EMAIL'
    TEAM_MEMBER_INVITE_EMAIL = 'TEAM_MEMBER_INVITE_EMAIL'
    NEW_BADGES_TAGS_EMAIL = 'NEW_BADGES_TAGS_EMAIL'

    def get_choices(self):
        return self.convert_to_tuple()


class AD_IMPRESSION_TYPE(CHOICES):
    FB_INSTANT_ARTICLE = 'FB_INSTANT_ARTICLE'
    def get_choices(self):
        return self.convert_to_tuple()
