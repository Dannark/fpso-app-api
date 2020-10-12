from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from core.models import Vessel
from core.serializers import VesselSerializer


def vessel_controller(req):
    if req.method == 'GET':
        return JsonResponse({'error':'This operation is not allowed from this request'}, status=400)

    elif req.method == 'POST':
        return get_vessel_list(req)

    elif req.method == 'PUT':
        return create_vessel(req)


def get_vessel(req, code):
    if req.method == 'DELETE':
        return delete_vessel(req)
    
    else:
        try:
            vessel = Vessel.objects.get(code=code)
        except Vessel.DoesNotExist:
            return JsonResponse({'error':'No Vessel found with this code'}, status=404)

        serializer = VesselSerializer(vessel)
        return JsonResponse(serializer.data)

def delete_vessel(req, code):
    try:
        vessel = Vessel.objects.get(code=code)
        vessel.delete()
        HttpResponse(status=204)
    except Vessel.DoesNotExist:
        return JsonResponse({'error':'No Vessel found with this code'}, status=404)


def get_vessel_list(req):
    vessel = Vessel.objects.all()
    serializer = VesselSerializer(vessel, many=True)
    return JsonResponse(serializer.data, safe=False)


def create_vessel(req):
    try:
        vessels = JSONParser().parse(req)

        for index, item in enumerate(vessels):
            try:
                code = item['code']
            except:
                return JsonResponse({'error':f"Invalid input at index [{index}]"}, status=400)

            try:
                vessel = Vessel.objects.get(code=code)

                return JsonResponse({'error':'This Vessel already exists'}, status=409)
            except Vessel.DoesNotExist:
                # vessel = Vessel(code=code)
                # vessel.save()
                pass
    except:
        return JsonResponse({'error':"The input is invalid"}, status=400)

    return HttpResponse(status=200)
