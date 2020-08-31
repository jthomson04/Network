from django.test import TestCase, Client
from .models import User, Post
from django.urls import reverse
# Create your tests here.
class BrowserTests(TestCase):
    def setUp(self):
        john = User.objects.create_user(username='jthomson', email='jthomson@yahoo.com', password='pass')
        fred = User.objects.create_user(username='fred', email='fred@fred.com', password='pass')
        bob = User.objects.create_user(username='bob', email='bob@bob.com', password='pass')
        john.save()
        fred.save()
        bob.save()
        # Add 27 posts to test pagination
        for i in range(27):
            Post.objects.create(posting_user=john, content=f'this is post {i}')

    def test_index(self):
            c = Client()
            # Checks for first page
            response = c.get(reverse('index') + f'?pagenum={1}')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['items']), 10)
            self.assertEqual(response.context['pagenum'], 1)
            self.assertEqual(len(response.context['pages']), 3)
            self.assertEqual(response.context['firstpage'], True)
            self.assertEqual(response.context['lastpage'], False)
            self.assertEqual(response.context['userpage'], False)
            self.assertEqual(response.context['title'], 'All Posts')
            # Checks for negative and invalid pages
            response = c.get(reverse('index') + '?pagenum=-3')
            self.assertEqual(response.status_code, 404)
            response = c.get(reverse('index') + '?pagenum=19')
            self.assertEqual(response.status_code, 404)
            response= c.get(reverse('index') + '?pagenum=yeet')
            self.assertEqual(response.status_code, 404)

            # Checks for last page
            response = c.get(reverse('index') + '?pagenum=3')
            self.assertEqual(response.status_code, 200)
            self.assertEqual(len(response.context['items']), 7)
            self.assertEqual(response.context['firstpage'], False)
            self.assertEqual(response.context['lastpage'], True)

    def test_userpage(self):
        c = Client()
        response = c.get(reverse('viewuser', args=('jthomson',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['userpage'], True)
        self.assertEqual(response.context['title'], 'jthomson')
    
    def test_followers_following(self):
        c = Client()
        john = User.objects.get(username='jthomson')
        fred = User.objects.get(username='fred')
        bob = User.objects.get(username='bob')
        john.following.add(fred, bob)
        john.followers.add(bob)
        response = c.get(reverse('viewuser', args=('jthomson',)))
        self.assertEqual(response.context['followers'], 1)
        self.assertEqual(response.context['following'], 2)

    def test_follow_unfollow(self):
        c = Client()
        self.assertEqual(c.login(username='jthomson', password='pass'), True)
        j = User.objects.get(username='jthomson')
        self.assertEqual(j.following.count(), 0)

        j.following.add(User.objects.get(username='bob'))

        response = c.get(reverse('viewuser', args=('bob',)))
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['title'], 'bob')
        self.assertEqual(response.context['user_follows'], True)
        
        response = c.get(reverse('viewuser', args=('fred',)))
        self.assertNotEqual(response.context['user_follows'], None)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.context['userpage'], True)
        self.assertEqual(response.context['user_follows'], False)





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