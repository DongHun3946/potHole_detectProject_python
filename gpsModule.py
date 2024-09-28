import serial  #시리얼 통신을 처리하는 모듈
import serial.tools.list_ports #현재 컴퓨터에 연결된 포트 목록을 가져옴

def printGPS():
    def list_serial_ports():
        ports = serial.tools.list_ports.comports() #현재 시트템에 연결된 모든 시리얼 포트를 반환
        for port in ports:
            print(port.device)  #각 포트의 이름을 출력
    def dmm_to_dd(degrees, minutes):  #DMM 형식의 좌표를 DD 형식으로 변환
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
        try:
            recvpacket = sr.readline().decode()
            uart_split = recvpacket.split(",")
            if uart_split[0] == '$GPRMC':
                lat_dmm = uart_split[3]
                lon_dmm = uart_split[5]
                lat_dd, lon_dd = convert_coordinates(lat_dmm, lon_dmm)
                print(f"{lat_dmm} N, {lon_dmm} E -> {lat_dd:.6f} N, {lon_dd:.6f} E")
        except Exception as e:
            print(f"Error: {e}")

    print("사용가능한 시리얼 포트 : ")
    list_serial_ports()

    uart = []
    try:  #COM3에서 115200의 보드레이트로 시리얼 통신을 설정
        sr = serial.Serial("COM3", 115200)
    except Exception as e:  #예외 발생 시 종료
        print(f"Port Not Found: {e}")
        exit()
    while True:
        uart = ""
        uart_split = []
        work()


