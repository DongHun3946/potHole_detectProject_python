from geopy.geocoders import Nominatim

def address(latitude, longitude):

    # Nominatim 객체 생성
    geolocator = Nominatim(user_agent="geoapiExercises")

    # 위도와 경도로 주소 찾기
    location = geolocator.reverse((latitude, longitude))

    # 결과 출력
    if location:
        # 주소를 쉼표로 분리
        address_components = location.address.split(", ")
        formatted_address = f"{address_components[4]} {address_components[3]} {address_components[2]} {address_components[1]} {address_components[0]} {address_components[-2]}"
        return formatted_address
    else:
        return "주소 없음"

