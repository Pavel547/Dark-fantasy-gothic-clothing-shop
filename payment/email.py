# Note
# SMTP is used only for development.
# In production, emails are sent via Resend
# API due to hosting SMTP restrictions. 

from django.core.mail import EmailMultiAlternatives
import resend
from django.template.loader import render_to_string
from django.conf import settings
from orders.models import Order, OrderItem
from django.db.models import Prefetch
from smtplib import SMTPException
import logging

logger = logging.getLogger(__name__)

resend.api_key = settings.RESEND_API_KEY

# Send email in dev
def send_via_smtp(order, text_content, html_content):
    try:
        msg = EmailMultiAlternatives(
            'Payment confirmation',
            text_content,
            settings.EMAIL_HOST_USER,
            [order.email]
        )
        msg.attach_alternative(html_content, 'text/html')
        msg.send()
        logger.info(f"Confirmation email for order {order.id} was sent")
    except SMTPException as e:
        logger.error(f"Failed to send confirmation email for order {order.id}: {e}")

# Send email in prod   
def send_via_resend(order, html_content):
    try:
        resend.Emails.send({
            'from': 'onboarding@resend.dev',
            'to': order.email,
            'subject': 'Payment confirmation',
            'html': html_content,
        })
    except Exception as e:
        logger.error(f'Resend failed for order {order.id}: {e}')

def confirmation_order_email(order_id):
    try:
        order = Order.objects.prefetch_related(
            Prefetch(
                'items',
                queryset=OrderItem.objects.select_related(
                    'product', 'product_size__size'
                )
            )
        ).get(id=order_id)
    except Order.DoesNotExist:
        logger.error(f'Order {order_id} not found')
    
    context = {'order': order}
    
    text_content = render_to_string('email/order_confirmation.txt', context)
    html_content = render_to_string('email/order_confirmation.html', context)
    
    if settings.DEBUG:
        send_via_smtp(order, text_content, html_content)
    else:
        send_via_resend(order, html_content)
    