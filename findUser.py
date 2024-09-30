import pymysql

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='9957', db='pothole', charset='utf8')
def validUser(userid):
    cur = conn.cursor()

    sql1 = f"SELECT id FROM user WHERE userid='{userid}'"
    cur.execute(sql1)
    result = cur.fetchone()

    if result:
        return result[0]
    else:
        return None
