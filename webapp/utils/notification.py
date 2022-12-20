from django.core.mail import send_mail
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse
from templated_email import send_templated_mail
from webapp.models import *
from django.conf import settings


def sendEmailToHumans(subject, body, from_whom, to_who):
    send_mail(subject, body, from_whom,
        to_who, fail_silently=True)


def send_register_email(user, site):
    try:
        send_templated_mail(
                        template_name='new_user',
                        from_email='Closhur Team  <support@closhur.com>',
                        recipient_list=[user.email],
                        context={
                            'site': site,
                            'user': user
                        },
                )
    except:
        pass


def send_user_stats_email(args,  email):
    new_user, total_user_count, \
    new_polls, total_polls_count, \
    new_votes, total_votes = args['new_user'], args['total_user_count'], \
                              args['new_polls'], args['total_polls_count'], \
                              args['new_votes'], args['total_votes']

    new_user_str = ''
    for user in new_user:
        new_user_str += '\n' + str(user.email) + ', Auth Type: ' + str(user.auth_type) + '\n'

    new_polls_str = ''
    for poll in new_polls:
        new_polls_str += '\n' + str(poll.unique_url)

    sendEmailToHumans('V: ' + str(new_votes) + ', U: ' + str(new_user.count())
                      + ', P: ' + str(new_polls.count()),
                      'New users \n' + str(new_user_str) + '\n\n'
                      + 'New Polls ' + str(new_polls_str) + '\n\n'
                      + 'Total Users: ' + str(total_user_count) + '\n\n'
                      + 'Total User Polls: ' + str(total_polls_count) + '\n\n'
                      + 'Total Votes: ' + str(total_votes['total_votes__sum']),
                      'support@closhur.com', email)


def send_verify_account_email(user, site):
    try:
        send_templated_mail(
                        template_name='verification_email',
                        from_email='Closhur Team  <support@closhur.com>',
                        recipient_list=[user.email],
                        context={
                            'site': site,
                            'user': user
                        },
                )
    except:
        pass


def send_forgot_password_email(user, site):
    try:
        send_templated_mail(
                        template_name='forgot_password',
                        from_email='Closhur Team  <support@closhur.com>',
                        #recipient_list=['niranjan@tokriful.com', 'natarajan@tokriful.com'],
                        recipient_list=[user.email],
                        context={
                            'site': site,
                            'user': user
                        },
                )
    except:
        pass


def send_email_poll_rejected(poll, to):
    if to:
        sendEmailToHumans('Poll rejected',
                          'Hello \nWe are sorry to say that your poll at ' + settings.PROD_URL_POLL + poll.unique_url + ' is rejected by our admin'
                          'The reason for the rejection is ' + poll.not_approval_reason + ' Please edit your poll.'
                           + '\n\nThank you',
                          'support@pollopine.com', [to])


def send_email_poll_approved(poll, to):
    if to:
        sendEmailToHumans('Poll approved',
                          'Hello \nWe are happy to say that your poll at ' + settings.PROD_URL_POLL + poll.unique_url + ' is approved by our admin'
                           + '\n\nThank you',
                          'support@pollopine.com', [to])


def send_register_social_email(user, site):
    sendEmailToHumans('Welcome to ' + site.replace('.com', '') + '!',
                      'Thank you for signing up with Closhur.'
                      '\nWe have also created a dedicated wall for you: http://' + site + 'user/' + user.private_url + '\nwhich you can share with your friends or visit the page yourself to see whats happening with your polls without having to sign in.' +
                      '\n\nThank you,\nThe closhur.com Team',
                      'support@closhur.com', [user.email])


def send_email_private_url(private, to):
    sendEmailToHumans('Private Url Created for Pollopine',
                      'Hello \nWe have created a private url for your account. ' +
                      'You can view/modify/delete the poll you just created' +
                      'using this url. To view our polls just click the link below.\n' + str(private) + ' \n\nThank you',
                      'support@pollopine.com', [to])


def send_email_private_url_again(private, to):
    sendEmailToHumans('Private Url for Pollopine',
                      'Hello \nPrivate url for your account. '
                      'You can view/modify/delete the poll you just created'
                      'using this url. To view our polls just click the link below.\n'+ str(private) +' \n\nThank you',
                      'support@pollopine.com', [to])