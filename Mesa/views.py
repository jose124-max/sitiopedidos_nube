from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.db import transaction

from .models import Administrador, Mesas

@method_decorator(csrf_exempt, name='dispatch')
class CrearMesa(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            id_administrador = request.POST.get('id_administrador', 1)

            observacion = request.POST.get('observacion')
            estado = request.POST.get('estado')
            activa = request.POST.get('activa')
            max_personas = request.POST.get('max_personas')

            administrador = Administrador.objects.get(id_administrador=id_administrador)

            mesa = Mesas(
                id_administrador=administrador,
                observacion=observacion,
                estado=estado,
                activa=activa,
                maxpersonas=max_personas
            )
            mesa.save()

            return JsonResponse({'mensaje': 'Mesa creada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class MostrarMesas(View):
    def get(self, request, *args, **kwargs):
        try:
            mesas = Mesas.objects.all()
            mesas_list = []

            for mesa in mesas:
                mesa_info = {
                    'id_mesa': mesa.id_mesa,
                    'observacion': mesa.observacion,
                    'estado': mesa.estado,
                    'activa': mesa.activa,
                    'max_personas': mesa.maxpersonas
                }
                mesas_list.append(mesa_info)

            return JsonResponse({'mesas': mesas_list})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)
@method_decorator(csrf_exempt, name='dispatch')
class EditarMesa(View):
    @transaction.atomic
    def post(self, request, *args, **kwargs):
        try:
            mesa_id = kwargs.get('id_mesa')
            mesa = Mesas.objects.get(id_mesa=mesa_id)

            observacion = request.POST.get('observacion')
            estado = request.POST.get('estado')
            activa = request.POST.get('activa')
            max_personas = request.POST.get('max_personas')

            # Validar valores de estado y activa
            if estado not in ['D', 'R', 'U', 'A']:
                return JsonResponse({'error': 'Valor no válido para estado'}, status=400)

            if activa not in ['0', '1']:
                return JsonResponse({'error': 'Valor no válido para activa'}, status=400)

            mesa = Mesas.objects.get(id_mesa=mesa_id)

            mesa.observacion = observacion
            mesa.estado = estado
            mesa.activa = activa
            mesa.maxpersonas = max_personas
            mesa.save()

            return JsonResponse({'mensaje': 'Mesa editada con éxito'})
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=400)