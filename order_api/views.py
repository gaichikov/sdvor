import logging
import json
import jwt
from datetime import datetime, timedelta

from django.shortcuts import render, HttpResponse, Http404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from django.contrib.auth.models import User
from .models import Order, Item, Contact, OrderedItem


JWT_SECRET = 'secret'
JWT_ALGORITHM = 'HS256'
JWT_EXP_DELTA_SECONDS = 60*10

logger = logging.getLogger(__name__)

@csrf_exempt
def login_jwt(request):
    print('Login JWT')
    if request.method == 'POST':
        try:
            user = User.objects.get(username=request.POST['username'])
            if user.check_password(request.POST['password']):
                print('Password matched')
            else:
                print('Wrong credentials')
                return JsonResponse({'message': 'Wrong credentials'}, status=400)
            payload = {
                    'user_id': user.id,
                    'exp': datetime.utcnow() + timedelta(seconds=JWT_EXP_DELTA_SECONDS)
                }
            jwt_token = jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)
            return JsonResponse({'token': jwt_token.decode('UTF-8')})
        except Exception as e:
            print(e)


def orders(request):
    ''' Handles post/get requests '''
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Not authorized'}, status=401)


    if request.method == 'POST':
        try:
            new_contact = Contact(
                phone=request.POST['phone'],
                address=request.POST['address'],
                full_name=request.POST['full_name'],
                email=request.POST['email'],
                )
            new_contact.save()

            new_order = Order(
                owner=request.user,
                contact=new_contact
            )
            new_order.save()

            # Save ordered items (with quantity parameter) and append to many to many item field of order
            if 'items' in request.POST:
                ordered_items_list = json.loads(request.POST['items'])
            else:
                return JsonResponse({'message': 'No items field present'}, status=404)

            if ordered_items_list:
                obj_list = []
                for item in ordered_items_list:
                    obj_list.append(OrderedItem(item_id=item['item']['id'], quantity=item['quantity']))
                created_items = OrderedItem.objects.bulk_create(obj_list)
                new_order.items.add(*created_items)

                return JsonResponse({'message': 'Order created'}, status=201)
            else:
                logger.error('No items in request')
                print('No items in request')
                return JsonResponse({'message': 'No items in request'}, status=404)

        except Exception as e:
            # print(e)
            return JsonResponse({'message': 'Internal server error'}, status=500)
    else:
        MAX_OBJECTS = 50
        orders = Order.objects.all().prefetch_related('contact')[:MAX_OBJECTS]
        data = {'results': list(orders.values('order_uid', 'ts', 'owner', 'contact'))}

        return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})



def orders_detail(request, pk):
    ''' Returns order detail '''
    order = Order.objects.get(pk=pk)

    data = {'results': {
        'email': order.contact.email,
        'phone': order.contact.phone,
        'address': order.contact.address,
        'full_name': order.contact.full_name,
        'items': list(order.items.values('item_id', 'quantity')),
        'total_sum': order.total_sum
        }
    }

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})


def items(request):
    ''' Returns items list '''
    if not request.user.is_authenticated:
        return JsonResponse({'message': 'Not authorized'}, status=401)

    items_qs = Item.objects.all().order_by('name').values('id', 'name', 'price')
    data = {'results': list(items_qs)}

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

