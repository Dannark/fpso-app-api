from django.db import models


class VesselManager(object):
    def create(self, code):

        if not code:
            raise ValueError("Vessel code can't be empty")

        vessel = Vessel(code=code)
        vessel.save()

        return vessel


class EquipmentManager(object):

    def create(self, code, name, location, vessel_code, status='active'):

        if not code:
            raise ValueError("Equipment code can't be empty")
        if not name:
            raise ValueError("Equipment name can't be empty")
        if not location:
            raise ValueError("Equipment location can't be empty")
        if not vessel_code:
            raise ValueError("Equipment vessel_code can't be empty")

        equipment = Equipment(code=code, name=name, vessel_code=vessel_code,
                              location=location, status=status)
        equipment.save()

        return equipment


# Create your models here.
class Vessel(models.Model):
    code = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.code


class Equipment(models.Model):
    code = models.CharField(max_length=200, unique=True)
    name = models.CharField(max_length=200)
    vessel_code = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    status = models.CharField(max_length=200, default='active')
