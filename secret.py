
import RPi.GPIO as GPIO
from flask import Flask, render_template, request
import time
import picamera

app = Flask(__name__)


SPICLK = 11
SPIMISO = 9
SPIMOSI = 10
SPICS = 8

photo_ch = 0

#새로고침할때 계속 사진이 바뀌는걸 도와주는 코드
@app.after_request
def add_header(response):
    """
    Add headers to both force latest IE rendering engine or Chrome Frame,
    and also to cache the rendered page for 10 minutes.
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

#조도측정
def readadc(adcnum, clockpin, mosipin, misopin, cspin):
    if ((adcnum > 7) or (adcnum < 0)):
        return -1
    GPIO.output(cspin, True)
    GPIO.output(clockpin, False)
    GPIO.output(cspin, False)
    commandout = adcnum
    commandout |= 0x18
    commandout <<= 3
    for i in range(5):
        if (commandout & 0x80):
            GPIO.output(mosipin, True)
        else:
            GPIO.output(mosipin, False)
        commandout <<= 1
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)

    adcout = 0
    for i in range(12):
        GPIO.output(clockpin, True)
        GPIO.output(clockpin, False)
        adcout <<= 1

        if (GPIO.input(misopin)):
            adcout |= 0x1

    GPIO.output(cspin, True)
    adcout >>= 1
    return adcout

@app.route("/")
def main():
    templateData = {
        'image_files' : '',
        'info' : '보안을 시작하려면 시작 버튼을 누르시오'
    }
    return render_template('secretSecurity.html',**templateData)

@app.route("/start")
def start_security():
    GPIO.setwarnings(False)
    GPIO.cleanup()
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(SPIMOSI, GPIO.OUT)
    GPIO.setup(SPIMISO, GPIO.IN)
    GPIO.setup(SPICLK, GPIO.OUT)
    GPIO.setup(SPICS, GPIO.OUT)
    oldLight = 0
    image_files = {}
    i =1;
    while True:
        newLight=readadc(photo_ch, SPICLK, SPIMOSI, SPIMISO, SPICS) #조도측정
        newLight = newLight/11
        print("n: %d" % newLight)
        print("o: %d" % oldLight)
        time.sleep(0.2)
        if newLight+1 < oldLight: #밝기가 밝아지면 숫자가 낮아짐
            print("밝아짐")
            camera = picamera.PiCamera()
            camera.resolution=(800,600)
            image_files[i] = "img"+str(i)+".jpg"
            print(image_files[i])
            camera.capture("static/"+image_files[i])
            time.sleep(1)
            camera.close()
            i=i+1
            #사람 이미지 비교
            break
        oldLight = newLight

    print("끝")
    templateData = {
        'image_files': image_files,
        'info': "감시작동중"
    }
    return render_template('secretSecurity.html', **templateData)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80, debug=True)


