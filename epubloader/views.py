import requests, json, zipfile, base64
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView
from bs4 import BeautifulSoup
import xml.etree.ElementTree as ET
import xmltodict



# @csrf_exempt
# def getfile(request):
#     # 각 변수 설정
#     zipopf ="opf is null"
#     zipcontent = "contetnt is null"
#     zipImage = "image is null"

#     # try,except
#     try:
#         if request.method == "POST":
#             print("posted file")
#             try:
#                 client_file = request.FILES['file']
#                 # unzip the zip file to the same directory 
#                 with zipfile.ZipFile(client_file, 'r') as zip_ref:
#                     ziplist = zip_ref.infolist()
#                     print('-------------------------')
#                     print("unzip")
#                     for i in range(0,len(ziplist)):
#                         selectedFile = ziplist[i]
#                         with zip_ref.open(selectedFile,"r") as sf:
#                             zipname = sf.name
#                             if zipname[-3:] == 'opf':
#                                 zipopf = sf.read() 
#                             if zipname[-5:] == "xhtml":
#                                 zipcontent = sf.read()
#                             if zipname[-3:] == 'jpg':
#                                 zipImage = sf.read()

#                 print("start input dict")
#                 temp_dict = {}
#                 temp_dict["name"] ="opfFile"
#                 temp_dict["spine"] = zipopf.decode('utf-8')
#                 temp_dict["xhtml"] = zipcontent.decode('utf-8')
#                 temp_dict['image'] = base64.encodebytes(zipImage).decode('utf-8')

#                 print("end input dict")
#                 return HttpResponse(json.dumps(temp_dict), content_type="application/json")

#             except Exception as e:
#                 return HttpResponse("error1")
#     except :
#         return HttpResponse("error2")

@csrf_exempt
def ImageController(request):
     # 각 변수 설정
    zipopf ="opf is null"

    # try,except
    try:
        if request.method == "POST":
            decoded_image_list = {}
            css_list = {}
            try:
                client_file = request.FILES['file']
                with zipfile.ZipFile(client_file, 'r') as zip_ref:
                    ziplist = zip_ref.infolist()
                    print('-------------------------')
                    for i in range(0,len(ziplist)):
                        selectedFile = ziplist[i]
                        with zip_ref.open(selectedFile,"r") as sf:
                            zipname = sf.name
                            if zipname[-3:] == 'jpg':
                                imageName = zipname[:-3]
                                split_contents = imageName.split('/')
                                split_content = split_contents[-1][:-1]
                                zipImage = sf.read()
                                zipdata = base64.encodebytes(zipImage).decode('utf-8')
                                decoded_image_list[split_content] = zipdata
                            elif zipname[-3:] == 'css':
                                zipCSS = sf.read()
                                print(zipCSS)
                print('----------------')
                # print(decoded_image_list)

                return HttpResponse(json.dumps(decoded_image_list), content_type="application/json")

            except Exception as e:
                return HttpResponse(e)
    except :
        return HttpResponse("error2")


@csrf_exempt
def opfController(request):
     # 각 변수 설정
    zipopf ="opf is null"

    # try,except
    try:
        if request.method == "POST":
            print("posted file")
            decoded_image_list = {}
            try:
                client_file = request.FILES['file']
                # unzip the zip file to the same directory 
                with zipfile.ZipFile(client_file, 'r') as zip_ref:
                    ziplist = zip_ref.infolist()
                    print('-------------------------')
                    print("unzip")
                    for i in range(0,len(ziplist)):
                        selectedFile = ziplist[i]
                        with zip_ref.open(selectedFile,"r") as sf:
                            zipname = sf.name
                            if zipname[-3:] == 'opf':
                                zipopf = sf.read() 
                                opf = zipopf.decode('utf-8')
                                break
                print('----------------')

                opfxml = xmltodict.parse(opf)
                opfjson = json.loads(json.dumps(opfxml))
                title = opfjson['package']['metadata']['dc:title']
                creator = opfjson['package']['metadata']['dc:creator']
                spine = opfjson['package']['spine']['itemref']
                manifest = opfjson['package']['manifest']['item']
                print('----------------')

                spine_list = []
                for i in range(len(spine)):
                    page = spine[i]
                    content = page['@idref']
                    spine_list.append(content)

                manifest_list = []
                for i in range(len(manifest)):
                    manifest_file = manifest[i]
                    content = manifest_file['@href']
                    split_contents = content.split('/')
                    split_content = split_contents[-1]
                    # xhtml 제한 추가
                    # if split_content[-4:] == "html":
                    manifest_list.append(split_content)
                # print(manifest_list)

                temp_dict = {}
                temp_dict["name"] ="opfFile"
                temp_dict["title"] = title
                temp_dict["creator"] = creator
                temp_dict["spine"] = spine_list
                temp_dict["manifest"] = manifest_list

                return HttpResponse(json.dumps(temp_dict), content_type="application/json")

            except Exception as e:
                return HttpResponse("error1")
    except :
        return HttpResponse("error2")
    

@csrf_exempt
def findFile(request):
     # 각 변수 설정
    zipopf ="opf is null"
    # try,except
    try:
        if request.method == "POST":
            try:
                # var setting
                client_file = request.FILES['file']
                file_name = request.POST['name']
                name_lang = len(file_name) * (-1)
                temp_dict = {}

                # unzip file 
                with zipfile.ZipFile(client_file, 'r') as zip_ref:
                    ziplist = zip_ref.infolist()
                    print('-------------------------')

                    # if html
                    if file_name[-4:] == 'html':
                        temp_dict["file"] = 'html'

                        # find same html file
                        for i in range(0,len(ziplist)):
                            if ziplist[i].filename[name_lang:] == file_name :
                                selectedFile = ziplist[i] 

                                # open html file
                                with zip_ref.open(selectedFile,"r") as sf:
                                    zipdata = sf.read().decode('utf-8')

                                    # parsing html
                                    print('soup------------------')
                                    soup = BeautifulSoup(zipdata, "lxml") # 만약 이상하면 html.parser로 변환할 것
                                    testsoup = soup.section
                                    # print(testsoup)
                                    # print('_______________')
                                    # print(testsoup.find_all())
                                    # print(testsoup.find_all({'p','img','h1','h2','h3','h4','h5','h6'}))
                                    # print(soup.prettify())
                                    paragraphlist  = testsoup.find_all({'p','img','h1','h2','h3','h4','h5','h6'})
                                    # print(body)
                                    
                                    



                                    # paragraph 가져오기
                                    # paragraphlist = soup.find_all('p')
                                    # print(paragraphlist)

                                    # # make dict for json
                                    arraylist = []
                                    for i in range(len(paragraphlist)):
                                        arraylist.append(str(paragraphlist[i]))
                                    temp_dict["ars"] = arraylist
                                    # print(temp_dict)
                                    break
                    
                    # if jpg 
                    else:
                        temp_dict["file"] = 'jpg'

                        # find same jpg
                        for i in range(0,len(ziplist)):
                            if ziplist[i].filename[name_lang:] == file_name :
                                selectedFile = ziplist[i] 

                                # open jpg file and make dict
                                with zip_ref.open(selectedFile,"r") as sf:
                                    zipImage = sf.read()
                                    zipdata = base64.encodebytes(zipImage).decode('utf-8')
                                    temp_dict["data"] = zipdata
                                    break

                    return HttpResponse(json.dumps(temp_dict), content_type="application/json")

    # error return
            except Exception as e:
                return HttpResponse(e)
    except :
        return HttpResponse("error2")
