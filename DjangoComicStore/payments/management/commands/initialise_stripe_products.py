from store.models import comic
from django.core.management.base import BaseCommand

import os
import stripe

STRIPE_API_PRIVATE_KEY = os.environ.get('STRIPE_API_PRIVATE_KEY')
STRIPE_API_PUBLISHABLE_KEY = os.environ.get("STRIPE_API_PUBLISHABLE_KEY")

stripe.api_key = STRIPE_API_PRIVATE_KEY

class Command(BaseCommand):
    
    
    """
    INITIALISE_STRIP_PRODUCTS COMMAND
    - Initialises stripe product id's
    - NOTE: Ensure to run "initialise_strip_price.py" after initialising product id's  
    """

    help = "Update Stripe Product IDs for existing comics"
    
    def handle(self, *args,**options):
        comics_without_stripe_id = comic.objects.filter(stripe_id =None)

        for Comic in comics_without_stripe_id:
            stripe_product = stripe.Product.create(
                name = Comic.title,
                type = 'good',
            )
            
            Comic.stripe_id = stripe_product.id
            Comic.save()
            
        
        self.stdout.write(self.style.SUCCESS(f'Stripe ID updated for comics'))
        return super().handle(*args, **options)
       
