from ultralytics import YOLO
import cv2
import math
import time                     # 시간 정보 및 딜레이를 주기 위해 사용
import serial                   #시리얼 통신을 처리하는 모듈
import sendImage
import findUser
import sendToDB
import gpsModule

#----------------- GPS 모듈 연결 --------------------#
try:                                                # COM3에서 115200의 보드레이트로 시리얼 통신을 설정
    sr = serial.Serial("COM3", 115200)
    print("GPS 모듈이 연결되었습니다.")
except Exception as e:                              # 예외 발생 시 종료
    print(f"포트 인식 안 됨: {e}")
    exit()
#---------------------------------------------------#




#-------------- 사용자 ID 입력 후 시작 ---------------#
userId = input("ID를 입력하세요 : ")
if findUser.validUser(f'{userId}'):
    print("인증되었습니다.")
    user = findUser.validUser(f'{userId}')          # user = 사용자 id(일련번호)
else:
    print("없는 사용자ID 입니다.")
    exit()
#---------------------------------------------------#




#------------------------------실시간 객체 탐지 시작---------------------------------#
cap = cv2.VideoCapture(2)           # 2번째 카메라로 비디오 실시간 캡처
frame_width = int(cap.get(3))       # 비디오 프레임의 너비
frame_height = int(cap.get(4))      # 비디오 프레임의 높이

out = cv2.VideoWriter('output.avi', cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'), 10, (frame_width, frame_height))  # 비디오 출력파일 생성, MJPG 코덱 사용, 초당 10프레임

model = YOLO("./YOLO-Weights/best_pothole_v2.pt")  # YOLO 모델 로드
classNames = ["PotHole"]                           # 탐지할 클래스 이름 정의

last_save_time = time.time()                       # 초 단위로 현재 시간을 저장
photo_count = 0                                    # 사진 카운터 초기화

while True:
    success, img = cap.read()             #카메라에서 현재 프레임을 읽고 성공여부 : success, 프레임 이미지 : img 에 반환
    results = model(img, stream=True)     #프레임 이미지를 model에 입력 후 처리결과를 results 에 저장(stream = true 는 스트리밍 모드에서 작동하도록 함)

    for r in results:
        boxes = r.boxes
        for box in boxes:
            x1, y1, x2, y2 = box.xyxy[0]  # 감지된 객체의 경계 상자 좌표를 가져옴

            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)
            print(x1, y1, x2, y2)
            cv2.rectangle(img, (x1, y1), (x2, y2), (255, 0, 255), 3)

            conf = math.ceil((box.conf[0] * 100)) / 100  # 신뢰도 계산
            cls = int(box.cls[0])  # 클래스 ID 가져옴
            class_name = classNames[cls]    # 클래스 이름을 가져옴
            label = f'{class_name} {conf}'  # 라벨 생성
            t_size = cv2.getTextSize(label, 0, fontScale=1, thickness=2)[0]

            c2 = x1 + t_size[0], y1 - t_size[1] - 3
            cv2.rectangle(img, (x1, y1), c2, [255, 0, 255], -1, cv2.LINE_AA)
            cv2.putText(img, label, (x1, y1 - 2), 0, 1, [255, 255, 255], thickness=1, lineType=cv2.LINE_AA)

            latitude, longitude = gpsModule.printGPS(sr)

            if class_name == "PotHole" and time.time() - last_save_time >= 5:
                formatted_time = time.strftime("%Y%m%d_%H%M%S", time.localtime())  # 현재 시각(20_13_33 형식)
                photo_name = f"pothole_{photo_count}_{formatted_time}.jpg"                  # 이미지 이름 설정
                cv2.imwrite(photo_name, img)                                                # 이미지 저장
                photo_count += 1
                sendImage.send(photo_name)                                                  # 서버에 이미지 전송
                sendToDB.create_potImage(latitude, longitude,
                                         "접수 중",
                                         formatted_time,
                                         f"/static/pothole_images/{photo_name}",
                                         user)                                              # DB에 정보 전송

                last_save_time = time.time()                                                # 마지막 저장 시간 갱신

    out.write(img)  # 비디오 파일에 프레임 저장
    cv2.imshow("Image", img)  # 처리된 프레임을 화면에 표시

    if cv2.waitKey(1) & 0xFF == ord('1'):  # 사용자가 1을 누르면 루프 종료
        break
#--------------------------------------------------------------------------------#

out.release()    #동영상 파일 쓰기 작업을 완료
cap.release()
cv2.destroyAllWindows() #모든 창을 닫음
