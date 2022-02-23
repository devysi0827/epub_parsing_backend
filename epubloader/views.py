from django.shortcuts import render
import requests
import json
from django.http import HttpResponse

from django.contrib.auth.models import User
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.views.decorators.csrf import csrf_exempt 


import zipfile
from json import load


# Create your views here.

def test(request):
    data = {"testname1":"testdata"}
    print("1")
    return HttpResponse(data) 

@csrf_exempt
def getfile(request):
    print("getfile")
    # client_file = request.FILES['file']
    try:
        if request.method == "POST":
            print("post")
            try:
                client_file = request.FILES['file']
                print("11")
                # unzip the zip file to the same directory 
                with zipfile.ZipFile(client_file, 'r') as zip_ref:
                    print("22")
                    ziplist = zip_ref.infolist()
                    print(len(ziplist))
                    for i in range(47,len(ziplist)):
                        selectedFile = ziplist[i]
                        print(selectedFile)
                        with zip_ref.open(selectedFile,"r") as sf:
                            print(sf.name)
                            print(sf.read())
                    # with zip_ref.open(first, "r") as fo:
                    # print(first)
                        # print("33")
                        # json_content = json.load(fo)
                        # print(fo)
                        # return HttpResponse(json_content)
                # doSomething(json_content)
                print("read end")
                return HttpResponse(json_content)

            except Exception as e:
                return HttpResponse(1)
    except :
        return HttpResponse(1)
    # with zipfile.ZipFile(zip, 'r') as zip_ref:
    #             first = zip_ref.infolist()[0]
    #             with zip_ref.open(first, "r") as fo:
    #                 json_content = json.load(fo)
    #         return HttpResponse(json_content)
    # # unzip = zip.read().decode()
    # # unzip = zip.extractall()
    # # print(unzip)
    
    # return HttpResponse("fail") 