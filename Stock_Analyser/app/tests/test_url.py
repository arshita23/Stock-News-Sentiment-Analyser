from django.test import SimpleTestCase
from django.urls import reverse,resolve
from app.views import index,get_news,logout_user

class TestUrls(SimpleTestCase):
    def test_url_index_is_resolved(self):
        url=reverse('index')
        self.assertEquals(resolve(url).func,index)

    def test_url_get_news_is_resolved(self):
        url=reverse('get_news')
        self.assertEquals(resolve(url).func,get_news)

    def test_url_logout_user_is_resolve(self):
        url=reverse('logout_user')
        self.assertEquals(resolve(url).func,logout_user)