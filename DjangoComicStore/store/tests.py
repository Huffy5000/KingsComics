from django.test import TestCase
from users.models import CustomUser,Cart
from store.models import comic
from datetime import datetime as dt 
from django.urls import reverse
from django.contrib.messages import get_messages



class StoreViewsTest(TestCase):
   
    @classmethod
    def setUpTestData(cls) -> None:

        test_user = CustomUser.objects.create(username='teststoreuser',email='teststoreuser@test.com')
        test_user.set_password('secret123') 
        test_user.save()
        
        test_date = dt.strftime(dt.now(),r"%Y-%m-%d")
        comic.objects.create(title = 'TestStoreComic',release_date=test_date,company='TestComicCompany',price=3.99)
        cls.comic_data = {'id':1,'title':'TestStoreComic','price':3.99}

    def test_add_to_cart_success(self):
        self.client.login(username='teststoreuser',password='secret123')

        #GET shouldnt work on add cart method
        response = self.client.get('/store/comic/add_cart/1')
        self.assertEqual(response.status_code,301,'GET request redirection on add to cart not working')
        
        #POST to session cart
        self.client.post(reverse('storeMain:add-cart',kwargs={'pk':'1'}))
        session = self.client.session
        self.assertIn(self.comic_data,session['cart'],"The comic is not in the session cart")

        #View cart puts session cart in db
        response = self.client.get(reverse('storeMain:view-cart'))
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'store/cart.html')

        user_cart = Cart.objects.get(user = CustomUser.objects.get(username='teststoreuser'))
        self.assertEqual(user_cart.products.first().title,self.comic_data['title'])
    
    def test_add_to_cart_fail(self):
        #Test if user can add to cart if already exists
        testUserCart = Cart.objects.get(user=CustomUser.objects.get(username ='teststoreuser'))
        testUserCart.products.add(comic.objects.get(id=1))
        testUserCart.save()

        self.client.login(username='teststoreuser',password='secret123')
        response = self.client.post(reverse('storeMain:add-cart',kwargs={'pk':'1'}))
        messages = list(get_messages(response.wsgi_request))
        
        self.assertEqual(len(messages),1,"Unescessary messages beign displayed")
        self.assertEqual(str(messages[0]),"This item is already in your cart","Duplicate item detection not working")
    
    #Remove from cart tests
    def test_remove_from_cart_get(self):
        self.client.login(username='teststoreuser',password='secret123')

        #GET shouldnt work on add cart method
        response = self.client.get(reverse('storeMain:remove-item',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,301,'GET request redirection on add to cart not working')

        response = self.client.get(reverse('storeMain:remove-item',kwargs={'pk':'1'}),follow=True)
        self.assertEqual(response.status_code,200,"Redirection from GET remove item not working")
        self.assertTemplateUsed(response,'store/store_home.html',"Remove cart get incorrect redirection template")

    def test_remove_from_cart_fail(self):
        self.client.login(username='teststoreuser',password='secret123')
        
        #Remove non-existent item from cart 
        response = self.client.post(reverse('storeMain:remove-item',kwargs={'pk':'1'}))
        self.assertEqual(response.status_code,404,"Removing non-existent item did not work")
    
    def test_remove_from_cart_success(self):
        self.client.login(username='teststoreuser',password='secret123')

        #Remove existing item from cart
        user_cart = Cart.objects.get(user=CustomUser.objects.get(username='teststoreuser'))
        user_cart.products.add(comic.objects.get(id=1))
        user_cart.save()

        response = self.client.post(reverse('storeMain:remove-item',kwargs={'pk':'1'}),follow=True)
        self.assertEqual(response.status_code,200,"Removal of item from cart failed")
        self.assertTemplateUsed(response,'store/cart.html',"Incorrect template used on successful cart item removal redirection")

        empty_cart = user_cart.products.first()
        self.assertEqual(empty_cart,None,'Comic was not removed from cart')


        
        
        
        

        
        
        
        
        