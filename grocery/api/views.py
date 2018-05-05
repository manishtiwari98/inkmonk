from django.shortcuts import render,get_object_or_404
from django.core import serializers
from .models import *
from django.http import JsonResponse,HttpResponse,HttpResponseRedirect
import json
from django.views.decorators.csrf import csrf_exempt
import hashlib

def authorize(authToken):
    userObj=User.objects.filter(authToken=authToken)
    if userObj:
        return True
    else:
        return False

@csrf_exempt
def getItemList(request):

    try:
        authToken=request.POST['authToken']
        if authorize(authToken):
            itemList=list(Item.objects.all().values())
            
            data={
                'items':itemList,    
                'isVerified':True
            }
        else :
            data={
                'isVerified':False
            }
    except:
        data={
            'isVerified':False
        }
    
    return JsonResponse(data)
        
    
@csrf_exempt
def verify(request):
   
    try:
        email=request.POST['inputEmail']
        password=request.POST['inputPassword']
        userobj=get_object_or_404(User,email=email)
    except:
        return HttpResponse(status=403)
    password=hashlib.md5(password.encode('utf-8 ')).hexdigest()  
    if userobj.password == password:
        data={
            'authToken': userobj.authToken,
            'isLogin': True
        }
    else :
        data={
            'isLogin':False
        }
    return JsonResponse(data)

@csrf_exempt
def createInvoice(request):
    try:
        order=request.POST['data']
        name=request.POST['name']
        mob=request.POST['mob']

        invoiceObj=Invoice( 
            customerName=name,
            mobNo=mob
            )
        invoiceObj.save()
        order=json.loads(order)
        totAmt=0
        for elem in order:
            id=int(elem['id'])
            noofunits=elem['noofunits']
            item=Item.objects.get(pk=id)
            detailObj=InvoiceDetail(
                invoiceId=invoiceObj,
                itemId=item,
                noOfUnits=noofunits
            )
            detailObj.save()
            taxPer=item.tax
            discPer=item.discount
            amt=noofunits*item.priceperunit 
            totAmt+=amt + amt*taxPer - amt*discPer

        invoiceObj.totAmt=totAmt
        invoiceObj.save()

        data = {
            "totAmt":totAmt,
            "invoiceId":invoiceObj.invoiceId
        }
        return JsonResponse(data)

    except:
        return HttpResponse(status=400)

@csrf_exempt
def update(request):
    try:
        itemId=request.POST['itemId']
        val=request.POST['noofunits']
        authToken=request.POST['authToken']
        if authorize(authToken):
            itemObj=Item.objects.get(pk=itemId)
            itemHistoryObj=Item_History(
                itemId=itemObj,
                unitsAdded=int(val)
            )
            itemHistoryObj.save()
            data={
                'isUpdated':True,
                'newVal': itemObj.unitsAvailable
            }
            return JsonResponse(data)
        else:
            raise Exception
    except:
        return HttpResponse(status=403)
