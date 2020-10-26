from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import json


class VesselTestCase(TestCase):
    # Helper functions
    def get(self, url):
        return self.client.get(url)

    def post(self, url, payload):
        return self.client.post(url, payload,
                                content_type="application/json")

    def put(self, url, payload):
        return self.client.put(url, payload,
                               content_type="application/json")

    def test_url_root(self):
        """Checks if root url is accessible"""
        url = reverse('index')
        response = self.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_url_vessel_empty_list(self):
        """Checks if a empty list is returned"""
        url = reverse('vessel-list')
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vessel_invalid_input(self):
        """Checks invalid input on creating vessel"""
        url = reverse('vessel-create')
        payload = json.dumps({
            "code2": "MV101"
        })
        response = self.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_url_create_vessel(self):
        """Execute helper tests in the right order of execution"""
        self.helper_test_create_vessel()
        self.helper_test_create_vessel_duplicated()
        self.helper_test_vessel_non_empty_list()

    # helpers tests ==========================================================
    def helper_test_create_vessel(self):
        """Checks if create vessel is successfully"""
        url = reverse('vessel-create')
        payload = json.dumps({
            "code": "MV101"
        })
        response = self.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def helper_test_create_vessel_duplicated(self):
        """Checks duplicated vessel validation"""
        url = reverse('vessel-create')
        payload = json.dumps({
            "code": "MV101"
        })
        response = self.post(url, payload)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def helper_test_vessel_non_empty_list(self):
        """Checks if a non-empty list is returned"""
        url = reverse('vessel-list')
        response = self.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = json.loads(response.content)
        is_empty = True
        if type(json_data) == list:
            is_empty = len(json_data) == 0

        self.assertEqual(is_empty, False)
