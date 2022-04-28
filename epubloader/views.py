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

# 작가/책정보, 목차 정보를 전달
@csrf_exempt
def opfController(request):
    try:
        decoded_image_list = {}
        try:
            client_file = request.FILES['file']

            # unzip file and find opf file 
            with zipfile.ZipFile(client_file, 'r') as zip_ref:
                ziplist = zip_ref.infolist()
                for i in range(0,len(ziplist)):
                    selectedFile = ziplist[i]
                    with zip_ref.open(selectedFile,"r") as sf:
                        zipname = sf.name
                        if zipname[-3:] == 'opf':
                            zipopf = sf.read() 
                            opf = zipopf.decode('utf-8')
                            break
                
                # set opfData
                opfjson = json.loads(json.dumps(xmltodict.parse(opf)))
                title = opfjson['package']['metadata']['dc:title']
                creator = opfjson['package']['metadata']['dc:creator']
                manifest = opfjson['package']['manifest']['item']

                manifest_list = []
                for i in range(len(manifest)):
                    manifest_file = manifest[i]
                    content = manifest_file['@href']
                    split_contents = content.split('/')
                    split_content = split_contents[-1]
                    # xhtml, html 제한 추가
                    if split_content[-4:] == "html":
                        manifest_list.append(split_content)

                data_dict = {}
                data_dict["name"] ="opfFile"
                data_dict["title"] = title
                data_dict["creator"] = creator
                data_dict["manifest"] = manifest_list

                return HttpResponse(json.dumps(data_dict), content_type="application/json")
        except Exception as e:
            return HttpResponse("error1")
    except :
        return HttpResponse("error2")

# 책의 imageData와 Css 정보를 전달
@csrf_exempt
def imageController(request):
    try:
        decoded_image_list = {}
        css_list = {}
        try:
            client_file = request.FILES['file']

            # unzip file and find jpg and css file 
            with zipfile.ZipFile(client_file, 'r') as zip_ref:
                ziplist = zip_ref.infolist()
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
                            css = zipCSS.decode('utf-8')
                            decoded_image_list['css'] = css 

            return HttpResponse(json.dumps(decoded_image_list), content_type="application/json")
        except Exception as e:
            return HttpResponse(e)
    except :
        return HttpResponse("error2")

# 목차에서 동일한 파일을 찾아서 해당 파일 정보 전달
@csrf_exempt
def findFile(request):
    try:
        try:
            client_file = request.FILES['file']
            file_name = request.POST['name']
            name_lang = len(file_name) * (-1)
            data_dict = {}

            # unzip file and find file
            with zipfile.ZipFile(client_file, 'r') as zip_ref:
                ziplist = zip_ref.infolist()

                # if html or xhtml
                if file_name[-4:] == 'html':
                    data_dict["file"] = 'html'

                    # find same html file
                    for i in range(0,len(ziplist)):
                        if ziplist[i].filename[name_lang:] == file_name :
                            selectedFile = ziplist[i] 

                            # open html file
                            with zip_ref.open(selectedFile,"r") as sf:
                                zipdata = sf.read().decode('utf-8')

                                # parsing html with BS4 library
                                soup = BeautifulSoup(zipdata, "lxml") # 만약 이상하면 html.parser로 변환할 것
                                testsoup = soup.section
                                paragraphlist  = testsoup.find_all({'p','img','h1','h2','h3','h4','h5','h6'})
                                arraylist = []
                                for i in range(len(paragraphlist)):
                                    arraylist.append(str(paragraphlist[i]))
                                data_dict["fileData"] = arraylist
                                break

                # 예외처리용
                # else:
                return HttpResponse(json.dumps(data_dict), content_type="application/json")
        except Exception as e:
            return HttpResponse(e)
    except :
        return HttpResponse("error2")



