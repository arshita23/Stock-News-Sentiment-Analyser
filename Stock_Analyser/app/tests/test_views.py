from django.test import TestCase, Client
from django.urls import reverse

class TestViews(TestCase):

    def test_index_post(self):
        client=Client()
        response=client.post(reverse('index'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'login.html')

    def test_get_news(self):
        client=Client()
        response=client.post(reverse('get_news'))
        self.assertEquals(response.status_code,302)