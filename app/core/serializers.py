from rest_framework import serializers
from core.models import Vessel, Equipment

class VesselSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=200)

    def create(self, validated_data):
        return Vessel.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.save()
        return instance


class EquipmentSerializer(serializers.Serializer):
    code = serializers.CharField(max_length=200)
    name = serializers.CharField(max_length=200)
    vessel_code = serializers.CharField(max_length=200)
    location = serializers.CharField(max_length=200)
    status = serializers.CharField(default='active')


    def create(self, validated_data):
        return Equipment.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.code = validated_data.get('code', instance.code)
        instance.name = validated_data.get('name', instance.name)
        instance.vessel_code = validated_data.get('vessel_code', instance.vessel_code)
        instance.location = validated_data.get('location', instance.location)
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance