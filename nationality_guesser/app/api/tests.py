from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from django.urls import reverse

from app.api.models import Country, NameNationality


class NameNationalityTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.country = Country.objects.create(
            country_code="US",
            name="United States",
            full_name="United States of America",
            region="Americas",
            is_independent=True,
        )
        self.name_nationality = NameNationality.objects.create(
            name="John", country=self.country, probability=0.75, count=10
        )

    def test_get_nationality_with_existing_name(self):
        url = reverse("names") + "?name=John"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["name"], "John")


class PopularNamesTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.country = Country.objects.create(
            country_code="US",
            name="United States",
            full_name="United States of America",
            region="Americas",
            is_independent=True,
        )
        NameNationality.objects.create(
            name="John", country=self.country, probability=0.75, count=10
        )
        NameNationality.objects.create(
            name="Maria", country=self.country, probability=0.65, count=8
        )

    def test_get_popular_names_with_valid_country(self):
        url = reverse("popular-names") + "?country=US"
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
