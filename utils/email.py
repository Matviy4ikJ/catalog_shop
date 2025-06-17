from django.shortcuts import render, redirect
from products.models import Cart, Product, Order
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib import messages
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest
from django.conf import settings


def sent_email_confirm(request, user, new_email):
    confirm_url = request.build_absolute_uri(reverse('account:confirm_email'))
    confirm_url += f'?user={user.id}&email={new_email}'

    subject = 'Confirm email'

    message = f'Hello {user.username} wanna change your email? ' \
              f'To confirm this operation, click on this link {confirm_url}'

    send_mail(
        subject, message, 'noreplay@gmail.com', [new_email], fail_silently=False
    )

    messages.info(request, 'Confirmation mail was sent')


def sent_order_confirmation_email(order: Order):
    subject = f'Confirmation order {order.id}'
    context = {'order': order}
    text_content = render_to_string('email/confirmation_email.txt', context)
    to_email = order.contact_email
    
    try:
        send_mail(
            subject,
            text_content,
            'noreply@gmail.com',
            [order.contact_email],
            fail_silently=False,
        )
    except Exception as e:
        print(f"Failed to send confirmation email: {e}")
