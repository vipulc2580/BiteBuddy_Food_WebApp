from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage
from django.conf import settings 


def detectUser(user):
    redirectUrl=None
    if user.role==1:
        redirectUrl='vendorDashboard'
    elif user.role==2:
        redirectUrl='custDashboard'
    elif user.role==None and user.is_superadmin:
        redirectUrl='admin'
    return redirectUrl


def send_verification_email(request,user,mail_subject,htmlfile):
    from_email=settings.DEFAULT_FROM_EMAIL
    current_site = get_current_site(request)
    message = render_to_string(f'accounts/emails/{htmlfile}', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),  
        'token': default_token_generator.make_token(user),
    })
    
    # print("DEBUG: Rendered Email Content:\n", message)  # Debugging line
    # print('DEBUG ',current_site)
    to_email = user.email
    mail = EmailMessage(mail_subject, message,from_email, to=[to_email])
    mail.content_subtype = "html"  # Ensures email is sent as HTML
    mail.send()

def send_notification(mail_subject,mail_template,context):
    from_email=settings.DEFAULT_FROM_EMAIL
    message=render_to_string(mail_template,context)
    to_email=context.get('to_email')
    if isinstance(to_email,str):
        to_email=[to_email]
    mail=EmailMessage(mail_subject,message,from_email,to=to_email)
    mail.content_subtype = "html"
    mail.send()