#!/usr/bin/python
# -*- coding: utf-8 -*-

# Este NÃO é um programa ROS

# GABARITO. Este codigo pode ser visto em
# https://youtu.be/pEW6QEdeqSU

from __future__ import print_function, division 

import cv2
import os,sys, os.path
import numpy as np

print("Rodando Python versão ", sys.version)
print("OpenCV versão: ", cv2.__version__)
print("Diretório de trabalho: ", os.getcwd())

# Arquivos necessários
video = "cartas.mp4"

def conta_contornos(mask, title):
    """Recebe uma imagem binaria e conta quantos contornos"""
    contornos, arvore = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)     
    desenha_contorno(mask, contornos, title)
    return len(contornos)

def desenha_contorno(mask, contornos, title): 
    mask_rgb = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
    cv2.drawContours(mask_rgb, contornos, -1, [255, 0, 0], 5);
    cv2.imshow(title, mask_rgb)

def processa(img):
    # recortar
    # pontos 
    # x,y (433, 170) ate (841, 565)
    cut = img[170:565, 437:832, :]
    

    reg = cut[:,:,2]


    # segmentar vermelho e preto 

    # limiariza vermelho
    lim, reg_limiar = cv2.threshold(reg, 240, 255, cv2.THRESH_BINARY)
    #cv2.imshow("R limiar", reg_limiar)
    mask_red = reg_limiar
    mask_red = cv2.blur(mask_red, (3,3))


    gray = cv2.cvtColor(cut, cv2.COLOR_BGR2GRAY)
    lim, gray_limiar  = cv2.threshold(gray, 20, 255, cv2.THRESH_BINARY)
    
    # BITWISE not
    # cv2.imshow("GRay limiar", ~gray_limiar)
    mask_black = 255-gray_limiar
    #cv2.imshow("GRay limiar", mask_black)

    # contar quantas figuras tem
    blacks = conta_contornos(mask_black, "BLACK")
    reds = conta_contornos(mask_red, "RED")

    font = cv2.FONT_HERSHEY_SIMPLEX

    if reds > blacks:        
        cv2.putText(img,'{} de Ouros'.format(reds),(20,50), font, 1,(255,255,255),2,cv2.LINE_AA)
    else:
        cv2.putText(img,'{} de Paus'.format(blacks),(20,50), font, 1,(255,255,255),2,cv2.LINE_AA)





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

        # print(frame.shape) para saber o tam da imagem

        processa(frame)
        cv2.imshow('imagem', frame)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    # When everything done, release the capture
    cap.release()
    cv2.destroyAllWindows()


