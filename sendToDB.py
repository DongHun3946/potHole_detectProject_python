from datetime import datetime
import makeAddress
import pymysql



def create_potImage(latitude, longitude, state, detectDate, imagePath, user):
    conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='9957', db='pothole', charset='utf8')
    try:
        cur = conn.cursor()   #db와 연결해주는 통로 역할
        detect_date = datetime.strptime(detectDate, '%Y%m%d_%H%M%S')

        sql = f'''INSERT INTO pothole (address, detect_date, latitude, longitude, state, user_id, image_path) 
              VALUES ('{makeAddress.address(latitude, longitude)}', '{detect_date}', {latitude}, {longitude}, '{state}', {user}, '{imagePath}')'''

        cur.execute(sql)  # sql 실행
        conn.commit()     # 실제 db에 적용
        cur.close()  # 커서를 닫음
    except pymysql.MySQLError as e:
        print(f"Error: {e}")
    finally:
        conn.close()  # 연결을 닫음


