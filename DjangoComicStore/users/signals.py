from django.db.models.signals import post_save
from django.contrib.auth.signals import user_logged_in,user_logged_out
from django.dispatch import receiver
from django.shortcuts import get_object_or_404

from .models import CustomUser,UserProfile,Cart
from .user_helpers import create_stripe_customer, session_cart_to_db


#On user creation create profile
@receiver(post_save,sender = CustomUser)
def create_profile(sender,instance,created,**kwargs):
    if created:
        UserProfile.objects.create(user = instance)
        customer_id = create_stripe_customer(instance)
        instance.stripe_customer_id =customer_id
        instance.save()
        
#Save profile on profile update
@receiver(post_save,sender=CustomUser)
def save_profile(sender,instance,**kwargs):
    instance.userprofile.save()

#Create cart when user is created
@receiver(post_save,sender = CustomUser)
def create_cart(sender,instance,created,**kwargs):
    if created:
        Cart.objects.create(user = instance)
    
@receiver(user_logged_in,sender = CustomUser)
def create_session_cart(sender,user,request,**kwargs):
    
    """
    Instantiate and population session cart with db cart products on login
    """
    
    cart_products = user.cart.products.all()
    cart_data = []
    
    for product in cart_products:
        product_info  = {'id':product.id,'title':product.title,'price':product.price}
        cart_data.append(product_info)
        
    request.session['cart'] = cart_data
    request.session.save()

@receiver(user_logged_in,sender = CustomUser)
def create_bookshelf(sender,user,request,**kwargs):
    """
    When user logs in instantiate bookshelf if it does not exist
    """

    user_profile= get_object_or_404(UserProfile, user = user)
    user_bookshelf =user_profile.bookshelf

    if 'comic' not in  user_bookshelf:
        user_bookshelf['comic'] = []
        user_profile.save()
       

@receiver(user_logged_out,sender=CustomUser)
def save_session_cart(sender,request,**kwargs):
    """
    Add comics in session cart to database if they do not exist
    """
    session_cart= request.session['cart']
    user_cart:Cart = get_object_or_404(Cart,user = request.user)

    session_cart_to_db(session_cart,user_cart)

    request.session['cart'] = []
    request.session.save()

            
            