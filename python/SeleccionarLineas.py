#!/usr/bin/python
from darknet import *
from Counter import linecounter as lc
from Track import tracking as tr
import cv2

 
"""
#YOLO VOC
net = load_net("../cfg/yolo-voc.cfg", "../../darknet/yolo-voc.weights", 0)
meta = load_meta("../cfg/voc_py.data")
"""

#NUESTRO YOLO ENTRENADO 80000 iteraciones
net = load_net("../yolo-obj.cfg", "/home/francisco/Dropbox/2018-1/Proyecto_Movilidad/EntrenamientoMayo/yolo-obj_final.weights", 0)
meta = load_meta("../data/obj.data")


"""
#YOLO COCO
net = load_net("yolo.cfg", "../../darknet/yolo.weights", 0)
meta = load_meta("coco_es.data")
"""
#primera vez
charlador=False
pintarTrayectos=False
if pintarTrayectos:
    framesttl=15
else:
    framesttl=15

deCamara=False


MAXW=550 ## 200 pixeles maximo de ancho permitido
mindist=100
if deCamara:
    cam = cv2.VideoCapture(0)
else: 
    videos=7
    
    if videos==1:
        cam = cv2.VideoCapture("/media/francisco/SiliconPowerArmor/MasVideosBogota/PALOQUEMAO1/CAM10_20171120101800_-1458335004.avi")
        MAXW=700
        mindist=250
        archsal='CAM10_20171120101800_-1458335004.csv'
    if videos==2:
        cam = cv2.VideoCapture("/media/francisco/SiliconPowerArmor/MasVideosBogota/CHICO1/CAM15_20171115090200_-1894263870.avi")
        MAXW=1000
        mindist=250
        archsal='CAM15_20171115090200_-1894263870.csv'
    if videos==3:
        mindist=250
        MAXW=550
        cam = cv2.VideoCapture("/media/francisco/SiliconPowerArmor/MasVideosBogota/CHICO1/CAM08_20171120095800_-1459870085.avi")
        archsal='CAM08_20171120095800_-1459870085.csv'
    if videos==4:
        MAXW=550
        mindist=250
        cam = cv2.VideoCapture("/media/francisco/SiliconPowerArmor/MasVideosBogota/PALOQUEMAO2/CAM08_20171101092300_1190757893.avi")
        archsal='CAM08_20171101092300_1190757893.csv'
    if videos==5:
        MAXW=1000
        mindist=250
        cam = cv2.VideoCapture("/media/francisco/SiliconPowerArmor/CAM24_20180116105800_-199917449.avi")
        archsal='CAM24_20180116105800_-199917449.csv'
    if videos==6:
        MAXW=1000
        mindist=250
        cam = cv2.VideoCapture("/home/francisco/Descargas/CAM07_20180415105200_-2072911051.avi")
        archsal='CAM07_20180415105200_-2072911051.csv'
    if videos==7:
        MAXW=750
        mindist=60
        cam = cv2.VideoCapture("/home/francisco/Descargas/VIDEOS_SDM/CAM02_20180521071448_80507233.avi")
        archsal='CAM02_20180521071448_80507233.csv'



frames=0
ret_val, imgFile2 = cam.read()
frames+=1
if not ret_val:
    print 'no se pudo abrir la camara, saliendo'
    exit()

imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)
#imgFile2 = cv2.imread("../data/eagle.jpg")
tama=imgFile2.shape
imgImported=make_image(tama[1],tama[0],tama[2])

imgFileptr,cv_img=get_iplimage_ptr(imgFile3)    
ipl_in2_image(imgFileptr,imgImported)
rgbgr_image(imgImported)
"""
#save_image(imgImported,"eagle_detect")
r = detect_img(net, meta, imgImported) 
print r
for i in range(len(r)):
    w=int(r[i][2][2])
    h=int(r[i][2][3])
    x=int(r[i][2][0])-w/2
    y=int(r[i][2][1])-h/2
    cv2.rectangle(imgFile2, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
cv2.imshow('Video', imgFile2)        
cv2.waitKey(10)
"""
track=tr.tracking(verbose=charlador,mindist=mindist,framesttl=framesttl)#verbose=False,mindist=100
lineaDeConteo=lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo',filename=archsal,linecount=1)
lineaDeConteo2=lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo',filename=archsal,linecount=2)

contar=lc.counter(lineaDeConteo.pt1,lineaDeConteo.pt2,filename=archsal,linecount=1)    

contar2=lc.counter(lineaDeConteo2.pt1,lineaDeConteo2.pt2,filename=archsal,linecount=2)    


while True:
    ret_val, imgFile2 = cam.read()
    frames+=1
    if not ret_val:
        print ("Fin del video o salida en camara, saliendo")
        cv2.imwrite('ultimofotogramaprocesado.jpg',cv2.cvtColor(imgFile3,cv2.COLOR_RGB2BGR))
        break
    segframes=cam.get(cv2.CAP_PROP_POS_MSEC)
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
        print r
        
        for i in range(len(r)):
            w=int(r[i][2][2])
            h=int(r[i][2][3])
            x=int(r[i][2][0])-w/2
            y=int(r[i][2][1])-h/2
            #cv2.rectangle(imgFile2, (x,y), (x+w,y+h), (255,255,0), thickness=1, lineType=8, shift=0)
    
    for i in range(len(r)):
        if r[i][2][2]<MAXW:
            track.insertNewObject(r[i][2][0],r[i][2][1],r[i][2][2],r[i][2][3],strFeature=r[i][0])
        else:
            print ("        eliminado objeto por tamanio= ",r[i][2][2])
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

    
    
    cv2.circle(imgFile2,lineaDeConteo.pt1,3,(0,0,255),-1)
    cv2.line(imgFile2,lineaDeConteo.pt1,lineaDeConteo.pt2,(0,0,255),1)
    cv2.circle(imgFile2,lineaDeConteo.pt2,3,(255,0,255),-1)
    # contar los que trayectos que pasen las lineas de conteo
    
    for idx in range(len( track.p.p)):
        if len(track.p.p[idx].path)>2: # si la longitud del parh es mayor a dos
            # toma los dos registros mas recientes y los prueba si pasaron la linea de conteo
            p1=(int(track.p.p[idx].path[-1].x),int(track.p.p[idx].path[-1].y))
            p2=(int(track.p.p[idx].path[-2].x),int(track.p.p[idx].path[-2].y))
            cv2.line(imgFile2,p1,p2,track.p.p[idx].colour,1)
            if (contar.testLine(p2,p1) and not track.p.p[idx].contadores[contar.linecount]):
                #contar.conteo+=1
                cv2.circle(imgFile2,contar.intersectPoint(p2,p1),4,(0,0,255), -1) #intersecting point
                track.p.p[idx].contado=True
                track.p.p[idx].contadores[contar.linecount]=1
                #clase
                contar.addToLineCounter(str(track.p.p[idx].str),frames)
    
            if (contar2.testLine(p2,p1) and not track.p.p[idx].contadores[contar2.linecount]):
                #contar2.conteo+=1
                cv2.circle(imgFile2,contar2.intersectPoint(p2,p1),4,(0,0,255), -1) #intersecting point
                track.p.p[idx].contado=True
                track.p.p[idx].contadores[contar2.linecount]=1
                #clase
                contar2.addToLineCounter(str(track.p.p[idx].str),frames)
                
    if pintarTrayectos:
        track.drawPaths(imgFile2)
    
    
    cv2.imshow('Video', imgFile2)
    k = cv2.waitKey(2)& 0xFF
    if k==ord('q'):    # Esc key=537919515 en linux WTF??? para parar y en mi otro PC 1048689
        print 'interrupcion de usuario...'
        break
contar.saveFinalCounts(frames)
contar2.saveFinalCounts(frames)
print 'Saliendo...'
cv2.destroyAllWindows()
cam.release()
exit()
"""

    source=imgFile.copy()
bitmap = cv2.cv.CreateImageHeader((source.shape[1], source.shape[0]), cv2.cv.IPL_DEPTH_8U, 3)
if len(source.shape)==3:
    cv2.cv.SetData(bitmap, source.tostring(),source.dtype.itemsize * 3 * source.shape[1])    
else:
    print("Posible error no se si soporta imagenes en blanco y negro")
    cv2.cv.SetData(bitmap, source.tostring(),source.dtype.itemsize * 1 * source.shape[1])  
#bitmap2=get_iplimage_ptr(source)
"""
