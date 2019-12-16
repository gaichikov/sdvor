import logging
import json

from django.shortcuts import render, HttpResponse, Http404
from django.http import JsonResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from .models import Order, Item, Contact, OrderedItem


def orders(request):
    ''' Handles post/get requests '''
    if not request.user.is_authenticated:
        return HttpResponse(status=401)

    if request.method == 'POST':
        # print('post method')
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

            # Save ordered items (with quantity parameter) and append to many to many item field
            if 'items' in request.POST:
                obj_list = []
                ordered_items_list = json.loads(request.POST['items'])

                for item in ordered_items_list:
                    obj_list.append(OrderedItem(item_id=item['item']['id'], quantity=item['quantity']))
                created_items = OrderedItem.objects.bulk_create(obj_list)
                new_order.items.add(*created_items)

                return HttpResponse(status=201)
            else:
                print('No items in request')
                return HttpResponse(status=404)

        except Exception as e:
            print(e)
            return HttpResponse(status=500)
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

    items_qs = Item.objects.all().order_by('name').values('id', 'name', 'price')
    data = {'results': list(items_qs)}

    return JsonResponse(data, safe=False, json_dumps_params={'ensure_ascii': False})

