from django.db import models
from datetime import datetime as dt 

from typing import Any

class comic(models.Model):
    title = models.CharField(max_length = 50,unique =True)
    cover = models.ImageField(default='default.jpg')
    description = models.TextField(max_length = 300, blank = True)
    featured = models.BooleanField(default = False)
    company = models.CharField(max_length=50)
    purchases = models.PositiveIntegerField(default = 0)
    price = models.FloatField()
    release_date = models.DateTimeField()
    bundle = models.SmallIntegerField(blank = True, null = True)
    stripe_id = models.CharField(max_length = 300,blank = True,null = True)
    stripe_price_id = models.CharField(max_length = 300,blank = True, null = True)
    
    def __str__(self):
        return f'{self.title} comic. ${self.price} '
   
    def save(self,*args,**kwargs) -> None:
        
        self.price = round(float(self.price),2)

        #Save date as datetime object in format : Year-month-day 
        # release_date_obj = dt.strptime(self.release_date,r"%d-%m-%Y")
        # self.release_date = dt.strftime(release_date_obj,r"%Y-%m-%d")
        return super().save(*args,**kwargs)
    
    def generate_comic_data(self)->dict[str,Any]:
        comic_data = {'id':self.pk,'title':self.title,'price':self.price}
        return comic_data

    @classmethod
    def get_popular_comics(cls,lim:int):
        return cls.objects.filter(featured = False).order_by('-purchases')[:lim]
        
    

    