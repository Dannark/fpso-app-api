from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from core.controllers.vessel_controller import create_vessel, get_vessel_list
from core.controllers.equipment_controller import get_equipment_list, \
    create_equipment, update_equipment

# Create your views here.


def not_allowed_response():
    return JsonResponse(
        {'error': 'This operation is not allowed from this request'},
        status=status.HTTP_405_METHOD_NOT_ALLOWED)


def index(req):
    return not_allowed_response()


@csrf_exempt
def vessel_list(req):
    if req.method in ['GET']:
        return get_vessel_list(req)
    else:
        return not_allowed_response()


@csrf_exempt
def vessel_create(req):
    if req.method == 'POST':
        return create_vessel(req)
    else:
        return not_allowed_response()


@csrf_exempt
def equipments_list(req):
    if req.method in ['GET']:
        return get_equipment_list(req)
    else:
        return not_allowed_response()


@csrf_exempt
def equipment_create(req, vessel_code):
    if req.method == 'POST':
        return create_equipment(req, vessel_code)
    else:
        return not_allowed_response()


@csrf_exempt
def equipment_update(req):
    if req.method in ['PUT']:
        return update_equipment(req)
    else:
        return not_allowed_response()
