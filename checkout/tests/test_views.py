from django.test import TestCase
from django.urls import reverse


class TestCheckout(TestCase):

    def setUp(self):
        self.pre_checkout_url = reverse('checkout:pre_checkout')


    def test_pre_checkout(self):
        response = self.client.get(self.pre_checkout_url + "?conditions=1")
        self.assertRedirects(response, reverse('checkout:pre_payment'))

