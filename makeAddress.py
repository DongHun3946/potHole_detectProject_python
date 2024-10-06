from geopy.geocoders import Nominatim

def address(latitude, longitude):

    try:
        # Nominatim 객체 생성
        geolocator = Nominatim(user_agent="geoapiExercises")

        # 위도와 경도로 주소 찾기
        location = geolocator.reverse((latitude, longitude))

        if location:
            address_components = location.address.split(", ")
            formatted_address = f"{address_components[3]} {address_components[2]} {address_components[1]} {address_components[0]} {address_components[4]} "
            return formatted_address
        else:
            return "주소 없음"

    except Exception as e: #예외 처리한 이유 : Nominatim은 API를 과도하게 호출할 경우 제한을 걸기 때문에
        return "API 요청 거부"


