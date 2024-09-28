import requests

def send(imgName):
    file_path = f'C:/Users/cdh39/PycharmProjects/ayu_capstone/venv/images/{imgName}.jpg'
    files = {'file': open(file_path, 'rb')} #file_path에 해당하는 이미지 파일을 바이너리 모드로 열어서 file에 저장

    url = 'http://localhost:8080/api/upload'

    response = requests.post(url, files=files) #지정한 url로 post 요청
    print(response.status_code) #서버로부터 받은 HTTP 응답 상태 코드를 출력
    print(response.text) #서버가 반환한 응답을 출력