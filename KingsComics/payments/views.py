from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages

from .payment_helpers import comics_from_line_items,create_line_items,user_from_stripe_checkout
import stripe.error
from users.models import Cart

import os 
import stripe

STRIPE_API_PRIVATE_KEY = os.environ.get('STRIPE_API_PRIVATE_KEY')
STRIPE_API_PUBLISHABLE_KEY = os.environ.get("STRIPE_API_PUBLISHABLE_KEY")

stripe.api_key = STRIPE_API_PRIVATE_KEY
endpoint_secret = str(os.environ.get('KINGSCOMICS_ENDPOINT_SECRET'))

@login_required
def create_checkout_session(request):
    """
    View to create stripe hosted checkout session
    """

    user_cart_contents = get_object_or_404(Cart,user=request.user).products.all()
    stripe_customer_id = request.user.stripe_customer_id

    if user_cart_contents.count() <1:
        messages.warning(request,"Your cart is currently empty, cannot proceed to payment")
        return redirect('storeMain:store-home')
     
    try:
        line_items = create_line_items(user_cart_contents) 

        checkout_session = stripe.checkout.Session.create(
            line_items=line_items,
            mode = 'payment',
            success_url="http://127.0.0.1:8000/checkout/payment_success/",
            cancel_url="http://127.0.0.1:8000/checkout/payment_cancelled/",
            customer=stripe_customer_id,
        )
    except stripe.InvalidRequestError as e:
        print(f"There was a problem with the request: {e}")
        return HttpResponse(status=400)
    except (stripe.APIConnectionError,stripe.AuthenticationError,stripe.PermissionError) as e:
        print(f"There was a problem with the service. Please try again soon.{e}")
        return HttpResponse(status=500)
    
    return redirect(checkout_session.url)

@csrf_exempt
def payment_successful_webhook(request):
    payload = request.body
    sig_header = request.META['HTTP_STRIPE_SIGNATURE']
    event=None

    try:
        event = stripe.Webhook.construct_event(
            payload,sig_header,endpoint_secret
        )

    except ValueError as e:
        #Invalid payload
        print(f'Error with payload {str(e)}')
        return HttpResponse(status=400)

    except stripe.SignatureVerificationError as e:
        #Invalid signature
        print(f'Error verifying signature: {str(e)}')
        return HttpResponse(status=400)
        
    except stripe.InvalidRequestError as e:
        print(f"There was a problem with the request: {e}")
        return HttpResponse(status=400)

    except (stripe.APIConnectionError,stripe.AuthenticationError,stripe.PermissionError) as e:
        print(f"There was a problem with the service. Please try again soon.{e}")
        return HttpResponse(status=500)

    data = event.data.object

    if event['type']=='checkout.session.completed':
        try:
            session = stripe.checkout.Session.retrieve(
                data['id'],
                expand=['customer']
            )
        except Exception as e:
            print(e) 

        customer_id = session.customer['id']
        line_items = session.list_line_items(limit=100)

        user_profile,user_cart = user_from_stripe_checkout(customer_id)
        user_bookshelf = user_profile.bookshelf['comic']

        comics_purchased= comics_from_line_items(line_items)

        for Comic in comics_purchased:
            user_bookshelf.append(Comic.title)
            Comic.purchases+=1
            Comic.save()
            
        user_cart.products.clear()
        user_profile.save()
        user_cart.save()
        

    return HttpResponse(status=200)



    
@login_required
def payment_success(request):
    return render(request,'payments/payment_success.html')
    
@login_required
def payment_cancelled(request):
    return render(request,'payments/payment_cancelled.html')

