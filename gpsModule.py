import serial  # 시리얼 통신을 처리하는 모듈


def printGPS(sr):
    def dmm_to_dd(degrees, minutes):  # DMM 형식의 좌표를 DD 형식으로 변환
        return degrees + minutes / 60

    def convert_coordinates(lat_dmm, lon_dmm):  # DMM 형식의 위도와 경도를 DD 형식으로 변환
        lat_degrees = int(lat_dmm[:2])
        lat_minutes = float(lat_dmm[2:])
        lon_degrees = int(lon_dmm[:3])
        lon_minutes = float(lon_dmm[3:])

        latitude = dmm_to_dd(lat_degrees, lat_minutes)
        longitude = dmm_to_dd(lon_degrees, lon_minutes)
        return latitude, longitude

    while True:  # 유효한 데이터가 나올 때까지 반복
        recvpacket = sr.readline().decode()
        uart_split = recvpacket.split(",")
        if uart_split[0] == '$GPRMC':  # $GPRMC 메시지만 처리
            if uart_split[2] == 'A':  # 상태 플래그 'A'는 유효한 데이터
                lat_dmm = uart_split[3]
                lon_dmm = uart_split[5]
                if lat_dmm and lon_dmm:  # 위도와 경도가 존재하는지 확인
                    lat_dd, lon_dd = convert_coordinates(lat_dmm, lon_dmm)
                    return lat_dd, lon_dd
        # 유효하지 않은 데이터를 받은 경우 다시 읽기