#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  1 21:10:08 2018

@author: luo3300612
"""

import os
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
from skimage import measure,draw
from PIL import Image
import time
def jump(num):
    print('ready to jump!')
    os.system("adb shell input swipe 590 1747 590 1747 " +str(num))
    print('we jump ' + str(num))
    
def remove_shadow(img):
    shadow = np.array([0.41176471,0.42745098,0.48627451,1])
    for i in range(img.shape[0]): 
        for j in range(img.shape[1]):
            if abs((img[i,j]/255-shadow)[0:3]).sum()<0.06:
                img[i,j] = np.array([0,0,0,1])

def my_back(img1):
    print("removing background...")
    img = img1.copy()
    Q=[]
    st = (1,1)
    Q.append(st)
    next_point = [(1,0),(-1,0),(0,1),(0,-1)]
    b = np.zeros(img.shape)
    b[0,0] = 1
    count = 0
    img[st] = 0
    while len(Q)!=0:
        v = Q[0]
        Q.remove(v)
        count += 1
        for k in range(4):
            p = v[0] + next_point[k][0],v[1] + next_point[k][1]
            if p[0] in range(b.shape[0]) and p[1] in range(b.shape[1]) and b[p]!=1 and abs(img1[p] - img1[v])<0.01:
                img[p] = 0
                b[p] = 1
                Q.append(p)
    print(count)
    print("OK!")
    return img
                
    
def get_pic():
    print("get picture...")
    os.system("adb shell screencap -p /sdcard/3.png")
    os.system("adb pull /sdcard/3.png ~/Desktop/play")
    print("OK!")


def rgb2gray(rgb):
    return np.dot(rgb[...,:3], [0.4, 0.4, 0.4])


def start():
    lena = mpimg.imread('/home/luo3300612/Desktop/play/3.png')
    lena.shape
    one = lena[500:,:,:].copy()
    oper_before = one[:1000,:,:].copy()
    #aver = one[0:100,0:1000,:].copy()
    #back_mean = rgb2gray(aver).mean()
    gray =rgb2gray(oper_before)
    oper = my_back(gray)
    #oper = abs(gray - back_mean)
    print("cal distance...")
    d,img_list = get_dis(oper)
    k = 1.5
    print("ready to jump!")
    if int(d*k) == 0:
        jump(350)
        print("jump " + str(350) + " ms")
        return img_list
    jump(int(d*k))
    print("jump " + str(d*k) + " ms")
    return img_list


def start2():
    lena = Image.open('/home/luo3300612/Desktop/play/3.png')
    row = int(lena.size[0]/3)
    col = int(lena.size[1]/3)
    lena2 = lena.resize((row,col))
    lena = np.array(lena2)
    remove_shadow(lena)
    #plt.imshow(lena)
    one = lena[200:550,:,:].copy()
    #aver = one[0:100,0:1000,:].copy()
    #back_mean = rgb2gray(aver).mean()
    gray =rgb2gray(one)/255
    oper = my_back(gray)
    #oper = abs(gray - back_mean)
    print("cal distance...")
    d,img_list = get_dis(oper)
    k = 1.5*3
    print("ready to jump!")
    if int(d*k) < 200:
        jump(350)
        print("jump " + str(350) + " ms")
        return img_list
    jump(int(d*k))
    print("jump " + str(d*k) + " ms")
    return img_list



def bfs(img_list,img,xy_list):
    result = np.zeros(img.shape)
    b = np.zeros(img.shape)
    row = b.shape[0]
    col = b.shape[1]
    next_point = [(1,0),(-1,0),(0,1),(0,-1)]
    fl = 0
    score =[]
    for i in range(row):
        for j in range(col):
            if img[i,j]>0.04 and b[i,j]!=1:
                xmin = (i,j)
                xmax = (i,j)
                ymin = (i,j)
                ymax = (i,j)
                color = img[i,j]
                Q = []
                c = np.zeros(img.shape)
                c[i,j] = img[i,j]
                b[i,j] = 1
                Q.append((i,j))
                count = 0
                flag = 1
                while len(Q)!=0:
                    v = Q[0]
                    Q.remove(v)
                    count += 1
                    for k in range(4):
                        p = v[0] + next_point[k][0],v[1] + next_point[k][1]
                        #and abs(img[p]-color)<0.2
                        if p[0] in range(row) and p[1] in range(col) and img[p]>0.04 and abs(img[p]-color)<0.1 and b[p]!=1:
                              b[p] = 1
                              c[p] = img[p]
                              Q.append(p)
                              if p[0] < xmin[0]:
                                  xmin = p[0],p[1]
                              if p[0] > xmax[0]:
                                  xmax = p[0],p[1]
                              if p[1] < ymin[1]:
                                  ymin = p[0],p[1]
                              if p[1] > ymax[1]:
                                  ymax = p[0],p[1]
                if count > 7000/9:
                   if abs(xmin[1] - xmax[1]) < 30 and abs(ymin[0]-ymax[0])<30:
                        '''for xy in xy_list:
                            if xmin[0] in range(xy[0][0],xy[1][0]) and \
                            xmax[0] in range(xy[0][0],xy[1][0]) and \
                            ymin[1] in range(xy[2][1],xy[3][1]) and \
                            ymax[1] in range(xy[2][1],xy[3][1]):
                                flag = 0
                            if xy[0][0] in range(xmin[0],xmax[0]) and \
                            xy[1][0] in range(xmin[0],xmax[0]) and \
                            xy[2][1] in range(ymin[1],ymax[1]) and \
                            xy[3][1] in range(ymin[1],ymax[1]):
                                flag = 0'''
                        if flag == 1:
                            img_list.append(c)
                            xy_list.append((xmin,xmax,ymin,ymax))
                            score.append(abs(count-840)+abs(xmax[0]-xmin[0]-46)+abs(ymax[1]-ymin[1]-25))
                            print(count)
                            print(xmax[0]-xmin[0])
                            print(ymax[1]-ymin[1])
                            if fl == 1:
                                return len(img_list)-1,len(img_list)-2
                            if 7000/9<abs(count) < 8000/9 and 1.6< (xmax[0]-xmin[0])/(ymax[1]-ymin[1]) <1.95:
                                if len(img_list)!=1:
                                    return 0,len(img_list)-1
                                else:
                                    fl = 1
                            
    for im in img_list:
        result += im
    print("WARNING: SCORE MODE!")
    min_score = 999999
    min_rec =0
    for i in range(len(score)):
        if score[i] < min_score:
            min_score = score[i]
            min_rec = i
    return 0,min_rec


def find_me(img):
    d1 = img.shape[0]
    d2 = img.shape[1]
    standard = np.array([54,60,102,255])
    b = np.zeros((d1,d2))
    count =0
    for i in range(d1):
        for j in range(d2):
            e = img[d1-i-1,j] - standard
            if (e**2).sum()  < 200:
                count += 1
                p = (d1-i-1,j)
                b[p] = 1
    print(count)
    plt.imshow(b)
    return b


def find_me_use(img):
    print('find me...')
    d1 = img.shape[0]
    d2 = img.shape[1]
    standard = np.array([61,55,82,255])
    x = 0
    y = 0
    flag = 0
    count = 0
    nowi = 0
    ally = 0
    for i in range(d1):
        for j in range(d2):
            e = img[d1-i-1,j] - standard
            if (e**2).sum()  < 200:
                if flag == 0:
                    x = d1-i-1
                    flag = 1
                    y = j
                    ally = y
                    count = 1
                    nowi = i
                if flag == 1 and i-nowi==50:
                    return x,y
                count += 1
                ally += j
                y = ally/count


def start3():
      lena = Image.open('/home/luo3300612/Desktop/play/3.png')
      row = int(lena.size[0])
      col = int(lena.size[1])
      lena2 = lena.resize((row,col))
      lena = np.array(lena2)
      img = lena[750:1300]
      me = find_me_use(img)
      to = find_to(img,me)
      distance = np.sqrt((me[0] - to[0])**2 + (me[1] - to[1])**2)
      second = distance * 1.4
      jump(int(second))
      return img

def get_dis(oper):                
    img_list = []
    xy_list = []
    r,fr_n = bfs(img_list, oper, xy_list)
    #plt.imshow(img_list[0])
    #plt.imshow(img_list[1])
    #to = img_list[r]
    #fr = img_list[fr_n]
    center_tox = (xy_list[r][0][0] + xy_list[r][1][0]) /2
    center_toy = (xy_list[r][2][1] + xy_list[r][3][1]) /2
    center_fromx = (xy_list[fr_n][0][0] + xy_list[fr_n][1][0]) /2
    center_fromy = (xy_list[fr_n][2][1] + xy_list[fr_n][3][1]) /2
    dis = np.sqrt((center_tox-center_fromx)**2 + (center_toy-center_fromy)**2)
    return dis,img_list


def find_to(img1,me):
    print('find to...')
    background_check = 500 # more than
    same_check = 70 # less than
    img = img1/255
    img = img*255
    row = img.shape[0]
    col = img.shape[1]
    background = img[0,0]
    b = np.zeros((row,col))
    next_point = [(1,0),(-1,0),(0,1),(0,-1)]
    first = 1,1
    for i in range(row):
        for j in range(col):
            e = ((img[i,j] - background)**2).sum()
            if e > background_check and b[i,j]!=1:# not background
                  Q = []
                  p = (i,j)
                  c = np.zeros((row,col))
                  Q.append(p)
                  count = 0
                  b[p] = 1
                  c[p] = 1
                  xmin = i
                  xmax = i
                  ymin = j
                  ymax = j
                  first = p
                  while len(Q)!=0:
                      p = Q[0]
                      Q.remove(p)
                      color = img[p]
                      count += 1
                      for k in range(4):
                          ni = p[0] + next_point[k][0]
                          nj = p[1] + next_point[k][1]
                          v = (ni,nj)
                          if ni in range(row) and nj in range(col) and b[v]!=1 and ((img[v]-background)**2).sum()>background_check:
                              ee = ((img[v] - color)**2).sum()
                              if ee < same_check:
                                  Q.append(v)
                                  b[v] = 1
                                  c[v] = 1
                                  if v[0] > xmax:
                                      xmax = v[0]
                                  if v[0] < xmin:
                                      xmin = v[0]
                                  if v[1] > ymax:
                                      ymax = v[1]
                                  if v[1] < ymin:
                                      ymin = v[1]
                  if abs((ymin+ymax)/2-me[1])<50:
                      print('self')
                      continue
                  break
        else:
            continue
        break
    print('count = ' + str(count))
    plt.imshow(c)
    if count < 10:
        print('day or super')
        return first[0] + 100 ,first[1]
    elif 1200< count < 1400:
        print('CDcount')
        return first[0] + 100 ,first[1]
    if xmax-xmin < 50:
        print('CD50')
        return first[0] + 100 ,first[1]
    #plt.imshow(b)
    return (xmax+xmin)/2,(ymax+ymin)/2
                  
                                  
                  
                  


def get_dis2(oper):                
    img_list = []
    xy_list = []
    r = bfs(img_list, oper, xy_list)
    #plt.imshow(img_list[0])
    #plt.imshow(img_list[1])
    to = img_list[r]
    fr_n = len(img_list)-1
    fr = img_list[fr_n]
    center_tox = (xy_list[r][0][0] + xy_list[r][1][0]) /2
    center_fromx = (xy_list[fr_n][0][0] + xy_list[fr_n][1][0]) /2
    dis = 2.2*abs(center_tox-center_fromx)
    return dis,img_list


while True:
    get_pic()
    img = start3()
    time.sleep(2)


'''
img_list = []  
while True:
    get_pic()
    img_list = start2()
    time.sleep(2)'''


'''
while True:
    c = input('next')
    if c == '1':
        get_pic()
        lena = Image.open('/home/luo3300612/Desktop/play/3.png')
        row = int(lena.size[0])
        col = int(lena.size[1])
        lena2 = lena.resize((row,col))
        lena = np.array(lena2)
        img1 = lena[750:]
            
        
        background_check = 500 # more than
        
        
        same_check = 150 # less than
        
        img = img1/255
        img = img*255
        row = img.shape[0]
        col = img.shape[1]
        background = img[0,0]
        Q = []
        b = np.zeros((row,col))
        next_point = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(1,-1),(-1,1),(-1,-1)]
        count = 0
        for i in range(row):
            for j in range(col):
                e = ((img[i,j] - background)**2).sum()
                if e > background_check:# not background
                      p = (i,j)
                      Q.append(p)
                      b[p] = 1
                      print(p)
                      while len(Q)!=0:
                          p = Q[0]
                          Q.remove(p)
                          color = img[p]
                          count += 1
                          for k in range(4):
                              ni = p[0] + next_point[k][0]
                              nj = p[1] + next_point[k][1]
                              v = (ni,nj)
                              if ni in range(row) and nj in range(col) and b[v]!=1 and ((img[v]-background)**2).sum()>background_check:
                                  ee = ((img[v] - color)**2).sum()
                                  if ee < same_check:
                                      Q.append(v)
                                      b[v] = 1
                      break
            else:
                continue
            break
        print(count)
        plt.imshow(b)


'''

'''
plt.imshow(img_list[0])

'''

'''
img_list = []
xy_list = []
bfs(img_list,oper,xy_list)
'''


'''

lena = Image.open('/home/luo3300612/Desktop/play/3.png')
row = int(lena.size[0]/3)
col = int(lena.size[1]/3)
lena2 = lena.resize((row,col))
lena = np.array(lena2)
plt.imshow(lena)

'''
