import paho.mqtt.subscribe as subscribe
topics = 'KWFI/3D/BDDATA/Update'
broker = "test.mosquitto.org"

def Mqtt_Subscribe():
    '''
    Coastal Acoustic Tomography Gui와 연동하기 위한 Python 코드로써 Mqtt_Subscribe()의 주된
    내용은 Subscribe 함수의 Simple을 이용하여 데이터가 들어올때마다 값을 Return해주는 함수이다.
    
    input: None
    Output: m.payload.docode()

    '''
    try:
        m = subscribe.simple(topics, hostname= broker, retained= False, keepalive=20)
        return m.payload.decode()
    except Exception as e:
        print(f"Error : {e}")

if __name__=='__main__':
    while True:
        print(Mqtt_Subscribe())
