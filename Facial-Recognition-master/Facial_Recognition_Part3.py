#https://github.com/codeingschool/Facial-Recognition.git
#https://blog.naver.com/chandong83/221695462391
import cv2
import numpy as np
from os import listdir
from os.path import isfile, join

face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

#사용자 얼굴 학습
def trains():
    data_path = 'faces/'
    #faces폴더에 있는 파일 리스트 얻기
    onlyfiles = [f for f in listdir(data_path) if isfile(join(data_path,f))]
    #데이터와 매칭될 라벨 변수
    Training_Data, Labels = [], []
    #파일 개수 만큼 루프
    for i, files in enumerate(onlyfiles):
        image_path = data_path + onlyfiles[i]
        #이미지 불러오기
        images = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        #이미지 파일이 아니거나 못 읽어 왔다면 무시
        if images is None:
            continue
        #Training_Data 리스트에 이미지를 바이트 배열로 추가
        Training_Data.append(np.asarray(images, dtype=np.uint8))
        #Labels 리스트엔 카운트 번호 추가
        Labels.append(i)
    #훈련할 데이터가 없다면 종료.
    if len(Labels) == 0:
        print("There is no data to train.")
        exit()
    #Labels를 32비트 정수로 변환
    Labels = np.asarray(Labels, dtype=np.int32)
    #모델 생성
    #model = cv2.face.LBPHFaceRecognizer_create()
    model = cv2.face.LBPHFaceRecognizer_create ()
    #학습
    model.train(np.asarray(Training_Data), np.asarray(Labels))
    print("Model Training Complete!!!!!")

#얼굴 검출
def face_detector(img, size = 0.5):
    # 흑백처리
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # 얼굴 찾기
    faces = face_classifier.detectMultiScale(gray,1.3,5)
    # 찾은 얼굴이 없으면
    if faces is():
        return img,[]
    for(x,y,w,h) in faces:
        # 얼굴 크기만큼
        cv2.rectangle(img, (x,y),(x+w,y+h),(0,255,255),2)
        roi = img[y:y+h, x:x+w]
        roi = cv2.resize(roi, (200,200))
    return img,roi   #검출된 좌표에 사각 박스 그리고(img), 검출된 부위를 잘라(roi) 전달

#인식 시작
def run(model):
    #카메라 열기
    cap = cv2.VideoCapture(0)

    while True:
        #카메라로 부터 사진 한장 읽기
        ret, frame = cap.read()
        # 얼굴 검출 시도
        image, face = face_detector(frame)
        try:
            #검출된 사진을 흑백으로 변환
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            #위에서 학습한 모델로 예측시도
            result = model.predict(face)
            #result[1]은 신뢰도이고 0에 가까울수록 자신과 같다는 뜻이다.
            if result[1] < 500:
                #????? 어쨋든 0~100표시하려고 한듯
                confidence = int(100*(1-(result[1])/300))
                # 유사도 화면에 표시
                display_string = str(confidence)+'% Confidence it is user'
            cv2.putText(image,display_string,(100,120), cv2.FONT_HERSHEY_COMPLEX,1,(250,120,255),2)
            #75 보다 크면 동일 인물로 간주해 UnLocked!
            if confidence > 75:
                cv2.putText(image, "Unlocked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 255, 0), 2)
                cv2.imshow('Face Cropper', image)
            else:
                #75 이하면 타인.. Locked!!!
                cv2.putText(image, "Locked", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (0, 0, 255), 2)
                cv2.imshow('Face Cropper', image)
        except:
            #얼굴 검출 안됨
            cv2.putText(image, "Face Not Found", (250, 450), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0), 2)
            cv2.imshow('Face Cropper', image)
            pass
        if cv2.waitKey(1)==13:
            break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    model = trains()
    run(model)