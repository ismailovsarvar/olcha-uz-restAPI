from django.conf import settings
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from rest_framework.authtoken.models import Token
from django.core.cache import cache
from olchauz.models import Product


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Product)
def invalidate_product_cache(sender, instance, **kwargs):
    cache_key = f'product_detail_{instance.slug}'
    cache.delete(cache_key)

    cache.delete('product_list')


@receiver(post_delete, sender=Product)
def invalidate_product_cache_on_delete(sender, instance, **kwargs):
    # Invalidate the cache for the specific product
    cache_key = f'product_detail_{instance.slug}'
    cache.delete(cache_key)

    # Optionally, invalidate cache for any related lists or pages
    cache.delete('product_list')

