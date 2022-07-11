from flask import Flask, render_template, jsonify, request
import time
import board  # 데이터 송신용 board모듈
import adafruit_dht
import os

condition = False
mydht11 = adafruit_dht.DHT11(board.D20)  # D20 = gpio 핀 번호
hope_temperature = 18  # 희망온도 범위 18°C~20°C

app = Flask(__name__)


def get_dht_data():
    while True:
        try:
            temperature, humidity = mydht11.temperature, mydht11.humidity
            if temperature is not None and humidity is not None:
                return temperature, humidity
            else:
                raise
        except:
            time.sleep(0.5)


@app.route('/update', methods=['post'])
def status():
    temperature, humidity = get_dht_data()
    global hope_temperature
    return jsonify({
        'temperature': temperature,
        'humidity': humidity,
        'ho_temp': hope_temperature
    })


@app.route('/')
def mainpage():
    return render_template("homepage.html")


@app.route('/control', methods=['POST'])
def control():
    global condition
    global hope_temperature
    data = request.get_json()
    if(data['on/off'] == 1):  # aircon ON
        if condition == False:
            os.chdir("/home/q201711097")
            os.system("sudo pigpiod")
            condition = True
        else:
            os.system("python irrp.py -p -g22 -fir-codes 1")
    elif data['on/off'] == 2:  # aircon OFF
        os.system("python irrp.py -p -g22 -fir-codes 2")
    elif data['on/off'] == 'none' and data['up/down'] == 'up':
        if(hope_temperature == 18):
            hope_temperature += 1
            os.system("python irrp.py -p -g22 -fir-codes 3")
        elif(hope_temperature == 19):
            hope_temperature += 1
            os.system("python irrp.py -p -g22 -fir-codes 4")
        elif(hope_temperature == 20):
            hope_temperature += 1
            os.system("python irrp.py -p -g22 -fir-codes 5")
        elif(hope_temperature == 21):
            hope_temperature += 1
            os.system("python irrp.py -p -g22 -fir-codes 6")
        elif(hope_temperature == 22):
            hope_temperature += 1
            os.system("python irrp.py -p -g22 -fir-codes 7")
        elif(hope_temperature == 23):
            hope_temperature += 1
            os.system("python irrp.py -p -g22 -fir-codes 8")
        elif(hope_temperature == 24):
            hope_temperature += 1
            os.system("python irrp.py -p -g22 -fir-codes 9")
        elif(hope_temperature == 25):
            hope_temperature += 1
            os.system("python irrp.py -p -g22 -fir-codes 10")
    elif data['on/off'] == 'none' and data['up/down'] == 'down':
        if(hope_temperature == 19):
            hope_temperature -= 1
            os.system("python irrp.py -p -g22 -fir-codes 18")
        elif(hope_temperature == 20):
            hope_temperature -= 1
            os.system("python irrp.py -p -g22 -fir-codes 17")
        elif(hope_temperature == 21):
            hope_temperature -= 1
            os.system("python irrp.py -p -g22 -fir-codes 16")
        elif(hope_temperature == 22):
            hope_temperature -= 1
            os.system("python irrp.py -p -g22 -fir-codes 15")
        elif(hope_temperature == 23):
            hope_temperature -= 1
            os.system("python irrp.py -p -g22 -fir-codes 14")
        elif(hope_temperature == 24):
            hope_temperature -= 1
            os.system("python irrp.py -p -g22 -fir-codes 13")
        elif(hope_temperature == 25):
            hope_temperature -= 1
            os.system("python irrp.py -p -g22 -fir-codes 12")
        elif(hope_temperature == 26):
            hope_temperature -= 1
            os.system("python irrp.py -p -g22 -fir-codes 11")

    return jsonify(data)


if __name__ == "__main__":
    app.run(host='0.0.0.0')
