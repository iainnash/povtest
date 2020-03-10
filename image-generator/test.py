# -*- coding: utf-8 -*-
import cv2
import os
import math
from PIL import Image
#Array setting
NUMPIXELS = 82 #Number of LEDs
Div = 160 #Number of divisions per lap
Bright = 100 #LED Brightness 
Led0Bright = 100 #Brightness of center LED [%]
#File creation
file = open('graphics.h', 'w')
file.write('#define NUMPIXELS ' + str(NUMPIXELS) + '\n')
file.write('#define Div ' + str(Div) + '\n' + '\n')
#file.write('#define Frame ' + str(Frame) + '\n' + '\n')
file.write('const uint32_t pic [Frame][Div][NUMPIXELS] = {' + '\n')
# Read GIF file
gif_file_name = "pic.gif"
gif = cv2.VideoCapture(gif_file_name)
#Image conversion function
def polarConv(pic, i):
   imgOrgin = cv2.imread(pic) #Read image data
   h, w, _ = imgOrgin.shape #Get image size
   print('h', h, 'w', w)
   #Image reduction
   
   rw = int(math.floor((NUMPIXELS * 2 -1)/float(h) *w))
   rh = int(math.floor(NUMPIXELS * 2 -1))
   print('rw', rw, 'rh', rh)
   imgRedu = cv2.resize(imgOrgin, (rw, rh)) 
   #cv2.imwrite(str(i) + '-resize.jpg',imgRedu)
   #Reduced image center coordinates
   h2, w2, _ = imgRedu.shape
   wC = int(math.floor(w2 / 2))
   hC = int(math.floor(h2 / 2))
   #Polar coordinate conversion image preparation
   imgPolar = Image.new('RGB', (NUMPIXELS, Div))
   #Polar transformation
   file.write('\t{\n')
   for j in range(0, Div):
       file.write('\t\t{')
       for i in range(0, int(hC+1)):
           #Get coordinate color
           rP = int(imgRedu[int(hC + math.ceil(i * math.cos(2*math.pi/Div*j))),
                        int(wC - math.ceil(i * math.sin(2*math.pi/Div*j))), 2]
                    * ((100 - Led0Bright) / NUMPIXELS * i + Led0Bright) / 100 * Bright /100)
           gP = int(imgRedu[int(hC + math.ceil(i * math.cos(2*math.pi/Div*j))),
                        int(wC - math.ceil(i * math.sin(2*math.pi/Div*j))), 1]
                    * ((100 - Led0Bright) / NUMPIXELS * i + Led0Bright) / 100 * Bright /100)
           bP = int(imgRedu[int(hC + math.ceil(i * math.cos(2*math.pi/Div*j))),
                        int(wC - math.ceil(i * math.sin(2*math.pi/Div*j))), 0]
                    * ((100 - Led0Bright) / NUMPIXELS * i + Led0Bright) / 100 * Bright /100)
           file.write('0x%02X%02X%02X' % (rP,gP,bP))
           if i == hC:
               file.write('},\n')
           else:
               file.write(', ')
           imgPolar.putpixel((i,j), (rP, gP, bP))
   file.write('\t},\n\n')
#Generate directory to save screen capture
dir_name = "screen_caps"
if not os.path.exists(dir_name):
   os.mkdir(dir_name)
i = 0
while True:
   is_success, frame = gif.read()
   # Exit when the file can not be read
   if not is_success:
       break
   # Write out to an image file
   img_name = str(i) + ".jpg"
   img_path = os.path.join(dir_name, img_name)
   cv2.imwrite(img_path, frame)
   #conversion
   polarConv(img_path, i)
   i += 1
file.write('};' + '\n' + '\n')
file.close()
#Inserting the number of frames at the beginning of the file
with open('graphics.h') as f:
   l = f.readlines()
l.insert(0, '#define Frame ' + str(i) + '\n')
with open('graphics.h', mode='w') as f:
   f.writelines(l)
