import RPi.GPIO as GPIO
from flask import Flask, render_template, request
app = Flask(__name__)

@app.route("/")
def main():
    templateData = {
        'cssV' : 'a',
        'faceJPG' : '',
        'info' : '보안을 시작하려면 시작 버튼을 누르시오'
    }
    return render_template('secretSecurity.html',**templateData)

app.route("/start")
def start_security():
    info = "감시작동중"

    #조도측정기가 밝아지면 카메라로 찰칵




