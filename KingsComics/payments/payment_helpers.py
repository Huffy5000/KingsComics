from store.models import comic
from users.models import Cart,UserProfile,CustomUser
from django.shortcuts import get_object_or_404


def create_line_items(user_cart_contents):
    """
    Create stripe line_items used to create the checkout session
    """
    line_items = []

    for Comic in user_cart_contents:
        line_items.append({
            
            'price':Comic.stripe_price_id,
            'quantity':1
        })
    
    return line_items

def comics_from_line_items(payload):
    """
    Processes the stripe line_items payload and extracts comics
    """
    purchase_data= payload['data']
    comic_names_purchased = [item['description'] for item in purchase_data]
    comics_purchased = comic.objects.filter(title__in=comic_names_purchased)
    return comics_purchased



def user_from_stripe_checkout(stripe_customer_id):
    user = get_object_or_404(CustomUser,stripe_customer_id=stripe_customer_id)
    user_profile = get_object_or_404(UserProfile,user = user)
    user_cart = get_object_or_404(Cart, user = user)
    return user_profile,user_cart

    
    
    

    
    

    
    

    
    
