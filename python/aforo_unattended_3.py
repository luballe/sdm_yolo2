#!/usr/bin/python2
from darknet import *
from Counter import linecounter as lc
from Track import tracking as tr
from time import sleep
import cv2
import os
import easygui
import pickle
import sys

import glob
import random
 
#primera vez
charlador=False
pintarTrayectos=False

SALVARCONTADO=False
contimagen=1


framesttl=10
deCamara=False
MAXW=1400 ## 200 pixeles maximo de ancho permitido
mindist=150


def getimage(capture,withroi=False,roi=None):
    """
    para uso normal cambiar:
    ret_val, imgFile2 = cam.read()
    por
    
    ret_val, imgFile2 = getimage(cam,withroi=WITHROI,roi=roi)
    """
    if withroi:
        ret_val, imgFile = capture.read()
        if ret_val:
            if roi==None:
                print("ERROR: por favor si activa seleccion de ROI entre una ROI")
            else:
                imgFile2=imgFile[roi[1]:roi[1]+roi[3],roi[0]:roi[0]+roi[2]]
        else:
            imgFile2=imgFile
    else:
        ret_val, imgFile2 = capture.read()
    
    return  ret_val, imgFile2




#folder=easygui.diropenbox(title="Seleccione la carpeta con los videos a aforar",default="/media/francisco/monitoreo")
print(sys.argv)
#folder=sys.argv[1]
video_path=sys.argv[1]
pickle_path=sys.argv[2]
if os.path.isfile(pickle_path):
    with open(pickle_path) as f:  # Python 3: open(..., 'rb')
        lineasDeConteo, lineasDeConteoCondicional, lineaDeConteo,lineaDeConteoCondicional = pickle.load(f)


#ROI Selection in Frame consist in an archive called ROI.txt with a tuple in the first and only line in file, that is the ROI. 
#In notation (X,Y,width,heigth), X and y are the upper left coordinate of the Region Of Interest ROI
#WITHROI=os.path.isfile(folder+"/ROI.txt")
WITHROI=None
roi=None
#NUESTRO YOLO ENTRENADO 80000 iteraciones
net = load_net("../yolo-obj.cfg", "../../weights/yolo-obj_final.weights", 0)
meta = load_meta("../data/obj.data")
        
print("Aforando "+video_path)
counterarchivos=1
    
fn=video_path
counterarchivos+=1
cam = cv2.VideoCapture(fn)
ruta,ext=os.path.splitext(fn)
archsal=ruta+'.csv'     
print ('Archivo de salida: '+archsal)
frames=0
ret_val, imgFile2 = getimage(cam,withroi=WITHROI,roi=roi)
frames+=1
if not ret_val:
    print ('ERROR: no se pudo abrir el archivo de video guardando registro, intentando siguiente')
    with open(folder+"/"+"Error.txt","a") as f:  # Python 3: open(..., 'rb')
        f.write("Error en archivo: "+fn+"\n")
    #continue
    exit()

imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)
tama=imgFile2.shape
imgImported=make_image(tama[1],tama[0],tama[2])

imgFileptr,cv_img=get_iplimage_ptr(imgFile3)    
ipl_in2_image(imgFileptr,imgImported)
rgbgr_image(imgImported)

track=tr.tracking(verbose=charlador,mindist=mindist,framesttl=framesttl)#verbose=False,mindist=100


contadores=[]
cc=1
for linlin in lineaDeConteo:
    contadores.append(lc.counter(linlin.pt1,linlin.pt2,filename=archsal,linecount=cc,fps=20))
    cc+=1

#CONTEOCONDICIONAL
contadoresCondicionales=[]
cc=1
for linlinc in lineaDeConteoCondicional:
    contadoresCondicionales.append(lc.conditionalCounter(linlinc.pt1,linlinc.pt2,linlinc.pt3,linlinc.pt4,filename=archsal,linecount=cc,fps=20))
    cc+=1
#FINCONTEOCONDICIONAL

while True:
    #ret_val, imgFile2 = cam.read()
    ret_val, imgFile2 = getimage(cam,withroi=WITHROI,roi=roi)
    frames+=1
    if not ret_val:
        print ("Fin del video o salida en camara, saliendo")
        cv2.imwrite('ultimofotogramaprocesado.jpg',imgFile3)
        break
    
    if SALVARCONTADO:
        copiaimagen=imgFile2.copy()
    segframes=cam.get(cv2.cv.CV_CAP_PROP_POS_FRAMES)
    tiempoactual=cam.get(cv2.cv.CV_CAP_PROP_POS_MSEC)*20.0/30.0
    imgFile3 = cv2.cvtColor(imgFile2,cv2.COLOR_BGR2RGB)
    #imgFile3 = cv2.imread("../data/eagle2.jpg")
    tama=imgFile3.shape
    #imgImported=make_image(tama[1],tama[0],tama[2])
    imgFileptr=copy_iplimage_ptr(imgFile3,imgFileptr,cv_img)
    
    ipl_in2_image(imgFileptr,imgImported)
    #save_image(imgImported,"dog_detect")
    r = detect_img(net, meta, imgImported) 
    if charlador:
        print ('Detecciones: '+str(len(r)))
        print (r)
        
        for i in range(len(r)):
            w=int(r[i][2][2])
            h=int(r[i][2][3])
            x=int(r[i][2][0])-w/2
            y=int(r[i][2][1])-h/2
            #cv2.rectangle(imgFile2, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
    
    for i in range(len(r)):
        if r[i][2][2]<MAXW:
            track.insertNewObject(r[i][2][0],r[i][2][1],r[i][2][2],r[i][2][3],strFeature=r[i][0])
        #else:
            #print ("        eliminado objeto por tamanio= ",r[i][2][2])
        #w=int(r[i][2][2])
        #h=int(r[i][2][3])
        #x=int(r[i][2][0])-w/2
        #y=int(r[i][2][1])-h/2
            
    if charlador:
        print('Antes de procesar')
        track.printObjets()
        track.printPaths()
        
    track.processObjectstoPaths()

    for j in (range(len(track.p.p[:]))):
        x=int(track.p.p[j].rect.x)
        y=int(track.p.p[j].rect.y)
        u=int(track.p.p[j].rect.u)
        v=int(track.p.p[j].rect.v)
        cv2.rectangle(imgFile2, (x,y), (u,v),track.p.p[j].colour, thickness=4, lineType=8, shift=0)
        if track.p.p[j].contado:
            cv2.putText(imgFile2,str(track.p.p[j].str), (int(track.p.p[j].cp.x),int(track.p.p[j].cp.y)), cv2.FONT_HERSHEY_SIMPLEX,1, (0,0,255))
        else:
            cv2.putText(imgFile2,str(track.p.p[j].str), (int(track.p.p[j].cp.x),int(track.p.p[j].cp.y)), cv2.FONT_HERSHEY_SIMPLEX,1, (255,255,255))
    if charlador:
        print('Despues de procesar')
        track.printPaths()

    #Falta graficar los dos ultimos puntos de los paths procesados
    #y si estos pasan la linea de conteo se suma uno
    
    for contar in contadores:
        cv2.circle(imgFile2,contar.point1,3,(0,0,255),-1)
        cv2.line(imgFile2,contar.point1,contar.point2,(0,0,255),1)
        cv2.circle(imgFile2,contar.point2,3,(255,0,255),-1)
        
        
    #CONTEOCONDICIONAL
    for contar in contadoresCondicionales:
        cv2.circle(imgFile2,contar.point1,3,(0,0,255),-1)
        cv2.line(imgFile2,contar.point1,contar.point2,(0,0,255),1)
        cv2.circle(imgFile2,contar.point2,3,(255,0,255),-1)
        cv2.circle(imgFile2,contar.point3,3,(255,255,255),-1)
        cv2.line(imgFile2,contar.point3,contar.point4,(255,255,255),1)
        cv2.circle(imgFile2,contar.point4,3,(255,255,255),-1)
    #FINCONTEOCONDICIONAL                
        
    # contar los que trayectos que pasen las lineas de conteo
    for idx in range(len( track.p.p)):
        if len(track.p.p[idx].path)>2: # si la longitud del path es mayor a dos
            # toma los dos registros mas recientes y los prueba si pasaron la linea de conteo
            p1=(int(track.p.p[idx].path[-1].x),int(track.p.p[idx].path[-1].y))#mas reciente (cuadro actual)
            p2=(int(track.p.p[idx].path[-2].x),int(track.p.p[idx].path[-2].y))#anterior     (cuadro anterior)
            cv2.line(imgFile2,p1,p2,track.p.p[idx].colour,1)

            for contar in contadores:
                if (contar.testLine(p2,p1) and not track.p.p[idx].contadores[contar.linecount]):
                    direct=contar.crossSign(p2,p1)
                    cv2.circle(imgFile2,contar.intersectPoint(p2,p1),4,(100,255,255), -1) #intersecting point
                    track.p.p[idx].contado=True
                    track.p.p[idx].contadores[contar.linecount]=1
                    contar.addToLineCounter(str(track.p.p[idx].str),frames,tiempoactual,direct)
                    if SALVARCONTADO:
                        imfilesave=folder+"/"+track.p.p[idx].str+'_'+str(contimagen)+'_'+str(random.randint(1000,10000))+'.JPG'
                        cx=int(track.p.p[idx].rect.x)
                        cy=int(track.p.p[idx].rect.y)
                        cu=int(track.p.p[idx].rect.u)
                        cv=int(track.p.p[idx].rect.v)
                        cw=int(track.p.p[idx].tam.w)
                        ch=int(track.p.p[idx].tam.h)
                        cv2.imwrite(imfilesave,copiaimagen[cy:cv,cx:cu])
                        contimagen=contimagen+1
            #CONTEOCONDICIONAL    
            for contard in contadoresCondicionales:
                esl1=contard.testLine1(p2,p1)
                esl2=contard.testLine2(p2,p1)

                if esl1:
                    track.p.p[idx].contadoresCondicionales[contard.linecount1]+=1
                    cv2.circle(imgFile2,contard.intersectPoint1(p2,p1),4,(100,100,255), -1) #intersecting point

                if track.p.p[idx].contadoresCondicionales[contard.linecount1]>=1 and track.p.p[idx].contadoresCondicionales[contard.linecount2]<1:# Lo pongo aqui para evitar bug en el que se cuente en las dos lineas al mismo tiempo,
                    track.p.p[idx].direccionCondicional=1

                if esl2:
                    track.p.p[idx].contadoresCondicionales[contard.linecount2]+=1
                    cv2.circle(imgFile2,contard.intersectPoint2(p2,p1),4,(100,255,100), -1) #intersecting point

                if track.p.p[idx].contadoresCondicionales[contard.linecount1]<1 and track.p.p[idx].contadoresCondicionales[contard.linecount2]>=1:
                    track.p.p[idx].direccionCondicional=-1

                if track.p.p[idx].contadoresCondicionales[contard.linecount1]>=1 and track.p.p[idx].contadoresCondicionales[contard.linecount2]>=1 and track.p.p[idx].direccionCondicional>=0:
                    if not track.p.p[idx].contadocondicional:
                        track.p.p[idx].contadocondicional=True
                        contard.addToLineCounter(str(track.p.p[idx].str),frames,tiempoactual)
            #CONTEOCONDICIONAL
                
    if pintarTrayectos:
        track.drawPaths(imgFile2)
    
    
    #cv2.imshow('Video', imgFile2)
    #k = cv2.waitKey(2)& 0xFF
    #if k==ord('q'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
    #    print ('interrupcion de usuario...')
    #    break

for contar in contadores:
    contar.saveFinalCounts(frames)
    
#CONTEOCONDICIONAL 
for contard in contadoresCondicionales:
    contard.saveFinalCounts(frames)
#FINCONTEOCONDICIONAL 
cv2.imwrite('ultimofotogramaprocesado.jpg',imgFile3)
print ('Saliendo...')
cam.release()

