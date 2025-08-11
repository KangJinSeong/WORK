import folium
import webbrowser

def result():
    m = folium.Map(location=[37.5072384, 127.0238756], zoom_start=14)
    folium.Marker([37.5072384, 127.0238756],
                popup='Station정보\n\rNumber:#1\n\rOrder:12\n\r경원산업\n\r강진성입니다.\r\n',
                tooltip='Costal_Tomography_TMC_Set_1',
                icon=folium.Icon(
                    color='red',
                    icon_color='blue',
                    icon='cloud'
                    )
    ).add_to(m)

    folium.Marker([37.1, 127.8],
                popup='경도:37.5072n\r위:127.023\n\r 안녕하세n\r 경원산업 강진성입니다.\r\n<b>',
                tooltip='Costal_Tomography_TMC_Set_2',
                icon=folium.Icon(
                    color='red',
                    icon_color='blue',
                    icon='cloud'
                    )
    ).add_to(m)
    m.save('index.html')

    webbrowser.open('file:///C:/Users/USER/Desktop/CATS/5.%20Python/index.html',new=0)


distance1to2 = calculate_distance(sites[0], sites[1], sites[2], sites[3])
distance1to2_x, distance1to2_y = Distance_center(sites[0], sites[1], sites[2], sites[3])
distance_marker = folium.Marker(
    [distance1to2_x, distance1to2_y],
    icon = folium.DivIcon(
        icon_size = (20000,20000),
        icon_anchor = (0,0),
        html = '<div style="font-size: 1.2rem; color:red;"><b>%s</b></div>' % "{:10.2f}kM\r\n1to2".format(distance1to2),
    )
)
nasa_map.add_child(distance_marker)
lines = folium.PolyLine(
    locations=[
        [sites[2], sites[3]], [sites[0], sites[1]],
    ],
    weight = 1
)
nasa_map.add_child(lines)