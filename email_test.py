import poplib
import getpass

server = poplib.POP3_SSL('pop.naver.com', port=995)
server.user('gpdnjs517')
server.pass_(getpass.getpass())

print(server.stat) #메일 개수, 크기(bytes)
recent_no = server.stat()[0] #가장 최근 메세지 번호
server.retr(recent_no) #메시지 가져오기 (바이트 문자열, 두번째 요소가 메시지 내용)

raw_email = b'\n'.join(server.retr(recent_no)[1]) #줄바꿈으로 메세지 내용 조인
print(raw_email)

#email : 바이트 문자열 형식의 이메일 메세지를 사람이 알아 볼 수 있는 문자열 형태로 파싱 및 디코딩할 때 사용되는 모듈
import email
from email.header import decode_header, make_header

#메세지 객체 생성
message = email.message_from_bytes(raw_email)
print(message)

#이메일 정보 확인
message.get('From') #송신자 확인

fr = make_header(decode_header(message.get('From'))) #email 모듈 디코더 활용
print(fr)

subject = make_header(decode_header(message.get('Subject'))) #제목 확인
print(subject)

#이메일 본문 확인
#이메일의 메세지는 멀티파트로 구성될 수도 있고 아닐수도 있음 => 멀티파트인지 아닌지 분기해서 확인
#멀티파트 형식 : 첨부파일이 있음 , text/plain, txt/html 형식
if message.is_multipart():
    #멀티 파트라면 여러개로 나누어진 메세지를 하나씩 처리
    for part in message.walk():
        ctypes = part.get_content_type()
        cdispo = str(part.get('Content-Disposition'))

        # 컨텐츠가 text/plain 이고, 첨부파일이 없다면
        if ctypes == 'text/plain' and 'attachment' not in cdispo:
            body = part.get_payload(decode = True) #메세지 내용 추출
            break
else:
    #싱글 파트라면
    body = message.get_payload(decode=True) #메세지 내용 추출

body = body.decode('utf-8')

print(f"보낸사람:{fr}")
print(f"보낸사람:{subject}")
print(f"보낸사람:{body}")