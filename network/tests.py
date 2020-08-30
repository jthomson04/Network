from django.test import TestCase, LiveServerTestCase
from .models import User, Post
from time import sleep
from selenium import webdriver

# Create your tests here.
class BrowserTests(LiveServerTestCase):
    def setUp(self):
        self.selenium = webdriver.Chrome()
        super(BrowserTests, self).setUp()
    def test_title(self):
        selenium = self.selenium
        selenium.get('http://127.0.0.1:8000/')
        self.assertEqual(selenium.title, 'Social Network') 
        
    def tearDown(self):
        self.selenium.quit()
        super(BrowserTests, self).tearDown()



class ServerTests(TestCase):
    def setUp(self):
        #  Create users
        john = User.objects.create_user(username='jthomson', email="jthomson@yahoo.com", password='pass')
        elon = User.objects.create_user(username='elonmusk', email="elonmusk@spacex.com", password='pass')
        homie = User.objects.create_user(username='homie', email="homie@homie.com", password='pass')
        john.save()
        elon.save()
        homie.save()
        
        # Set followers 
        john.following.add(elon, homie);
        elon.following.add(homie);
        homie.following.add(elon);

        #Create Posts
        p1 = Post.objects.create(posting_user=john, content='this is a post')
        p1.likes.add(elon)

        p2 = Post.objects.create(posting_user=elon, content='rockets are cool')
        p2.likes.add(john, homie)

        p3 = Post.objects.create(posting_user=john, content='elon is cool')
        p3.likes.add(elon)

    def test_get_user_posts(self):
        '''given a user, get all posts from the user'''
        john = User.objects.get(username='jthomson')
        self.assertEqual(john.posts.count(), 2)

    def test_get_liked_posts(self):
        '''given a user, get their liked posts'''
        elon = User.objects.get(username='elonmusk')
        self.assertEqual(elon.liked_posts.count(), 2)
    
    def test_get_likes_on_post(self):
        '''given a post, get users who liked the post'''
        post = Post.objects.get(content='rockets are cool')
        self.assertEqual(post.likes.count(), 2)
    def test_get_followers(self):
        '''given a user, get the users followers'''
        john = User.objects.get(username='jthomson')
        self.assertEqual(john.followers.count(), 0)