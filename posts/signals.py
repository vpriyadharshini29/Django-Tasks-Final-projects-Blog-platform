from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile, Post, Subscriber


@receiver(post_save, sender=User)
def create_profile_for_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=Post)
def notify_subscribers_on_new_post(sender, instance, created, **kwargs):
    if created:
        emails = list(Subscriber.objects.values_list("email", flat=True))
        if emails:
            subject = f"New blog post: {instance.title}"
            msg = (
                f"Hi!\n\nA new blog post was published by {instance.author}.\n\n"
                f"Title: {instance.title}\n"
                f"Read here: "
                f"{settings.ALLOWED_HOSTS[0] if settings.ALLOWED_HOSTS else 'http://localhost:8000'}{instance.get_absolute_url()}\n\nEnjoy!"
            )
            send_mail(subject, msg, settings.DEFAULT_FROM_EMAIL, emails, fail_silently=True)
