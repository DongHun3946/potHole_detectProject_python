def printGPS(sr):
    def dmm_to_dd(degrees, minutes):      #DMM 형식의 좌표를 DD 형식으로 변환
        return degrees + minutes / 60
    def convert_coordinates(lat_dmm, lon_dmm): #DMM형식의 위도와 경도를 DD형식으로 변환
        lat_degrees = int(lat_dmm[:2])
        lat_minutes = float(lat_dmm[2:])
        lon_degrees = int(lon_dmm[:3])
        lon_minutes = float(lon_dmm[3:])

        latitude = dmm_to_dd(lat_degrees, lat_minutes)
        longitude = dmm_to_dd(lon_degrees, lon_minutes)
        return latitude, longitude
    def work(): #시리얼 포트에서 데이터를 읽고 NMEA 프로토콜의 $GPRMC 메시지를 처리하여 GPS 좌표를 변환
        global uart
        global uart_split

        recvpacket = sr.readline().decode()
        uart_split = recvpacket.split(",")
        if uart_split[0] == '$GPRMC':
            lat_dmm = uart_split[3]
            lon_dmm = uart_split[5]
            lat_dd, lon_dd = convert_coordinates(lat_dmm, lon_dmm)
            return lat_dd, lon_dd
        else:
            return 0.0, 0.0

    uart = []
    while True:
        uart = ""
        uart_split = []
        work()

