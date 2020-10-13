from django.test import TestCase
from django.urls import reverse
from rest_framework import status
import json


class EquipmentTestCase(TestCase):
    # Helper functions
    def get(self, url):
        return self.client.get(url)

    def post(self, url):
        return self.client.post(url)

    def post_json(self, url, body):
        return self.client.post(url, body,
                                content_type="application/json")

    def put(self, url, body):
        return self.client.put(url, body,
                               content_type="application/json")

    # Test cases =============================================================
    def test_url_root(self):
        """Checks if root url is accessible"""
        url = reverse('index')
        response = self.get(url)
        self.assertEqual(response.status_code,
                         status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_url_equipment_empty_list(self):
        """Checks if a empty list is returned"""
        url = reverse('equipment-list')
        response = self.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_url_create_equipment_invalid_input(self):
        """
        Checks invalid input on creating equipment
        The Location item was intentionally REMOVED so it should return
        an error
        """
        url = reverse('equipment-create', kwargs={'vessel_code': 'MV404'})
        body = json.dumps({
            "code": "5310B9D7",
            "name": "compressor"
        })
        response = self.put(url, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_url_equipment_update_invalid_input(self):
        """Checks invalid input on equipment update"""
        url = reverse('equipment-update')
        body = json.dumps([
            {
                "code2": "5310B9D8",
                "status": "inactive"
            }
        ])
        response = self.post_json(url, body)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_url_equipment_update_list(self):
        """Test equipment update with a list as input"""
        self.helper_test_create_equipment_successfully(
            vessel_code="MV555", equip_code="A0000000"
        )
        url = reverse('equipment-update')
        body = json.dumps([
            {
                "code": "A0000000",
                "status": "inactive"
            }
        ])
        response = self.post_json(url, body)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_equipment_update_inexistence(self):
        """Test update error when equipment doesn't exists"""
        url = reverse('equipment-update')
        body = json.dumps([
            {
                "code": "X0000000",
                "status": "active"
            }
        ])
        response = self.post_json(url, body)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_url_create_equipment(self):
        """Execute helper tests in the right order of execution"""
        self.helper_test_create_equipment_inexistent()
        self.helper_test_create_equipment_successfully()
        self.helper_test_create_equipment_duplicated()
        self.helper_test_equipment_non_empty_list()

    # helpers tests ==========================================================
    def helper_test_create_equipment_inexistent(self):
        """Checks if creating a new equipment is inexistent"""
        url = reverse('equipment-create', kwargs={'vessel_code': 'MV404'})
        body = json.dumps({
            "code": "5310B9D7",
            "name": "compressor",
            "location": "Brazil"
        })
        response = self.put(url, body)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def helper_test_create_equipment_successfully(self, vessel_code="MV404",
                                                  equip_code="5310B9D7"):
        """Checks if creating a new equipment is inexistent"""
        # First create the missing Vessel
        url = reverse('vessel-create')
        body = json.dumps({"code": vessel_code})
        response = self.put(url, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Try creating the equipment again with the associated Vessel
        url = reverse('equipment-create', kwargs={'vessel_code': vessel_code})
        body = json.dumps({
            "code": equip_code,
            "name": "compressor",
            "location": "Brazil"
        })
        response = self.put(url, body)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def helper_test_create_equipment_duplicated(self):
        """Checks duplicated equipment validation"""
        url = reverse('equipment-create', kwargs={'vessel_code': 'MV404'})
        body = json.dumps({
            "code": "5310B9D7",
            "name": "compressor",
            "location": "Brazil"
        })
        response = self.put(url, body)
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    def helper_test_equipment_non_empty_list(self):
        """Checks if a non-empty list is returned"""
        url = reverse('equipment-list')
        response = self.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        json_data = json.loads(response.content)
        is_empty = True
        if type(json_data) == list:
            is_empty = len(json_data) == 0

        self.assertEqual(is_empty, False)
