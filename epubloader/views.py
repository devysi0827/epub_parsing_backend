import requests, json, zipfile, base64
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt 
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView


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