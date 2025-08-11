'''
Date: 2024.01.31
Title:  Generate_Map_html(Get Webbrowser)
By: Kang Jin Seong
'''
import folium
import webbrowser
from folium.plugins import MousePosition
from math import sin, cos, sqrt, atan2, radians

def calculate_distance(lat1, lon1, lat2, lon2):
    '''
    지구상에서의 경도,위도를 근거로 하여 거리를 계산하는 함수\r\n
    Variable:
     __R: 지구의 근가 반지름
    Input:
     __lat1: 첫 번쨰 지점의 위도,long1: 첫 번째 지점의 경도
     __lat2: 두 번째 지점의 위도,long2: 두 번쨰 지점의 경도
    Return:
     _distance: 거리값
    '''
    R = 6373.0
    lat1 = radians(lat1);lat2 = radians(lat2)
    lon1 = radians(lon1);lon2 = radians(lon2)
    dlon = lon2 - lon1;dlat = lat2 - lat1
    a = sin(dlat / 2 )**2 + cos(lat1)*cos(lat2)*sin(dlon/2)**2
    c = 2* atan2(sqrt(a), sqrt(1-a))
    distance = R*c
    return distance

def Distance_center(x1,y1,x2,y2):
    return (x1+x2)/2, (y1+y2)/2 

def Mouse_Position_func(m):
    '''
    우측 상단에 마우스 상태의따라 위도,경도를 표시하는 함수\r\n
    Input:
     __m: 생성된 지도
    Return:
     __.add_to(m)
    '''
    formatter = "function(num) {return L.Util.formatNum(num, 5);};"
    MousePosition(
        position = 'topright',
        separator = ' Long: ',
        empty_string = 'NaN',
        lng_first = False,
        num_digits = 20,
        prefix = 'Lat: ',
        lat_formatter = formatter,
        lng_formatter = formatter
    ).add_to(m)

def Point_marker(m, sites=[]):
    '''
    생선된 지도에 위도,경도 값을 표시하는 함수\r\n
    lat, lng 값이 0이면 pass, 0이 아니면 해당 지점에 Marker 표시\r\n
    Variable:
     __index: 마커 툴팁에 표시되는 장비의 고유 번호
    Input:
     __m: 생성된 지도
     __sites: 위도,경도 값의 따른 리스트
    Return:
     __.add_to(m)
    '''
    index = 0
    for lat, lng in zip(sites[::2], sites[1::2]):
        index += 1
        if lat == 0 or lng == 0:
            pass
        else:
            folium.Marker(
                [lat, lng],
                popup = f'위도(N): {lat},경도(E): {lng}',
                tooltip = f'Costal_Tomography_TMC_Set_{index}',
                icon = folium.Icon(
                    color = 'red',
                    icon_color = 'blue',
                    icon = 'cloud'
                )
            ).add_to(m)

def Point_line(m, sites=[]):
    '''
    생성된 지도에 두 지점 사이의 선을 그어주는 함수\r\n
    folium.Marker를 이용하여 두 지점 사이의 중간지점에 거리를 표시\r\n
    folium.Polyline를 이용하여 두 지점 사이를 선으로 연결\r\n
    variable:
     __lat_lng_list: 위도 경도 값을 한 쌍으로 설정하여 가독성을 높이는 변수
    Input:
     __m: 생성된 지도
     __sites: 위도,경도의 따른 리스트
    Return:
     __add_to(m)
    '''
    lat_lng_list = []
    for lat, lng in zip(sites[::2], sites[1::2]):
        lat_lng_list.append([lat, lng])
    for i in lat_lng_list:
        for j in lat_lng_list[lat_lng_list.index(i):]:
            if i != j:
                if i[0] != 0 and j[0] != 0:
                    distance = calculate_distance(i[0],i[1],j[0],j[1])
                    distance_x , distance_y = Distance_center(i[0],i[1],j[0],j[1])
                    folium.Marker(
                        [distance_x,distance_y], 
                        icon = folium.DivIcon(
                            icon_size = (20,20),
                            icon_anchor = (0,0),
                            html = '<div style="font-size: 1.5rem; color:red;"><b>%s</b></div>' % "{:10.2f}kM".format(distance)
                        )
                    ).add_to(m)
                    folium.PolyLine(
                        locations=[
                            [i[0],i[1]],[j[0],j[1]]
                        ],
                        weight = 2
                    ).add_to(m)
                else:
                    pass
            else:
                pass

def Mapping(sites=[],zomm=14):
    '''
    Map 생성 블럭 함수로써 입력된 위도,경도 값의 한점을 중심으로 내부 변수인 zoo_Start값을 이용하여
    Map을 출력한다.\r\n
    variable:
     __zoom: 지도 생성시 zoom 값(default:14)
    Input:
     __sites: 위도,경도의 따른 리스트
    Return:
     __folium.Map()
    '''
    for lat, lng in zip(sites[::2], sites[1::2]):
        if lat != 0 and lng != 0:
            return folium.Map(location=[lat, lng], zoom_start=zomm)

def Map(path, IN=[]):
    sites = IN
    new_path = path+f'/Map.html'
    '''
    Map 생성블락: nans_map
    ''' 
    nasa_map = Mapping(sites)
    '''
    지도에 장비 마커 표시 블락
    '''
    Point_marker(nasa_map, sites)
    '''
    지도의 우측상단에 마우스 포인트 표시 블락
    '''
    Mouse_Position_func(nasa_map)
    '''
    지도에 두 지점사이의 거리 및 선 표시 블락
    '''
    Point_line(nasa_map,sites)
    '''
    생성된 지도는 .html로 저장되어 브라우저로 실행된다.
    '''
    nasa_map.save(new_path)
    webbrowser.open(new_path)
