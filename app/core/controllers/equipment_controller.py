from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from core.models import Equipment, Vessel
from core.serializers import EquipmentSerializer


def get_equipment(req, code):
    try:
        equipment = Equipment.objects.get(code=code)
    except Equipment.DoesNotExist:
        return JsonResponse({'error':'No Equipment found with this code'}, status=404)

    serializer = EquipmentSerializer(equipment)
    return JsonResponse(serializer.data)

def get_equipment_list(req):
    vessel = Equipment.objects.all()
    serializer = EquipmentSerializer(vessel, many=True)
    return JsonResponse(serializer.data, safe=False)


def create_equipment(req, vessel_code):
    try:
        equip_item = JSONParser().parse(req)
    except:
        return JsonResponse({'error': "The input is invalid"}, status=400)
    
    err = validate_item(equip_item)
    if err != None:
        return err
    err = checks_if_item_exists(equip_item)
    if err != None:
        return err
    err = checks_if_vessel_exists(vessel_code)
    if err != None:
        return err

    #if none of the validations above fails, then save it.
    save_item(equip_item, vessel_code)

    return HttpResponse(status=200)


def validate_item(item):
    try:
        code = item['code']
        name = item['name']
        location = item['location']
    except:
        return JsonResponse({'error': "The input has invalid or missing values"}, status=400)


def checks_if_item_exists(item):
    try:
        equipments = Equipment.objects.get(code=item['code'])
        return JsonResponse({'error': 'This Equipment already exists'}, status=409)
    except Equipment.DoesNotExist:
        # if not, then continue code
        pass


def checks_if_vessel_exists(vessel_code):
    try:
        vessel = Vessel.objects.get(code=vessel_code)
        # if yes, then continue the code
    except Vessel.DoesNotExist:
        return JsonResponse({'error':f"The Vessel code {vessel_code} assigned doens't exists"}, status=404)


def save_item(item, vessel_code):
    default_status = 'active'
    if 'status' in item:
        default_status = item['status']

    print('saving equipment....')
    equipment = Equipment(code=item['code'], name=item['name'], vessel_code=vessel_code,
                          location=item['location'], status=default_status)
    equipment.save()
