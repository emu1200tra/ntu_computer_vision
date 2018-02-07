from PIL import Image

image = Image.open('lena.bmp')
right_left = image.copy()

(h , w) = image.size

for i in range(0 , h):
  for j in range(0 , w):
    tmp = image.getpixel((i , j))
    right_left.putpixel((h-i-1 , j) , tmp)

right_left.show()
#right_left.save('C:\Users\user\Documents\computer_vision\Right_left.bmp')

up_down = image.copy()

for j in range(0 , w):
  for i in range(0 , h):
    tmp = image.getpixel((i , j))
    up_down.putpixel((i , w-j-1) , tmp)

up_down.show()
#up_down.save('C:\Users\user\Documents\computer_vision\up_down.bmp')

diagonal = image.copy()

for i in range(0 , h):
  for j in range(0 , w):
    tmp = image.getpixel((i , j))
    diagonal.putpixel((j , i) , tmp)

diagonal.show()
#diagonal.save('C:\Users\user\Documents\computer_vision\diagonal.bmp')