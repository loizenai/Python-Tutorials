from django.shortcuts import render 
from django.http import HttpResponse
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser 
from rest_framework import status
 
from customers.models import Customer
from customers.serializers import CustomerSerializer

from rest_framework.decorators import api_view

@csrf_exempt
@api_view(['GET', 'POST', 'DELETE'])
def customer_list(request):
    if request.method == 'GET':
        try:
          customers = Customer.objects.all()
          customers_serializer = CustomerSerializer(customers, many=True)

          response = {
             'message': "Get all Customers'Infos Successfully",
             'customers': customers_serializer.data,
             'error': ""
          }
          return JsonResponse(response, status=status.HTTP_200_OK);
        except: 
          error = {
            'message': "Fail! -> can NOT get all the customers List. Please check again!",
            'customers': "[]",
            'error': "Error"
          }
          return JsonResponse(error, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
 
    elif request.method == 'POST':
        try:
            customer_data = JSONParser().parse(request)
            customer_serializer = CustomerSerializer(data=customer_data)
            
            if customer_serializer.is_valid():
                customer_serializer.save()
                print(customer_serializer.data)
                response = {
                   'message': "Successfully Upload a Customer with id = %d" % customer_serializer.data.get('id'),
                   'customers': [customer_serializer.data],
                   'error': "" 
                }
                return JsonResponse(response, status=status.HTTP_201_CREATED)
            else:
                error = {
                    'message':"Can Not upload successfully!",
                    'customers':"[]",
                    'error': customer_serializer.errors
                }
                return JsonResponse(error, status=status.HTTP_400_BAD_REQUEST)
        except: 
            exceptionError = {
                    'message': "Can Not upload successfully!",
                    'customers': "[]",
                    'error': "Having an exception!"
                }
            return JsonResponse(exceptionError, status=status.HTTP_500_INTERNAL_SERVER_ERROR);
    
    elif request.method == 'DELETE':
        try:
            Customer.objects.all().delete()
            return HttpResponse(status=status.HTTP_204_NO_CONTENT)
        except:
            exceptionError = {
                    'message': "Can Not Deleted successfully!",
                    'customers': "[]",
                    'error': "Having an exception!"
                }
            return JsonResponse(exceptionError, status=status.HTTP_500_INTERNAL_SERVER_ERROR);

@csrf_exempt 
@api_view(['GET', 'PUT', 'DELETE'])
def customer_detail(request, pk):
    try: 
        customer = Customer.objects.get(pk=pk)
    except Customer.DoesNotExist:
        exceptionError = {
            'message': "Not found a Customer with id = %s!" % pk,
            'customers': "[]",
            'error': "404 Code - Not Found!"
        }
        return JsonResponse(exceptionError, status=status.HTTP_404_NOT_FOUND) 
 
    if request.method == 'GET':
        customer_serializer = CustomerSerializer(customer) 
        response = {
            'message': "Successfully get a Customer with id = %s" % pk,
            'customers': [customer_serializer.data],
            'error': ""
        }
        return JsonResponse(response, status=status.HTTP_200_OK);
 
    elif request.method == 'PUT':
        try:
            customer_data = JSONParser().parse(request)
            customer_serializer = CustomerSerializer(customer, data=customer_data)

            if customer_serializer.is_valid(): 
                customer_serializer.save()
                response = {
                    'message': "Successfully Update a Customer with id = %s" % pk,
                    'customers': [customer_serializer.data],
                    'error': ""
                }                
                return JsonResponse(response) 

            response = {
                    'message': "Fail to Update a Customer with id = %s" % pk,
                    'customers': [customer_serializer.data],
                    'error': customer_serializer.errors
                }
            return JsonResponse(response, status=status.HTTP_400_BAD_REQUEST) 
        except:
            exceptionError = {
                'message': "Fail to update a Customer with id = %s!" % pk,
                'customers': [customer_serializer.data],
                'error': "Internal Error!"
            }
            return JsonResponse(exceptionError, status=status.HTTP_500_INTERNAL_SERVER_ERROR) 
 
    elif request.method == 'DELETE':
        print("Deleting a Customer with id=%s"%pk)
        customer.delete() 
        customer_serializer = CustomerSerializer(customer) 
        response = {
                'message': "Successfully Delete a Customer with id = %s" % pk,
                'customers': [customer_serializer.data],
                'error': ""
            }
        return JsonResponse(response)

@csrf_exempt
@api_view(['GET'])
def customer_list_age(request, age):
    try:
        customers = Customer.objects.filter(age=age)
        
        if request.method == 'GET': 
            customers_serializer = CustomerSerializer(customers, many=True)
            response = {
                'message': "Successfully filter all Customers with age = %s" % age,
                'customers': customers_serializer.data,
                'error': ""
            }
            return JsonResponse(response, safe=False)
            # In order to serialize objects, we must set 'safe=False'
    except:
        exceptionError = {
                'message': "Fail to get a Customer with age = %s" % age ,
                'customers': "[]",
                'error': "Raise an Exception!"
            }
        return JsonResponse(exceptionError, status=status.HTTP_500_INTERNAL_SERVER_ERROR);