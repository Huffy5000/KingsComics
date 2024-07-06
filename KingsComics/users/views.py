from typing import Any

from django.contrib import messages
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView,TemplateView

from store.models import comic

from .forms import RegistrationForm,LoginForm
from .models import UserProfile
from .user_helpers import  get_comic_pdf_path




def register(request):
    """
    Register the user if they are not currently logged in
    """
    if request.user.is_authenticated:
        return redirect('comicMain:comic-home')

    if request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form =RegistrationForm()
            
    return render(request,'users/register.html',{'form':form})
            

def logout_view(request):

    if request.user.is_authenticated:
        logout(request)
    
    return redirect('comicMain:comic-home')
    
    
def custom_login_view(request):
    if request.user.is_authenticated:
        return redirect('comicMain:comic-home')
    else:
        return LoginView.as_view(template_name='users/login.html',authentication_form=LoginForm)(request)
    
    
class Bookshelf(LoginRequiredMixin,ListView):

    model = UserProfile
    template_name = "users/bookshelf.html"
    

    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        user_profile = get_object_or_404(UserProfile,user = self.request.user)
        
        context = super().get_context_data(**kwargs)
        
        owned_comics = comic.objects.filter(title__in = user_profile.list_all_comics())
        context['bookshelf'] = owned_comics
        return context
    

class comic_reader(LoginRequiredMixin,TemplateView):
    """
    View for reading comic if in users bookshelf
    """
    model = comic
    template_name = "users/comic_reader.html"
    
    
    def get(self, request: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        
        pk = kwargs['pk']
        comic_title = get_object_or_404(comic,id = pk).title
        user_bookshelf = get_object_or_404(UserProfile,user = request.user).bookshelf['comic']

        if comic_title not in user_bookshelf:
            messages.warning(request,"This comic is not in your bookshelf. Please purchase the comic first")
            return redirect('storeMain:store-detail',pk = pk)
        else:
            return super().get(request, *args, **kwargs)
        
    def get_context_data(self, **kwargs: Any) -> dict[str, Any]:
        """
        Gets data required for the reader function to work.
        """

        pk = kwargs['pk']
        context = super().get_context_data(**kwargs)
        context['Comic'] = get_object_or_404(comic,id = pk)

        context['pdf'] = get_comic_pdf_path(pk) 
        return context
        
        