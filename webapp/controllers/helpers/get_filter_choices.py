from webapp.models import *


def get_filter_choices(community):
    PRODUCT_HUNT_COMMUNITY_ID = 29
    if community.community_type == CommunityType.APARTMENT:
        filter_choices = [
            PeopleDiscoveryFilter.FILTER_TYPE_TOWER,
            PeopleDiscoveryFilter.FILTER_TYPE_WORKPLACE,
            PeopleDiscoveryFilter.FILTER_TYPE_HOME_STATE,
            PeopleDiscoveryFilter.FILTER_TYPE_DESIGNATION
        ]
    elif community.community_type == CommunityType.CLUB:
        filter_choices = [
            PeopleDiscoveryFilter.FILTER_TYPE_AREA,
            PeopleDiscoveryFilter.FILTER_TYPE_CURRENT_CITY,
            PeopleDiscoveryFilter.FILTER_TYPE_HOME_STATE,
            PeopleDiscoveryFilter.FILTER_TYPE_GENDER
        ]
    elif community.community_type == CommunityType.CO_LIVING:
        filter_choices = [
            PeopleDiscoveryFilter.FILTER_TYPE_AREA,
            PeopleDiscoveryFilter.FILTER_TYPE_CURRENT_CITY,
            PeopleDiscoveryFilter.FILTER_TYPE_HOME_STATE,
            PeopleDiscoveryFilter.FILTER_TYPE_GENDER
        ]
    elif community.community_type == CommunityType.VIRTUAL:
        filter_choices = [
            PeopleDiscoveryFilter.FILTER_TYPE_AREA,
            PeopleDiscoveryFilter.FILTER_TYPE_CURRENT_CITY,
            PeopleDiscoveryFilter.FILTER_TYPE_HOME_STATE,
            PeopleDiscoveryFilter.FILTER_TYPE_GENDER
        ]
    elif community.community_type == CommunityType.COLLEGE:
        filter_choices = [
            PeopleDiscoveryFilter.FILTER_TYPE_COLLEGE_BRANCH,
            PeopleDiscoveryFilter.FILTER_TYPE_COLLEGE_JOIN_YEAR,
            PeopleDiscoveryFilter.FILTER_TYPE_HOME_STATE,
            PeopleDiscoveryFilter.FILTER_TYPE_GENDER
        ]
    elif community.community_type == CommunityType.TECH_PARK:
        filter_choices = [
            PeopleDiscoveryFilter.FILTER_TYPE_DESIGNATION,
            PeopleDiscoveryFilter.FILTER_TYPE_WORKPLACE,
            PeopleDiscoveryFilter.FILTER_TYPE_AREA,
            PeopleDiscoveryFilter.FILTER_TYPE_GENDER
        ]
    elif community.id == PRODUCT_HUNT_COMMUNITY_ID:
        filter_choices = [
            PeopleDiscoveryFilter.FILTER_TYPE_CURRENT_CITY,
            PeopleDiscoveryFilter.FILTER_TYPE_DESIGNATION,
            PeopleDiscoveryFilter.FILTER_TYPE_GENDER
        ]
    else:
        filter_choices = [
            PeopleDiscoveryFilter.FILTER_TYPE_CURRENT_CITY,
            PeopleDiscoveryFilter.FILTER_TYPE_DESIGNATION,
            PeopleDiscoveryFilter.FILTER_TYPE_GENDER
        ]
    return filter_choices
