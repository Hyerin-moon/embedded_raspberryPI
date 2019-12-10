'''
기말프로젝트 13조(문혜린)
flask + python + html 사용을 기본으로 함
프로젝트 명: secret box
1. 조도센서로 빛의 밝기측정
2. 카메라로 사진 촬영
3. 사진 속 얼굴과 사용자 얼굴 비교
4. 웹페이지로 알람 전송
'''

from flask import Flask, render_template, request
import time

app = Flask(__name__)

index = 0
image_files = {} #이미지 파일 저장

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

@app.route("/")
def main():
    print("main 불림")
    global image_files
    global index
    image_files.clear()
    index = 0 #이거 없애면 계속 다른 이미지로 저장됨
    templateData = {
        'image_files' : '',
        'info' : '보안을 시작하려면 시작 버튼을 누르시오'
    }
    return render_template('secretSecurity.html',**templateData)

@app.route("/pause")
def pause():
    global image_files
    global index
    templateData = {
        'state': 'pause',
        'image_files': image_files,
        'info': "감시 일시정지"
    }
    return render_template('secretSecurity.html', **templateData)


@app.route("/start")
def start_security():
    global image_files
    global index
    for i in range(1,1001):
        if index ==0: break
        print(i)
        #조도측정
        if i%50 == 0:
            image_files[index] = "img" + str(index) + ".jpg"
            print(image_files[index])
            time.sleep(1)
            break
    if index != 0:
        #led 경고등
        print("led"+str(index))
    index = index + 1
    templateData = {
        'state': 'true',
        'image_files': image_files,
        'info': "감시작동중"
    }
    return render_template('secretSecurity.html', **templateData)


if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000, debug=True)


