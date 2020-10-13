from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, exceptions
from core.models import Vessel
from core.serializers import VesselSerializer


def get_vessel(req, code):
    try:
        vessel = Vessel.objects.get(code=code)
    except Vessel.DoesNotExist:
        return JsonResponse({'error': 'No Vessel found with this code'},
                            status=status.HTTP_404_NOT_FOUND)

    serializer = VesselSerializer(vessel)
    return JsonResponse(serializer.data)


def get_vessel_list(req):
    vessel = Vessel.objects.all()
    serializer = VesselSerializer(vessel, many=True)
    return JsonResponse(serializer.data, safe=False, status=status.HTTP_200_OK)


def create_vessel(req):
    try:
        vessels = JSONParser().parse(req)
    except exceptions.ParseError:
        return JsonResponse({'error': "The input is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

    err = _validate_item(vessels)
    if err is not None:
        return err

    err = _checks_if_item_exists(vessels)
    if err is not None:
        return err

    vessel = Vessel(code=vessels['code'])
    vessel.save()

    return HttpResponse(status=status.HTTP_201_CREATED)


def _validate_item(item, fields=['code']):
    for field in fields:
        if field not in item:
            r = {'error': "The input has invalid or missing values"}
            return JsonResponse(r, status=status.HTTP_400_BAD_REQUEST)


def _checks_if_item_exists(item):
    try:
        Vessel.objects.get(code=item['code'])
        return JsonResponse({'error': 'This vessel already exists'},
                            status=status.HTTP_409_CONFLICT)
    except Vessel.DoesNotExist:
        # if not, then continue code
        pass
