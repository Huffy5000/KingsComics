from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(unique = True)
    stripe_customer_id = models.CharField(max_length = 300,blank = True,null = True)

    def __str__(self) -> str:
        return self.username

    
class UserProfile(models.Model):
    user = models.OneToOneField(CustomUser,on_delete = models.CASCADE)

    #Default is a dict, bookshelf is stored as ={'comic':[List of comics]} 
    bookshelf = models.JSONField(default =dict)
    
    def __str__(self) -> str: 
        return f'{self.user.username} Profile'
    
    def list_all_comics(self):
        comic_list = [i for i in self.bookshelf['comic']]
        return comic_list
    
    def list_all_comic_ids(self):
        comic_id_list = [i['id'] for i in self.bookshelf['comic']]
        return comic_id_list
            
class Cart(models.Model):
    user = models.OneToOneField(CustomUser,on_delete=models.CASCADE)
    products = models.ManyToManyField('store.comic')

    def list_comic_ids(self):
        comic_id_list = self.products.values_list('id',flat=True)
        return comic_id_list
    
    def is_comic_in_cart(self,pk):
        return self.products.filter(id = pk).exists()
        
    def remove_from_cart(self,comic_id:int)->None:
        comic_to_delete = self.products.filter(id = comic_id)
        if comic_to_delete:
            self.products.remove(comic_to_delete)
            self.save()

    def __str__(self) -> str:
        comicList = [comic.title for comic in self.products.all()]
        return f"User has {len(comicList)} items in cart, {comicList}" 
    
    