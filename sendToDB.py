from datetime import datetime

import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='9957', db='pothole', charset='utf8')


def create_potImage(latitude, longitude, address, state, detectDate, imagePath, user):
    cur = conn.cursor()

    detect_date = datetime.strptime(detectDate, '%Y%m%d_%H%M%S')

    sql = f'''INSERT INTO pothole (address, detect_date, latitude, longitude, state, user_id, image_path) 
              VALUES ('{address}', '{detect_date}', {latitude}, {longitude}, '{state}', {user}, '{imagePath}')'''

    cur.execute(sql)
    conn.commit()
    cur.close()  # 커서를 닫아줍니다.
    conn.close()  # 연결을 닫아줍니다.
    print("정상적으로 값이 전송되었습니다.")

# 예시 호출
create_potImage(36.5000, 127.5000, "", "접수 중", "20240928_142530", "/static/pothole_images/pothole1", 9)
