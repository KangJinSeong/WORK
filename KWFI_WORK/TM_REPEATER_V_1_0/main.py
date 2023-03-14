from Subpy import GPS_V_1_0, TRX_Controller_Swtich, TRX_Triger #하드웨어 조작 관련 모듈


if __name__ == "__main__":
    compas = GPS_V_1_0.GPS_HAT()
    lat, lon = compas.main()
    