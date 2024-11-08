import requests

def send(imageName):
    try:
        file_path = f'C:/Users/cdh39/PycharmProjects/4th_capstone/images/{imageName}'
        files = {'file': open(file_path, 'rb')}  # file_path에 해당하는 이미지 파일을 바이너리 모드로 열어서 file에 저장

        url = 'http://localhost:8080/api/upload'

        response = requests.post(url, files=files)  # 지정한 url로 post 요청

    except Exception as e:
        print("이미지 전송에 실패했습니다.")
        exit()
