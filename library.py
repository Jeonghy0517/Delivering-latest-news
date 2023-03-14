#웹브라우저 실행 및 저장
#webbrowser : 파이썬 프로그램에서 시스템 브라우저를 호출할 때 사용하는 모듈
import getpass
import poplib
import webbrowser
url = "www.google.com"

#브라우저 실행
# webbrowser.open(url)

#어떤 브라우저가 호출되는지 확인
print(webbrowser.get())

#호출 브라우저 변경
#브라우저 실행파일 경로
chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
edge_path = "C:/Program Files (x86)/Microsoft/Edge/Application/msedge.exe %s"

#브라우저 실행
# webbrowser.get(edge_path).open(url)

#urllib : URL을 읽고 분석할 떄 사용하는 모듈
#특정 웹 페이지를 .html 확장자로 저장해서 오프라인에서도 읽을 수 있게 활용 가능

#웹페이지 저장 예제
#위키독스 특정 페이지를 오프라인으로도 읽을 수 있도록 페이지 번호를 입력받아 wikidocs_페이지번호.html 파일로 저장
import urllib.request; urllib.request.urlopen

#위키독스 페이지
# webbrowser.open("https://wikidocs.net/1")

#페이지 리소스 객체
urllib.request.urlopen('https://wikidocs.net/1')

#위키독스의 페이지 번호를 입력받아 해당 페이지의 리소스 내용을 파일로 저장하는 함수
def get_wikidocs(page):
    print("wikidocs page:{}".format(page)) #페이지 호출시 출력
    resource = 'https://wikidocs.net/{}'.format(page)

    with urllib.request.urlopen(resource) as s: #페이지 리소스 객체 생성
        with open('wikidocs_%s.html' % page, 'wb') as f:
            f.write(s.read()) #리소스 내용을 읽어서 html 파일로 저장

get_wikidocs(1)
get_wikidocs(2)
#------------------------------------------------------------------------------------------------------------------
#웹페이지에서 원하는 텍스트만 추출
#html.parser : HTML문서를 파싱할 때 사용하는 모듈

#HTML 파일에서 내용을 굵은 글씨로 표시하는 태그와 태그 사이의 문자열을 모두 찾아서 출력하는 프로그램
from html.parser import HTMLParser #HTMLParser 클래스 상속

class MyHTMLParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.is_strong = False

    def handle_starttag(self, tag, attrs): #태그가 열릴 때 호출
        if tag == 'strong':                #<strong> 태그 시작
            self.is_strong = True
    
    def handle_endtag(self, tag):          #태그가 닫힐 때 호출
        if tag == 'strong':                #<strong> 태그 닫힘
            self.is_strong = False
    
    def handle_data(self, data):           #해당 태그 사이의 문자열을 data 변수로 전달
        if self.is_strong:                 #<strong>~</strong> 구간인 경우
            print(data)                    #데이터를 출력

with open('html_sample_1.html') as f:
    parser = MyHTMLParser()
    parser.feed(f.read())

#HTML 파일에서 문서를 연결하는 <a>태그와 </a> 태그 사이의 하이퍼링크를 모두 찾아서 출력하는 프로그램
class MyHTMLParser(HTMLParser): #HTMLParser 클래스 상속
    def __init__(self):
        HTMLParser.__init__(self)
        self.links = []

    def handle_starttag(self, tag, attrs):  #태그가 열릴 때 호출
        if tag == 'a':                      #<a> 태그 시작
            if len(attrs) == 0:             #<a> 태그 속성이 없을 경우
                pass
            else:                           #<a> 태그 속성이 있을 경우
                for (variable, value) in attrs:
                    if variable == "href":  #속성 변수가 하이퍼링크일 경우
                        self.links.append(value)
                        print(value)

with open('html_sample_2.html') as f:
    parser = MyHTMLParser()
    parser.feed(f.read())

print(parser.links)

#------------------------------------------------------------------------------------------------------------------
#이메일 확인하기
#poplib : pop3 서버에 연결하여 받은 메일을 확인하는 데 사용하는 모듈
#매번 gmail과 같은 웹 메일에 접속해서 새로운 메일 내용 확인이 번거로울 때 이를 자동화 할 경우 사용

#이메일 계정 연결
#email_test.py

#email : 바이트 문자열 형식의 이메일 메세지를 사람이 알아 볼 수 있는 문자열 형태로 파싱 및 디코딩할 때 사용되는 모듈

#------------------------------------------------------------------------------------------------------------------
#이메일 보내기
#smtplib : 이메일을 보낼 때 사용하는 모듈
#여러사람에게 메일을 보내거나 첨부파일을 첨부할 수 있음

#이메일 보내기 실습----------------------------#
#SMTP 메일서버 주소 : smtp.naver.com
#보내는 메일 계정 : gpdnjs517@naver.com
#보내는 메일 계정의 비밀번호 :
#받는 사람의 메일 계정 : jeonghy0517@gamil.com
#메일의 제목 : 파일첨부 메일 송신 테스트
#메일의 내용 : "첨부된 파일 2개를 확인해 주세요."
#------------------------------------------#
import smtplib
from email.mime.multipart import MIMEMultipart
msg = MIMEMultipart() #파일 첨부용 멀티파트 객체

#이메일 송수신자 설정
msg['From'] = 'gpdnjs517@naver.com'
msg['To'] = 'jeonghy0517@gmail.com'

#날짜 설정
from email.utils import formatdate
msg['Date'] = formatdate(localtime=True) #현재 지역에 맞는 날짜

#이메일 제목/본문 작성
from email.header import Header
from email.mime.text import MIMEText
msg['Subject'] = Header(s='파일첨부 메일송신 테스트', charset='utf-8')
body = MIMEText('첨부된 파일 2개를 확인해 주세요.', _charset='utf-8')
print(body)  # 내용 확인 - base64 인코딩

msg.attach(body) #메일 본문 추가

#파일 첨부하기
files = list()
files.append('html_sample_1.html')
files.append('html_sample_2.html')

import os
from email.mime.base import MIMEBase
from email.encoders import encode_base64

for f in files:
    part = MIMEBase('application', "octet-stream")
    part.set_payload(open(f,"rb").read())
    encode_base64(part) #바이너리 파일 base64 인코딩
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path.basename(f))
    msg.attach(part) #파일 첨부

#메일 발송하기
import getpass
mailServer = smtplib.SMTP_SSL('smtp.naver.com')
mailServer.login('gpdnjs517@naver.com', getpass.getpass())
mailServer.send_message(msg)
mailServer.quit()

#------------------------------------------------------------------------------------------------------------------
#최신 뉴스 이메일로 받아보기
#BeautifulSoup : HTML 정보로 부터 원하는 데이터를 가져오기 쉽게, 비슷한 분류의 데이터별로 나누어주는 (Parsing) 기능 제공
#보통 html 정보를 가져오는 urllib.request.urlopen() 모듈과 함께 사용
#find()함수를 통해서 원하는 HTML 태그 추출

#BeautifulSoup 설치
from bs4 import BeautifulSoup

#크롤링 웹 페이지 확인
#F12 : 개발자 도구 활성화 => HT
url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&sid1=001&sid2=140&oid=001&isYeonhapFlash=Y'

#html 헤더 설정 : 클라이언트와 서버가 통신할 때 함께 전달하는 부가정보
#날짜, 인코딩정보, 유저정보 등 다양한 내용을 담고 있음
#user-agent에는 운영체제, 소프트웨어 버전, 소프트웨어 유형 등 여러 내용이 포함되어 있음

#헤더 추가
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

#서버 응답 확인
import requests
response = requests.get(url, headers=headers)
response

#뉴스 정보 크롤링
beautifulSoup = BeautifulSoup(response.content, "html.parser") #BeautifulSoup 객체 생성
print(beautifulSoup.title.string) #페이지 제목 크롤링
print(beautifulSoup.find("dl", attrs={"class":"type04"}).get_text()) #페이지 상단 텍스트 크롤링
print(beautifulSoup.find("ul", attrs={"class":"type02"}).get_text()) #페이지 하단 텍스트 크롤링




