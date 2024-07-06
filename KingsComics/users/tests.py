from django.test import TestCase
from datetime import datetime as dt 

from .models import CustomUser,UserProfile,Cart

from store.models import comic


class UserModelTest(TestCase):
   
    @classmethod
    def setUpTestData(cls) -> None:
        CustomUser.objects.create(username = 'TestUser1',email='TestUser1@test.com',password = 'testuser1password')
        test_date = dt.strftime(dt.now(),r"%Y-%m-%d")
        comic.objects.create(title = 'TestComic',release_date=test_date,company='TestComicCompany',price=3.99)

    def test_profile(self):
        TestUser1 = CustomUser.objects.get(id=1)
        self.assertEqual(str(TestUser1),"TestUser1")

        TestUser1Profile = UserProfile.objects.get(user = TestUser1)
        self.assertEqual(str(TestUser1Profile),"TestUser1 Profile","__str__ Not working as intended") 
    
    def test_default_bookshelf(self):                
        TestUser1 = CustomUser.objects.get(id=1)
        TestUser1Bookshelf = UserProfile(user = TestUser1).bookshelf

        self.assertEqual(TestUser1Bookshelf,{},"Default Bookshelf not assigned properly")
    
    def test_user_cart(self):
        
        TestUser1 = CustomUser.objects.get(id=1)
        TestCart1 = Cart.objects.get(user = TestUser1)

        self.assertEqual(len(TestCart1.products.all()),0,"Default cart is not empty")

        TestCart1.products.add(comic.objects.get(id=1))

        self.assertEqual(len(TestCart1.products.all()),1,"Adding an item to the cart did not work")
        self.assertEqual(TestCart1.products.get(id=1),comic.objects.get(id=1),"The comic in the cart is not correct")
        self.assertEqual(str(TestCart1),"User has 1 items in cart, ['TestComic']")

 

        
class UserViewsTest(TestCase):

    @classmethod
    def setUp(cls) -> None:
        test_user = CustomUser.objects.create(username='testviewuser',email='testviewuser1@test.com')
        test_user.set_password('secret123') #This will hash the password before storing it, otherwise comparing unhashed to hashed
        test_user.save()
        
        test_user_2 = CustomUser.objects.create(username='testviewuser2',email='testviewuser2@test.com')
        test_user_2.set_password('secret123') 
        test_user_2.save()
        
        
        test_date = dt.strftime(dt.now(),r"%Y-%m-%d")
        comic.objects.create(title = 'TestComic2',release_date=test_date,company='TestComicCompany',price=3.99)

        test_user_profile = UserProfile.objects.get(user = test_user)
        test_user_profile.bookshelf['comic']=['TestComic2']
        test_user_profile.save()

    
    def test_bookshelf_view_load(self):
        self.client.login(username='testviewuser',password='secret123')
        response = self.client.get('/bookshelf/')
        
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'users/bookshelf.html')

    def test_contact_view_load(self):
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code,302,'The unautheticated user was not redirected accordingly')

        self.client.login(username='testviewuser',password='secret123')
        response = self.client.get('/contact/')
        self.assertEqual(response.status_code,200)
        self.assertTemplateUsed(response,'webApp/contact.html')
    
    def test_comic_reader_view_load(self):
        self.client.login(username='testviewuser',password='secret123')
        response = self.client.get('/bookshelf/reader/1/')
        
        self.assertEqual(response.status_code,200,"The comic reader view failed to load")
        self.assertTemplateUsed(response,'users/comic_reader.html')
        
        #Test book that doesnt exist
        response = self.client.get('/bookshelf/reader/2',follow=True)
        self.assertEqual(response.status_code,404,"Redirection for non-existent comic not working as intended")

    def test_comic_reader_view_fail(self):
        self.client.login(username='testviewuser2',password='secret123')
        response = self.client.get('/bookshelf/reader/1/')
        self.assertEqual(response.status_code,302,"Unowned comic redirection not working")
        self.assertTemplateNotUsed(response,'store/store_home.html')
        