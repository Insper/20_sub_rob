#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

import triutil

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
video = "triangulos.mp4"

def crosshair(img, point, size, color):
    """ Desenha um crosshair centrado no point.
        point deve ser uma tupla (x,y)
        color é uma tupla R,G,B uint8
    """
    x,y = point
    cv2.line(img,(x - size,y),(x + size,y),color,5)
    cv2.line(img,(x,y - size),(x, y + size),color,5)


def acha_triangulo(bgr):
    print(bgr.shape)
    red = bgr[:,:,2]
    ret,limiarizada = cv2.threshold(red,thresh=240,maxval=255,type=cv2.THRESH_BINARY)

    cv2.imshow("canal vermelho", limiarizada)

    imagem_gray = limiarizada

    maior_i = -1
    menor_i = imagem_gray.shape[0] + 1
    menor_j = imagem_gray.shape[1] + 1
    maior_j = -1

    for i in range(imagem_gray.shape[0]):
        for j in range(imagem_gray.shape[1]):
            if imagem_gray[i][j] == 255:
                if i < menor_i:
                    menor_i = i
                if i  > maior_i:
                    maior_i = i
                if j  > maior_j:
                    maior_j = j 
                if j < menor_j:
                    menor_j = j
    
    media_j  = int((maior_j + menor_j)/2)

    c = ( media_j, menor_i) # ponto de cima
    a = (menor_j, maior_i)
    b = (maior_j, maior_i)

    print(a,b,c)

    #crosshair(bgr, a, 10, (0,255,0))
    #crosshair(bgr, a, 10, (0,255,0))

    # triutil.plot_tri(bgr, a,b,c, color=(0,255,0))

    return a,b,c


def center_of_mass(mask):
    """ Retorna uma tupla (cx, cy) que desenha o centro do contorno"""
    M = cv2.moments(mask)
    # Usando a expressão do centróide definida em: https://en.wikipedia.org/wiki/Image_moment
    cX = int(M["m10"] / M["m00"])
    cY = int(M["m01"] / M["m00"])
    return (int(cX), int(cY))

def acha_estrela(bgr):
    blue = bgr[:,:,0]
    ret, limiarizada = cv2.threshold(blue,thresh=240,maxval=255,type=cv2.THRESH_BINARY)

    p = center_of_mass(limiarizada)
    crosshair(bgr, p, 15, (0,0,255))
    #cv2.imshow("centro estrela", bgr)    
    return p



if __name__ == "__main__":

    # Inicializa a aquisição da webcam
    cap = cv2.VideoCapture(video)


    print("Se a janela com a imagem não aparecer em primeiro plano dê Alt-Tab")

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if ret == False:
            #print("Codigo de retorno FALSO - problema para capturar o frame")
            cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            continue
            #sys.exit(0)

        # Our operations on the frame come here
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB) 
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        tri = acha_triangulo(frame)
        p = acha_estrela(frame)


        font = cv2.FONT_HERSHEY_SIMPLEX

        if triutil.point_in_triangle(tri[0], tri[1], tri[2], p):
            cv2.putText(frame,'ESTRELA DENTRO',(5,50), font, 1,(255,255,255),2,cv2.LINE_AA)        
        else:
            cv2.putText(frame,'ESTRELA FORA',(5,50), font, 1,(255,255,255),2,cv2.LINE_AA)        

        
        




        # NOTE que em testes a OpenCV 4.0 requereu frames em BGR para o cv2.imshow
        cv2.imshow('imagem', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


