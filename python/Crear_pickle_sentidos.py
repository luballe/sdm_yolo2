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



"""
Llamado del script:
./2_crear_pickle.sh /monitoreo/videos_caracas_cll6/2021-08-05/0600-0700/results/ NS,SN,WE,EW

"""
#folder=easygui.diropenbox(title="Seleccione la carpeta con los videos a aforar",default="/media/francisco/monitoreo")
print(sys.argv)
folder=sys.argv[1]
#num_lineas_conteo=sys.argv[2]
sentidos_str=sys.argv[2]

#print(sentidos_str)
sentidos_arr=sentidos_str.split(',')
#print(sentidos_arr)
num_lineas_conteo=len(sentidos_arr)
#print(num_lineas)

#ROI Selection in Frame consist in an archive called ROI.txt with a tuple in the first and only line in file, that is the ROI. 
#In notation (X,Y,width,heigth), X and y are the upper left coordinate of the Region Of Interest ROI
WITHROI=os.path.isfile(folder+"/ROI.txt")
roi=None
if WITHROI:
    with open(folder+"/ROI.txt", "r") as f:
        data = f.readline()
    roi=eval(data)
    print ("Cargando ROI ",roi)
    


filelist=glob.glob(folder+"/*.avi")
if len(filelist) == 0:
    print("ERROR LA CARPETA NO CONTIENE ARCHIVOS .AVI buscando .mp4")
    filelist=glob.glob(folder+"/*.mp4")
    
filelist.sort()
if len(filelist) == 0:
    print("ERROR LA CARPETA NO CONTIENE ARCHIVOS DE VIDEO SALIENDO")
else:  
    if os.path.isfile(folder+"/"+"config.pkl"):
        with open(folder+"/"+"config.pkl") as f:  # Python 3: open(..., 'rb')
            lineasDeConteo, lineasDeConteoCondicional, lineaDeConteo,lineaDeConteoCondicional,sentidos_arr = pickle.load(f)
        
    else:
        title  ="Cuantas lineas de conteo?"
        msg = "Seleccione el numero de lineas de conteo que quiere poner, se recomiendan maximo 6 lineas de conteo"
        choices = ["0","1", "2", "3", "4", "5","6","7","8","9"]
        #choice = easygui.choicebox(msg, title, choices)
        #choice = "2"
        choice = num_lineas_conteo
        lineasDeConteo=int(choice)
        print "usted ha seleccionado ",lineasDeConteo," lineas de conteo"
    
        #CONTEOCONDICIONAL
        title  ="Cuantas lineas de conteo condicional?"
        msg = "Seleccione el numero de lineas de conteo condicional que quiere poner, se recomiendan maximo 6 pares de lineas de conteo"
        choices = ["0","1", "2", "3", "4", "5", "6","7","8","9"]
        #choice2 = easygui.choicebox(msg=msg, title=title, choices=choices)
        choice2 = "0"
        lineasDeConteoCondicional=int(choice2)
        print "usted ha seleccionado ",lineasDeConteoCondicional," lineas de conteo condiconal"
        #FINCONTEOCONDICIONAL
        
        
        print "Se va a tomar el primercuadro del primer video encontrado para seleccionar las lineas de conteo"
        fn=filelist[0]
        cam = cv2.VideoCapture(fn)
        #ret_val, imgFile2 = cam.read()
        ret_val, imgFile2 = getimage(cam,withroi=WITHROI,roi=roi)
        if not ret_val:
            print ('ERROR:  no se pudo abrir la camara, saliendo')
            exit()
        
        imgFile3 = cv2.cvtColor(imgFile2, cv2.COLOR_BGR2RGB)
        #imgFile2 = cv2.imread("../data/eagle.jpg")
        tama=imgFile2.shape
        imgImported=make_image(tama[1],tama[0],tama[2])
        
        imgFileptr,cv_img=get_iplimage_ptr(imgFile3)    
        ipl_in2_image(imgFileptr,imgImported)
        rgbgr_image(imgImported)
        
        lineaDeConteo=[]
        for cc in range(lineasDeConteo):
            sleep(1)
            lineaDeConteo.append(lc.selectLine(imgFile2,ownString='Selecciona la linea de conteo #' +str(cc+1)+' sentido: '+sentidos_arr[cc],filename=fn,linecount=cc+1,sentido=sentidos_arr[cc]))
            sleep(1)
            
            
        #CONTEOCONDICIONAL
        lineaDeConteoCondicional=[]  
        for cc in range(lineasDeConteoCondicional): 
            sleep(1)
            lineaDeConteoCondicional.append(lc.selecttwoLines(imgFile2,ownString='Selecciona la lineas de conteo condicional' +str(cc+1),filename=fn,linecount=cc+1))
        #FINCONTEOCONDICIONAL
            
        with open(folder+"/"+"config.pkl","w") as f:  # Python 3: open(..., 'rb')
            pickle.dump([lineasDeConteo, lineasDeConteoCondicional, lineaDeConteo,lineaDeConteoCondicional,sentidos_arr],f)
    

