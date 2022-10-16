import cv2
import time
import math

#centro do alvo
p1=550
p2=150

#trajetória
dx = []
dy = []

vid = cv2.VideoCapture("soccer.mp4")
tracker = cv2.TrackerCSRT_create()
returned,img = vid.read() #ler o 1o frame do video

#ROI=Region of Interest
box = cv2.selectROI("Tracking...",img,False)
tracker.init(img, box)
print(box)

def drawBox(img,box):
    #4 valores inteiros para fazer o quadrado
    x,y,w,h = int(box[0]), int(box[1]), int(box[2]), int(box[3])
    cv2.rectangle(img,(x,y),((x+w),(y+h)),(255,0,255),3,1)
    cv2.putText(img,"Tracking...",(150,90),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,0,255),2)

def goal(img,box):
    x,y,w,h=int(box[0]), int(box[1]), int(box[2]), int(box[3])
    #centro do quadrado
    c1=x+int(w/2)
    c2=y+int(h/2)
    cv2.circle(img,(c1,c2),2,(0,255,0),5)

    cv2.circle(img, (int(p1),int(p2)), 2, (0,255,255), 3)
    dist=math.sqrt(((c1-p1)**2) + ((c2-p2)**2))
    print(dist)

    if(dist<=20):
        cv2.putText(img,"Congrats!",(650,300),cv2.FONT_HERSHEY_COMPLEX, 1, (169,0,253), 2)

    dx.append(c1)
    dy.append(c2)

    for i in range(len(dx)-1):
        cv2.circle(img,(dx[i],dy[i]),1,(0,252,0),5)

while True:
    check,img = vid.read()
    success,box=tracker.update(img) #manter o quadrado em todos os frames
    
    if success:
        drawBox(img, box)
    else:
        cv2.putText(img,"Error",(75,90),cv2.FONT_HERSHEY_COMPLEX, 0.7, (178,34,34), 2)


    goal(img,box)
    cv2.imshow("result",img)

    key = cv2.waitKey(25)
    if key == 32:
        print("Pause")
        break


vid.release()
cv2.destroyAllWindows()