from datetime import datetime
import makeAddress
import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='9957', db='pothole', charset='utf8')

def create_potImage(latitude, longitude, state, detectDate, imagePath, user):
    cur = conn.cursor()   #db와 연결해주는 통로 역할

    detect_date = datetime.strptime(detectDate, '%Y%m%d_%H_%M_%S')

    if latitude != 0.0 and longitude != 0.0:
        sql = f'''INSERT INTO pothole (address, detect_date, latitude, longitude, state, user_id, image_path) 
              VALUES ('{makeAddress.address(latitude, longitude)}', '{detect_date}', {latitude}, {longitude}, '{state}', {user}, '{imagePath}')'''

        cur.execute(sql)  # sql 실행
        conn.commit()     # 실제 db에 적용
        cur.close()       # 커서를 닫음
        conn.close()      # 연결을 닫음
        print("정상적으로 값이 전송되었습니다.")
    else:
        cur.close()       # 커서를 닫음
        conn.close()      # 연결을 닫음
        print("GPS 인식이 원활치않아 DB에 전송하지 못했습니다.")

