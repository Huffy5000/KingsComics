from typing import Any

from .models import comic

from users.models import Cart,UserProfile
from users.user_helpers import session_cart_to_db


from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import ListView,DetailView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404
from django.contrib import messages

class StoreListView(ListView):
    """
    Main store page view, context data gets list of comics and uses for loop in template to show comics
    """
    model = comic
    
    template_name = "store/store_home.html"
    
    context_object_name = "comicList"

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        
        context = super().get_context_data(**kwargs)
        search_request = self.request.GET.get('search')
        if search_request in [' ',"",None,"Search by title"]: 
            context['comics'] =comic.objects.all()
        else:
            context['comics'] = comic.objects.filter(title__icontains=search_request)
        
        return context




class ProductDetailView(DetailView):
    model = comic

    def get_context_data(self, **kwargs: Any): 
        context = super().get_context_data(**kwargs)

        #Detailed comic can be accessed from home or store page
        if 'HTTP_REFERER' in self.request.META.keys() and 'store' not in self.request.META['HTTP_REFERER']:
            context['back_url'] = reverse('comicMain:comic-home')
        else:
            context['back_url'] = reverse('storeMain:store-home')

        return context

    

class AddToCart(LoginRequiredMixin,View):
    
    #Get function to prevent url access to page
    def get(self,*args,**kwargs):
        return redirect('storeMain:store-home')
    
    def post(self,request,*args,**kwargs):
        """
        Adds comics to session cart upon post request 
        """ 
       
        comic_data= get_object_or_404(comic,pk = kwargs['pk']).generate_comic_data()
        user_bookshelf = get_object_or_404(UserProfile,user = request.user).bookshelf['comic']
        user_cart = get_object_or_404(Cart,user = request.user)
        session_cart:list = request.session['cart']
        
        if (comic_data in session_cart) or user_cart.is_comic_in_cart(comic_data['id']):
            messages.warning(request,"This item is already in your cart")
        elif comic_data['title'] in user_bookshelf:
            messages.warning(request,'This item is already in your bookshelf')
        else:
            session_cart.append(comic_data)
            request.session.save()
         
        return redirect('storeMain:store-detail',comic_data['id'])
        
class ViewCart(LoginRequiredMixin,ListView):
    """
    Add all products from session cart into db cart 
    """

    model =Cart
    
    def get(self, request, *args, **kwargs):
        
        try:
            session_cart = request.session['cart']
        except KeyError as e:
            print(f'Session cart not found: {e}')
            request.session['cart'] = []
            request.session.save()
            
        user_cart = get_object_or_404(Cart,user = request.user)   

        session_cart_to_db(session_cart,user_cart)

        request.session['cart'] = []
        request.session.save()
        
        return super().get(request, *args, **kwargs)
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)
        user_cart = get_object_or_404(Cart,user = self.request.user)
        context['cart'] = user_cart.products.all()
        return context
        
    template_name = 'store/cart.html'
    context_object_name = 'object'


class RemoveItem(LoginRequiredMixin,View):
    """
    View to remove items in the cart 
    """ 

    def post(self,request,*args,**kwargs):
        
        comic_id = kwargs['pk']
        user_cart = get_object_or_404(Cart,user = request.user)
        user_cart.remove_from_cart(comic_id)
        return redirect('storeMain:view-cart')


            