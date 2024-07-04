from typing import Any

from django.views.generic.base import TemplateView
from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.contrib.auth.decorators import login_required


from store.models import comic

from .forms import ContactForm,NewsletterForm
from .webApp_helpers import get_featured_cache



    
class HomePageView(TemplateView):
    """
    The main home page view showing popular comics filtered by purchases and
    featured comics. The featured comics and recently bought comics are stored in the
    memory cache. 
    """
    model = comic
    template_name = "webApp/home.html"
    
    def get_context_data(self, **kwargs: Any):
        context = super().get_context_data(**kwargs)

        featured_comics = get_featured_cache()['featured_comics'] 
        comic_popular_queryset = comic.get_popular_comics(4)

        form = NewsletterForm(initial={'name': self.request.user.username,'email':self.request.user.email}) if self.request.user.is_authenticated else NewsletterForm()

        context.update({
            'featured_comics':featured_comics,
            'popular_comics':comic_popular_queryset,
            'form':form
        })

        return context
    
    def post(self,request):
        form = NewsletterForm(request.POST)
        if form.is_valid():
            form.save()
            form.send_test_mail()

            messages.success(request,"Thankyou for signing up!")
            return redirect('comicMain:comic-home') 
        else:
            messages.warning(request,"You have already signed up for the newsletter!")
            return redirect('comicMain:comic-home')
         

@login_required(login_url='login') 
def contact(request):
    """
    View for contact form, presets the field of username and email based on user details
    """

    form = ContactForm()
    form.fields['name'].initial = request.user.username
    form.fields['email'].initial = request.user.email
    
    if request.method == "POST":
        form = ContactForm(request.POST)
        
        if form.is_valid():
            form.send_mail()
            messages.success(request,"Your request has been successfuly sent")
            return redirect('comicMain:contact')
        else:
            messages.warning(request,'There was an error submitting your message')
            return redirect('comicMain:contact')
    
    return render(request,'webApp/contact.html',{'form':form})
            


    