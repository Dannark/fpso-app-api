from django.http import HttpResponse, JsonResponse
from rest_framework.parsers import JSONParser
from rest_framework import status, exceptions
from core.models import Equipment, Vessel
from core.serializers import EquipmentSerializer


def get_equipment(req, code):
    try:
        equipment = Equipment.objects.get(code=code)
    except Equipment.DoesNotExist:
        return JsonResponse({'error': 'No Equipment found with this code'},
                            status=status.HTTP_404_NOT_FOUND)

    serializer = EquipmentSerializer(equipment)
    return JsonResponse(serializer.data)


def get_equipment_list(req):
    try:
        params = JSONParser().parse(req)
        equipment = Equipment.objects.filter(**params)
        serializer = EquipmentSerializer(equipment, many=True)
        return JsonResponse(serializer.data, safe=False)
    except exceptions.ParseError:
        # No filters retrived or invalids
        pass

    # show all items instead
    vessel = Equipment.objects.all()
    serializer = EquipmentSerializer(vessel, many=True)
    return JsonResponse(serializer.data, safe=False,
                        status=status.HTTP_200_OK)


def update_equipment(req):
    try:
        equip_item = JSONParser().parse(req)
    except exceptions.ParseError:
        return JsonResponse({'error': "The input is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

    # if it is a single value object, convert it to list
    if type(equip_item) != list:
        equip_item = [equip_item]

    for index, item in enumerate(equip_item):
        err = _validate_item(item, ['code'])
        if err is not None:
            return err

        err = _checks_if_item_exists(item)
        if err is not None:
            # item exists
            err = _update_item(item)
            if err is not None:
                return err
        else:
            msg = f"The equipment of code '{item['code']}' doens't exists"
            return JsonResponse({'error': msg},
                                status=status.HTTP_404_NOT_FOUND)

    return HttpResponse(status=status.HTTP_200_OK)


def create_equipment(req, vessel_code):
    try:
        equip_item = JSONParser().parse(req)
    except exceptions.ParseError:
        return JsonResponse({'error': "The input is invalid"},
                            status=status.HTTP_400_BAD_REQUEST)

    err = _validate_item(equip_item)
    if err is not None:
        return err

    err = _checks_if_item_exists(equip_item)
    if err is not None:
        return err

    err = _checks_if_vessel_exists(vessel_code)
    if err is not None:
        return err

    # if none of the validations above fails, then save it.
    _save_item(equip_item, vessel_code)

    return HttpResponse(status=status.HTTP_201_CREATED)


def _validate_item(item, fields=['code', 'name', 'location']):
    for field in fields:
        if field not in item:
            r = {'error': "The input has invalid or missing values"}
            return JsonResponse(r, status=status.HTTP_400_BAD_REQUEST)


def _checks_if_item_exists(item):
    try:
        Equipment.objects.get(code=item['code'])
        r = {'error': f"The equipment code {item['code']} already exists"}
        return JsonResponse(r, status=status.HTTP_409_CONFLICT)
    except Equipment.DoesNotExist:
        # if not, then continue code
        pass


def _checks_if_vessel_exists(vessel_code):
    try:
        Vessel.objects.get(code=vessel_code)
        # if yes, then continue the code
    except Vessel.DoesNotExist:
        msg = f"The Vessel code {vessel_code} assigned doens't exists"
        return JsonResponse({'error': msg}, status=status.HTTP_404_NOT_FOUND)


def _save_item(item, vessel_code):
    default_status = 'active'
    if 'status' in item:
        default_status = item['status']

    equipment = Equipment(code=item['code'], name=item['name'],
                          vessel_code=vessel_code, location=item['location'],
                          status=default_status)
    equipment.save()


def _update_item(item):
    try:
        equip = Equipment.objects.get(code=item['code'])

        if 'name' in item:
            equip.name = item['name']

        if 'status' in item:
            equip.status = item['status']

        if 'location' in item:
            equip.status = item['location']

        equip.save()

    except Equipment.DoesNotExist:
        r = {'error': f"The Item code {item['code']} assigned doens't exists"}
        return JsonResponse(r, status=status.HTTP_404_NOT_FOUND)
