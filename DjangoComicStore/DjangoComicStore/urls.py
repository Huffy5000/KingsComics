from users import forms 
from users import views as user_views

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static 




urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('webApp.urls',namespace = 'comicMain')),
    path('store/',include('store.urls',namespace= 'storeMain')),
    
    #Auth path
    path('register/',user_views.register,name = 'register'),
    path('login/',user_views.custom_login_view,name = 'login'),
    path('logout/',user_views.logout_view,name = 'logout'),
    
    #Password reset path
    path('password_reset/',auth_views.PasswordResetView.as_view(form_class = forms.forgotPasswordEmailVal, template_name = 'users/password_reset.html'),name= 'password-reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(template_name = 'users/password_reset_done.html'),name = 'password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name = 'users/password_reset_confirm.html'),name = "password_reset_confirm"),
    path('password_reset_complete',auth_views.PasswordResetCompleteView.as_view(template_name = 'users/password_reset_complete.html'),name = 'password_reset_complete'),
    
    #Payment path
    path('checkout/',include('payments.urls',namespace = 'paymentsMain')),
    
    #Bookshelf path
    path('bookshelf/',user_views.Bookshelf.as_view(),name = 'bookshelf'),
    path('bookshelf/reader/<int:pk>/',user_views.comic_reader.as_view(),name ='bookshelf_reader'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root = settings.MEDIA_ROOT)
