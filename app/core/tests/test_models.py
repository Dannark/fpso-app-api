from django.test import TestCase
from core.models import VesselManager, EquipmentManager


class ModelTests(TestCase):

    def test_create_vessel_successful(self):
        """Test if creating a new vessel is successful"""
        code = "MV102"

        vessel = VesselManager().create(code=code)
        self.assertEqual(vessel.code, code)

    def test_create_vessel_code_valid(self):
        """Test if vessel code is valid"""
        with self.assertRaises(ValueError):
            VesselManager().create(None)

    def test_create_equipment_successful(self):
        """Test if creating equipment is successful"""
        name = "compressor"
        code = "5310B9D7"
        location = "Brazil"

        equip = EquipmentManager().create(code=code, name=name,
                                          location=location,
                                          vessel_code='MV102')
        self.assertEqual(equip.name, name)
        self.assertEqual(equip.code, code)
        self.assertEqual(equip.location, location)

    def test_create_equipment_valid(self):
        """Test if equipment fields are valids"""
        name = "compressor"
        code = "5310B9D7"
        location = "Brazil"

        equip = EquipmentManager().create(code=code, name=name,
                                          location=location,
                                          vessel_code='MV102')
        self.assertNotEqual(equip.code, None)
        self.assertNotEqual(equip.name, None)
        self.assertNotEqual(equip.location, None)
        self.assertNotEqual(equip.vessel_code, None)
