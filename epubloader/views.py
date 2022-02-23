from django.shortcuts import render
import requests
import json
from django.http import HttpResponse
from django.http import JsonResponse

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
    zipopf ="opf is null"
    zipcontent = "contetnt is null"
    zipImage = "image is null"
    try:
        if request.method == "POST":
            print("post")
            try:
                client_file = request.FILES['file']
                # unzip the zip file to the same directory 
                with zipfile.ZipFile(client_file, 'r') as zip_ref:
                    ziplist = zip_ref.infolist()
                    print(len(ziplist))
                    # for i in range(47,len(ziplist)):
                    #     selectedFile = ziplist[i]
                    #     print(selectedFile)
                    #     with zip_ref.open(selectedFile,"r") as sf:
                    #         zipname = sf.name
                    #         zipcontent = sf.read())
                    for i in range(0,len(ziplist)):
                        selectedFile = ziplist[i]
                        # print(selectedFile.name[-3])
                        # print(selectedFile)
                        with zip_ref.open(selectedFile,"r") as sf:
                            zipname = sf.name
                            if zipname[-3:] == 'opf':
                                print("find opf")
                                zipopf = sf.read() 
                            # print(zipname[-3:])
                            if zipname[-5:] == "xhtml":
                                zipcontent = sf.read()
                            if zipname[-3:] == 'jpg':
                                zipImage = sf.read()
                                img.write(zipImage)
                print(type(zipopf))
                print(zipImage)
                print(2)

                temp_dict = {}
                temp_dict["name"] ="opfFile"
                temp_dict["spine"] = zipopf.decode('utf-8')
                temp_dict["xhtml"] = zipcontent.decode('utf-8')
                # temp_dict["image"] = zipImage.decode('utf-8')
                # json_dict = json.dumps(temp_dict)
                print("read end")
                # print(temp_dict)
                # print(type(json_dict))
                return HttpResponse(json.dumps(temp_dict), content_type="application/json")

            except Exception as e:
                return HttpResponse("error1")
    except :
        return HttpResponse("error2")
    # with zipfile.ZipFile(zip, 'r') as zip_ref:
    #             first = zip_ref.infolist()[0]
    #             with zip_ref.open(first, "r") as fo:
    #                 json_content = json.load(fo)
    #         return HttpResponse(json_content)
    # # unzip = zip.read().decode()
    # # unzip = zip.extractall()
    # # print(unzip)
    
    # return HttpResponse("fail") 