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



@csrf_exempt
def getfile(request):
    # 각 변수 설정
    zipopf ="opf is null"
    zipcontent = "contetnt is null"
    zipImage = "image is null"

    # try,except
    try:
        if request.method == "POST":
            print("posted file")
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
                            if zipname[-5:] == "xhtml":
                                zipcontent = sf.read()
                            if zipname[-3:] == 'jpg':
                                zipImage = sf.read()

                print("start input dict")
                temp_dict = {}
                temp_dict["name"] ="opfFile"
                temp_dict["spine"] = zipopf.decode('utf-8')
                temp_dict["xhtml"] = zipcontent.decode('utf-8')
                temp_dict['image'] = base64.encodebytes(zipImage).decode('utf-8')

                print("end input dict")
                return HttpResponse(json.dumps(temp_dict), content_type="application/json")

            except Exception as e:
                return HttpResponse("error1")
    except :
        return HttpResponse("error2")

                                # zipImageEnc = BytesIO(zipImage)
                                # print(zipImageEnc)
                                # img = Image.open(zipImageEnc)
                                # print(img)
                                # print(type(img))
                                # img.show()
                                # print(type(zipImageEnc))
                                # stringImage = StringIO(zipImage)
                                # print(stringImage)
                                # img.write(zipImage)

@csrf_exempt
def opfController(request):
     # 각 변수 설정
    zipopf ="opf is null"

    # try,except
    try:
        if request.method == "POST":
            print("posted file")
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
                spine = opfjson['package']['spine']['itemref']
                manifest = opfjson['package']['manifest']['item']
                # print(manifest)
                print('----------------')
                # print(spine)
                # print(spine[0]['@idref'])
                spine_list = []
                for i in range(len(spine)):
                    page = spine[i]
                    content = page['@idref']
                    spine_list.append(content)
                # print(spine_list)

                manifest_list = []
                for i in range(len(manifest)):
                    manifest_file = manifest[i]
                    content = manifest_file['@href']
                    split_contents = content.split('/')
                    split_content = split_contents[-1]
                    manifest_list.append(split_content)
                print(manifest_list)

                temp_dict = {}
                temp_dict["name"] ="opfFile"
                temp_dict["title"] = title
                # temp_dict["check"] = opfjson['package']
                temp_dict["spine"] = spine_list
                temp_dict["manifest"] = manifest_list

                print("end input dict")
                return HttpResponse(json.dumps(temp_dict), content_type="application/json")

            except Exception as e:
                return HttpResponse("error1")
    except :
        return HttpResponse("error2")
    

@csrf_exempt
def finder(request):
     # 각 변수 설정
    zipopf ="opf is null"
    # try,except
    try:
        if request.method == "POST":
            print("posted file")
            try:
                client_file = request.FILES['file']
                file_name = request.POST['name']
                name_lang = len(file_name) * (-1)
                print(name_lang)
                # unzip the zip file to the same directory 
                with zipfile.ZipFile(client_file, 'r') as zip_ref:
                    ziplist = zip_ref.infolist()
                    print('-------------------------')
                    print("unzip")
                    temp_dict = {}
                    if file_name[-4:] == 'html':
                        temp_dict["file"] = 'html'
                        for i in range(0,len(ziplist)):
                            if ziplist[i].filename[name_lang:] == file_name :
                                selectedFile = ziplist[i] 
                                with zip_ref.open(selectedFile,"r") as sf:
                                    zipdata = sf.read().decode('utf-8')
                                    print(type(zipdata))
                                    soup = BeautifulSoup(zipdata)
                                    print('soup------------------')
                                    # print(soup)
                                    paragraphlist = soup.find_all('p')
                                    # print(type(paragraphlist))
                                    # print(paragraphlist)
                                    arraylist = []
                                    for i in range(len(paragraphlist)):
                                        arraylist.append(str(paragraphlist[i]))
                                    print(arraylist)
                                    temp_dict["ars"] = arraylist
                                    # print(json.dumps(temp_dict))
                                    # print('2-----------------')
                                    break

                    else:
                        temp_dict["file"] = 'jpg'
                        for i in range(0,len(ziplist)):
                            if ziplist[i].filename[name_lang:] == file_name :
                                selectedFile = ziplist[i] 
                                with zip_ref.open(selectedFile,"r") as sf:
                                    zipImage = sf.read()
                                    zipdata = base64.encodebytes(zipImage).decode('utf-8')
                                    temp_dict["data"] = zipdata

                                    break

                    
                            
                            # print(ziplist[i].filename[name_lang:])
                    return HttpResponse(json.dumps(temp_dict), content_type="application/json")
            except Exception as e:
                return HttpResponse(e)
    except :
        return HttpResponse("error2")
    #                         selectedFile = ziplist[i]
    #                         with zip_ref.open(selectedFile,"r") as sf:
    #                             zipname = sf.name
    #                             if zipname[-3:] == 'opf':
    #                                 zipopf = sf.read() 
    #                                 opf = zipopf.decode('utf-8')
    #                                 break
    #             print('----------------')

    #             opfxml = xmltodict.parse(opf)
    #             opfjson = json.loads(json.dumps(opfxml))
    #             title = opfjson['package']['metadata']['dc:title']
    #             spine = opfjson['package']['spine']['itemref']
    #             manifest = opfjson['package']['manifest']['item']
    #             # print(manifest)
    #             print('----------------')
    #             # print(spine)
    #             # print(spine[0]['@idref'])
    #             spine_list = []
    #             for i in range(len(spine)):
    #                 page = spine[i]
    #                 content = page['@idref']
    #                 spine_list.append(content)
    #             # print(spine_list)

    #             manifest_list = []
    #             for i in range(len(manifest)):
    #                 manifest_file = manifest[i]
    #                 content = manifest_file['@href']
    #                 split_contents = content.split('/')
    #                 split_content = split_contents[-1]
    #                 manifest_list.append(split_content)
    #             print(manifest_list)

    #             temp_dict = {}
    #             temp_dict["name"] ="opfFile"
    #             temp_dict["title"] = title
    #             # temp_dict["check"] = opfjson['package']
    #             temp_dict["spine"] = spine_list
    #             temp_dict["manifest"] = manifest_list

    #             print("end input dict")
    #             return HttpResponse(json.dumps(temp_dict), content_type="application/json")

    #         except Exception as e:
    #             return HttpResponse("error1")
    # except :
    #     return HttpResponse("error2")
    