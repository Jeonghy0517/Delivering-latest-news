#최신 뉴스 이메일로 받아보기
##진행 순서##
#1. 뉴스 홈페이지 접속
#2. 웹페이지 저장
#3. 뉴스 속보 크롤링
#4. 이메일 보내기
#5. 이메일 수신 확인

#1. 뉴스 홈페이지 접속
import webbrowser
url = 'https://news.naver.com/main/list.naver?mode=LPOD&mid=sec&sid1=001&sid2=140&oid=001&isYeonhapFlash=Y'
# webbrowser.open(url)

#2. 웹페이지 저장
import urllib.request; urllib.request.urlopen

#뉴스 속보 페이지를 html 파일로 저장
def save_to_html(url):
    with urllib.request.urlopen(url) as s: #웹 페이지 리소스 객체 생성
        with open('breaking_news.html', 'wb') as f:
            f.write(s.read()) #리소스 내용을 읽어서 html 파일로 저장
save_to_html(url)

#3. 뉴스 속보 크롤링
from bs4 import BeautifulSoup
import requests

#헤더 추가
headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/104.0.0.0 Safari/537.36"}

response = requests.get(url, headers=headers) #서버 응답 확인
beautifulSoup = BeautifulSoup(response.content, "html.parser") #BS 객체 생성

#페이지 제목 크롤링
page_title = beautifulSoup.title.string
print(page_title)

#공백 제거
import re
regex = re.compile(r'[\n\r\t]')
page_title = regex.sub(' ', page_title)
print(page_title)

# 페이지 상단 텍스트 크롤링
main_contents = beautifulSoup.find("dl", attrs={"class":"type04"}).get_text()
print(main_contents)

# 페이지 하단 텍스트 크롤링
sub_contents = beautifulSoup.find("ul", attrs={"class":"type02"}).get_text()
print(sub_contents)

#4. 이메일 보내기
#멀티파트 객체 생성
import smtplib
from email.mime.multipart import MIMEMultipart
msg = MIMEMultipart()

#이메일 송수신자 설정
msg['From'] = 'gpdnjs517@naver.com'
msg['To'] = 'gpdnjs517@naver.com'

#날짜 설정
from email.utils import formatdate
msg['Date'] = formatdate(localtime=True) #현재 지역에 맞는 날짜
msg['Date']

#이메일 제목/본문 작성
from email.header import Header
from email.mime.text import MIMEText
msg['Subject'] = Header(s = page_title, charset='utf-8')
body = MIMEText(main_contents + sub_contents, _charset='utf-8')

#메일 본문 추가
msg.attach(body)

#파일 첨부
import os
from email.mime.base import MIMEBase
from email.encoders import encode_base64

files = list()
files.append('breaking_news.html')

for f in files:
    part = MIMEBase('application',"octet-stream")
    part.set_payload(open(f, "rb").read())
    encode_base64(part) #바이너리 파일 base64 인코딩
    part.add_header('Content-Disposition', 'attachment; filename="%s"' % os.path)
    msg.attach(part) #파일 첨부

import getpass

mailServer = smtplib.SMTP_SSL('smtp.naver.com')
mailServer.login('gpdnjs517@naver.com', getpass.getpass())
mailServer.send_message(msg)
mailServer.quit()

#5. 이메일 수신 확인
import poplib

#암호화된 소켓 연결 (기본 955)
server = poplib.POP3_SSL('pop.naver.com', port=995)

#ID/PW입력
server.user('gpdnjs517@naver.com')
server.pass_(getpass.getpass())

import email
from email.header import decode_header, make_header

#가장 최근 메세지 확인
recent_no = server.stat()[0] #가장 최근 메시지 확인
server.retr(recent_no) #메시지 가져오기 (바이트 문자열, 두번째 요소가 메세지 내용)
raw_email = b'\n'.join(server.retr(recent_no)[1]) #줄바꿈으로 메세지 내용 조인
message = email.message_from_bytes(raw_email) #메세지 객체 생성

#송신자 확인
fr = message.get('From')
print(fr)

#제목 확인
subject = make_header(decode_header(message.get('Subject')))
print(subject)

# 본문 확인
attachments = []

if message.is_multipart():
    # 멀티 파트라면 여러개로 나누어진 메세지를 하니씩 처리
    for part in message.walk():
        ctype = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))
        print(ctype)

        # 컨텐츠에 첨부파일이 있다면
        if 'attachment' in cdispo:
            name = part.get_filename()
            data = part.get_payload(decode=True)
            f = open(name, 'wb')
            f.write(data)
            f.close()
            attachments.append(name)

            # 컨텐츠가 text/plain 이고, 첨부파일이 없다면
        if ctype == 'text/plain' and 'attachment' not in cdispo:
            body = part.get_payload(decode=True)  # 메세지 내용 추출

else:
    # 싱글 파트라면
    body = message.get_payload(decode=True)  # 메세지 내용 추출

body = body.decode('utf-8')

print(f"보낸사람:{fr}")
print(f"제목:{subject}")
print(f"내용:{body}")
print(f"첨부파일:{attachments}")

# 첨부파일 열기
webbrowser.open('file://' + os.path.realpath(attachments[0]))

