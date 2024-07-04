from store.models import comic
from django.core.management.base import BaseCommand


from typing import Any
import stripe
import os

STRIPE_API_PRIVATE_KEY = os.environ.get('STRIPE_API_PRIVATE_KEY')
STRIPE_API_PUBLISHABLE_KEY = os.environ.get("STRIPE_API_PUBLISHABLE_KEY")

stripe.api_key = STRIPE_API_PRIVATE_KEY

class Command(BaseCommand):
    
    """
    INITIALISE_STRIP_PRICE COMMAND
    - Initialises the stripe price id's for each product in the database
    - NOTE: Only run after product id's have been created, see "initialise_stripe_products.py"
    """

    help = "Updating stripe price Id's for existing comics"
    
    def handle(self, *args: Any, **options: Any):
        comics_without_price_id = comic.objects.filter(stripe_price_id = None)
        
        for Comic in comics_without_price_id:
            stripe_price = stripe.Price.create(
                product=Comic.stripe_id,
                unit_amount = int(Comic.price*100),
                currency="aud",
            )
        
            Comic.stripe_price_id = stripe_price.id
            Comic.save()
        
        self.stdout.write(self.style.SUCCESS(f'Stripe PRICE ID updated for comics'))
        return super().handle(*args, **options)