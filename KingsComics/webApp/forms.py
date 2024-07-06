from django import forms
from django.core.validators import EmailValidator
from django.core.mail import send_mail

from crispy_forms.helper import FormHelper

from .models import Newsletter


class ContactForm(forms.Form):
    name = forms.CharField(max_length=20,label='Name',required=True,widget=forms.TextInput(attrs={'readonly':'readonly','class':'form-input contact-input'}))
    email = forms.EmailField(validators=[EmailValidator],label='Email',required=True,max_length=50,widget=forms.EmailInput(attrs={'readonly':'readonly', 'class':'form-input contact-input'}))
    subject = forms.CharField(max_length=50,label='Subject',widget= forms.TextInput(attrs={'class':'form-input contact-input'}))
    content = forms.CharField(label='Message',widget=forms.Textarea(attrs={'class':'form-control form-input contact-input','autocomplete':'off','placeholder':'Put your message here','maxlength':'400'}),required=True)

    def send_mail(self):
        
        subject = self.cleaned_data['subject']
        content = self.cleaned_data['content']
        sender = self.cleaned_data['email']
        send_mail(
            subject,
            content,
            sender,
            ['example_email@gmail.com']    
        )
    
    
class NewsletterForm(forms.ModelForm):

    name = forms.CharField(max_length=20,required=True,widget=forms.TextInput(attrs={'class':'newsletter-input newsletter-name','placeholder':'ENTER NAME'}))
    email = forms.EmailField(validators=[EmailValidator],required=True,max_length=100,widget = forms.EmailInput(attrs={'class':'newsletter-input newsletter-email','placeholder':'ENTER EMAIL'}))    

    class Meta:
        model = Newsletter
        fields=['name','email']
        

    def __init__(self, *args,**kwargs): 
        super().__init__(*args,**kwargs)
        self.helper = FormHelper()
        self.helper.form_show_labels = False

    
    def user_exists(self) -> bool:
        return Newsletter.objects.filter(email=self.cleaned_data['email']).exists()
    
    def send_test_mail(self)-> None:
        name,email = self.cleaned_data['name'],self.cleaned_data['email']
        subject = "Registering for Kings Comics Newsletter!"
        message = f"Hi {name},\nThankyou for registering for Kings Comics Newsletter.\nThis is a test email."
        send_mail(
            subject=subject,
            message=message,
            from_email='example_email@gmail.com',
            recipient_list=[email]
        )

        
    

        