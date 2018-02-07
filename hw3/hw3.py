from PIL import Image 
from matplotlib import pyplot as plt

histo = [0]*256
histo2 = [0]*256
histo3 = [0]*256

cdf = [0 for i in range(256)]


image = Image.open('lena.bmp')
dark_image = image.copy()
result = dark_image.copy()

(h , w) = image.size

for i in range(h):
  for j in range(w):
    dark_image.putpixel((i , j) , (image.getpixel((i , j)) / 3) * 2)
    histo[image.getpixel((i , j))] += 1
    histo2[dark_image.getpixel((i , j))] += 1


tmp = 0
min_num = 0
for i in range(256):
  tmp += histo2[i]
  cdf[i] = tmp
for i in range(256):
  if cdf[i] != 0:
    min_num = i
    break

#print min_num

for i in range(w):
  for j in range(h):
    hv = round( (float(cdf[dark_image.getpixel((i , j))] - cdf[min_num]) / float((h*w)-cdf[min_num])) * (255.0) )
    result.putpixel((i , j) , int(hv))
    histo3[result.getpixel((i , j))] += 1

dark_image.show()
dark_image.save('C:\Users\user\Documents\computer_vision\dark_image.bmp')

result.show()
result.save('C:\Users\user\Documents\computer_vision\hito_equal.bmp')


plt.bar(range(0 , 256) , histo)
plt.show()
plt.bar(range(0 , 256) , histo2)
plt.show()
plt.bar(range(0 , 256) , histo3)
plt.show()
