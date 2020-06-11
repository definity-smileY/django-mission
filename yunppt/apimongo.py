import pandas as pd
import csv
import json
import os
import sys
import urllib.request
import collections
import pymongo
from pymongo import MongoClient
from xml.dom import minidom
from xml.etree import ElementTree

# 도로명 API결과 JSON으로 받기
# http://www.juso.go.kr/addrlink/jusoSearchSolutionIntroduce.do
def doJusoApi(request, pKey):
    # 초기
    pKey = urllib.parse.quote(pKey)
    url = "http://www.juso.go.kr/addrlink/addrLinkApi.do?currentPage=1&countPerPage=10&keyword="+pKey+"&confmKey=devU01TX0FVVEgyMDIwMDUyMDE2MDg0ODEwOTc3ODk=&resultType=json"

    # 주소 json 결과 받기 : 
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    rescode = response.getcode()
    if(rescode==200):
        # 주소 json 결과 처리 : 
        response_body = response.read()
        # 파이썬 json 객체
        u8_json = response_body.decode('utf-8')
        j = json.loads(u8_json)
        print(type(j))

        roadAddr = []
        #print(j)
        for it in j["results"]["juso"]:
            roadAddr.append(it['roadAddr'])
        print(roadAddr)
    else:
        print("Error Code:" + rescode)
    return roadAddr

# 주소정보 몽고디비에 저장
def insertAddrs(pJson):
    # 몽고디비 연결 클라이언트
    # 1.몽고디비 클라이언트 연결객체 생성
    client = MongoClient('mongodb://localhost:27017/')
    # -- 객체생성확인
    print('client.HOST: {0}'.format(client.HOST))

    # 2. 데이터베이스 생성
    mdb = client['djangodb']
    # -- 디비 생성 확인
    print(mdb)

    # 3. 컬렉션 객체 생성
    # mdb[pColname].remove()
    keys = mdb['addrs']

    #5. 여러개의 데이터 입력
    keys.insert_one(pJson)