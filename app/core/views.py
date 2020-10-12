from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from core.models import Vessel
from core.serializers import VesselSerializer
from core.controllers.vessel_controller import vessel_controller, get_vessel
from core.controllers.equipment_controller import get_equipment_list, create_equipment, get_equipment

# Create your views here.

def index(req):
    return JsonResponse({'error':'This operation is not allowed from this request'}, status=400)

@csrf_exempt
def vessel_list(request):
    """List all vessels or create a new one."""
    return vessel_controller(request)


@csrf_exempt
def vessel(request, vessel_code):
    """Get a vessel or delete one."""
    return get_vessel(request, vessel_code)
    

@csrf_exempt
def equipments_list(req):
    """Retrieve all equipments."""
    if req.method in ['POST', 'GET']:
        return get_equipment_list(req)
    else:
        return JsonResponse({'error': 'This operation is not allowed from this request'}, status=400)

@csrf_exempt
def equipment(req, vessel_code):
    """Get update or create an equipment"""
    if req.method in ['POST', 'GET']:
        return get_equipment(req, vessel_code)
    elif req.method == 'PUT':
        return create_equipment(req, vessel_code)
    else:
        return JsonResponse({'error': 'This operation is not allowed from this request'}, status=400)
    
