import os
import stripe 

from store.models import comic

from django.http import HttpResponse


STRIPE_API_PRIVATE_KEY = os.environ.get('STRIPE_API_PRIVATE_KEY')
STRIPE_API_PUBLISHABLE_KEY = os.environ.get("STRIPE_API_PUBLISHABLE_KEY")
stripe.api_key = STRIPE_API_PRIVATE_KEY

def create_stripe_customer(user):
    try: 
        customer_data= stripe.Customer.create(
            name=user.username,
            email = user.email
        )
    except stripe.InvalidRequestError as e:
        print(f"There was a problem with the request: {e}")
        return HttpResponse(status=400)
    except (stripe.APIConnectionError,stripe.AuthenticationError,stripe.PermissionError) as e:
        print(f"There was a problem with the service. Please try again soon.{e}")
        return HttpResponse(status=500)

    customer_id = str(customer_data['id'])
    return customer_id
        
    
def session_cart_to_db(session_cart,user_cart)->None:

    session_cart_comics = {Comic['id'] for Comic in session_cart}
    user_cart_comics = set(user_cart.list_comic_ids())

    comics_to_add_id = session_cart_comics-user_cart_comics
    comics_to_db = comic.objects.filter(id__in = comics_to_add_id)

    user_cart.products.add(*comics_to_db)
    user_cart.save()



def get_comic_pdf_path(pk:int)->str:
    """
    Return url for pdf for comic with pk 
    """
    
    key = pk-8
    pdf_List = [
        "Insert list of urls for comic pdf's here"
    ]

    return pdf_List[key]

