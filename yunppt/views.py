import re
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, HttpResponseRedirect
from datetime import datetime
from django import forms
from django.views.generic import CreateView
from django.http import JsonResponse
from collections import Counter
import folium
from yunppt.apimongo import doJusoApi, insertAddrs
from collections import Counter
from django.http import HttpResponse
import json
from django.shortcuts import redirect
from django.forms import BaseForm

from yunppt.form_.jusoFrm import jusoF as jf
import urllib.request



def go_juso(request):
    jf_ = jf()
    print('여기!')
    # 포스트방식
    if request.method == 'POST':
        print('저기!')
        jf_ = jf(request.POST)
        print(jf_.is_valid())
        print(jf_)
        # if request.method == 'POST': 데이터를 제대로 받았는지 확인
        if jf_.is_valid():
            # jf_.cleaned_data 클래스로 가져온 데이터를 json으로 정리
            cd = jf_.cleaned_data
            print(cd)
            insertAddrs(cd)
        return redirect('/yunppt/go_juso', kwargs={ "title": " 클래스 스터디 타이틀", "message": " 스터디 페이징 ㅋㅋ", "jf_": jf_})

    return render(request, "yunppt/go_juso.html", { "title": " 클래스 스터디 타이틀", "message": " 스터디 페이징 ㅋㅋ", "jf_": jf_})

    
def go_juso_proc(request):
    # 검색어 / 컬렉션이름을 받아서 검색하고 몽고디비에 저장
    # json_list = doNavApiXml(request.GET.get('))
    addrs = doJusoApi(request, pKey = request.GET.get("pKey"))
    print(addrs)
    return JsonResponse(addrs,content_type='application/json', safe=False,json_dumps_params={'ensure_ascii':False})




