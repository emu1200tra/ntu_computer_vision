from PIL import Image

image = Image.open('binary.bmp')
(h , w) = image.size
dilation = image.copy()
erosion = image.copy()
hit_and_miss = image.copy()
inverse = image.copy()
closing = image.copy()

#dilation
map_record = [[0 for i in range(h+4)] for j in range(w+4)]

for i in range(h):
  for j in range(w):
    if image.getpixel((i , j)) == 255:
      map_record[i+1][j] += 1 ; map_record[i+3][j] += 1 ; map_record[i+2][j] += 1
      map_record[i][j+1] += 1 ; map_record[i+1][j+1] += 1 ; map_record[i+2][j+1] += 1 ; map_record[i+3][j+1] += 1 ; map_record[i+4][j+1] += 1 ;
      map_record[i][j+2] += 1 ; map_record[i+1][j+2] += 1 ; map_record[i+2][j+2] += 1 ; map_record[i+3][j+2] += 1 ; map_record[i+4][j+2] += 1 ;
      map_record[i][j+3] += 1 ; map_record[i+1][j+3] += 1 ; map_record[i+2][j+3] += 1 ; map_record[i+3][j+3] += 1 ; map_record[i+4][j+3] += 1 ;
      map_record[i+1][j+4] += 1 ; map_record[i+3][j+4] += 1 ; map_record[i+2][j+4] += 1

      

for i in range(h):
  for j in range(w):
    if map_record[i+2][j+2] != 0:
      dilation.putpixel((i , j) , 255)
    else:
      dilation.putpixel((i , j) , 0)

dilation.show()
dilation.save('dilation.bmp')

#erosion
map_record = [[0 for i in range(h+4)] for j in range(w+4)]

for i in range(2 , h-2):
  for j in range(2 , w-2):
    if (image.getpixel((i-1 , j-2)) == 255 and image.getpixel((i , j-2)) == 255 and image.getpixel((i+1 , j-2)) == 255 and 
        image.getpixel((i-2 , j-1)) == 255 and image.getpixel((i-1 , j-1)) == 255 and image.getpixel((i , j-1)) == 255 and 
        image.getpixel((i+1 , j-1)) == 255 and image.getpixel((i+2 , j-1)) == 255 and image.getpixel((i-2 , j)) == 255 and
        image.getpixel((i-1 , j)) == 255 and image.getpixel((i , j)) == 255 and image.getpixel((i+1 , j)) == 255 and 
        image.getpixel((i+2 , j)) == 255 and image.getpixel((i-2 , j+1)) == 255 and image.getpixel((i-1 , j+1)) == 255 and
        image.getpixel((i , j+1)) == 255 and image.getpixel((i+1 , j+1)) == 255 and image.getpixel((i+2 , j+1)) == 255 and 
        image.getpixel((i-1 , j+2)) == 255 and image.getpixel((i , j+2)) == 255 and image.getpixel((i+1 , j+2)) == 255):
      map_record[i+2][j+2] += 1
        

for i in range(h):
  for j in range(w):
    if map_record[i+2][j+2] != 0:
      erosion.putpixel((i , j) , 255)
    else:
      erosion.putpixel((i , j) , 0)

erosion.show()
erosion.save('erosion.bmp')

#hit and miss
for i in range(h):
  for j in range(w):
    if image.getpixel((i , j)) == 255:
      inverse.putpixel((i , j) , 0)
    else:
      inverse.putpixel((i , j) , 255)

map_record = [[0 for i in range(h+2)] for j in range(w+2)]

for i in range(1 , h):
  for j in range(0 , w-1):
    if image.getpixel((i , j)) == 255 and image.getpixel((i-1 , j)) == 255 and image.getpixel((i , j+1)) == 255:
      map_record[i+1][j+1] += 1
        
for i in range(h):
  for j in range(w):
    if map_record[i+1][j+1] != 0:
      erosion.putpixel((i , j) , 255)
    else:
      erosion.putpixel((i , j) , 0)


map_record = [[0 for i in range(h+2)] for j in range(w+2)]

for i in range(0 , h-1):
  for j in range(1 , w):
    if inverse.getpixel((i+1 , j)) == 255 and inverse.getpixel((i , j-1)) == 255 and inverse.getpixel((i+1 , j-1)) == 255:
      map_record[i+1][j+1] += 1
        
for i in range(h):
  for j in range(w):
    if map_record[i+1][j+1] != 0:
      inverse.putpixel((i , j) , 255)
    else:
      inverse.putpixel((i , j) , 0)

for i in range(h):
  for j in range(w):
    if inverse.getpixel((i , j)) == erosion.getpixel((i , j)):
      hit_and_miss.putpixel((i , j) , erosion.getpixel((i , j)))
    else:
      hit_and_miss.putpixel((i , j) , 0)
hit_and_miss.save('hit_and_miss.bmp')
hit_and_miss.show()

#opening

opening = image.copy()
map_record = [[0 for i in range(h+4)] for j in range(w+4)]

for i in range(2 , h-2):
  for j in range(2 , w-2):
    if (image.getpixel((i-1 , j-2)) == 255 and image.getpixel((i , j-2)) == 255 and image.getpixel((i+1 , j-2)) == 255 and 
        image.getpixel((i-2 , j-1)) == 255 and image.getpixel((i-1 , j-1)) == 255 and image.getpixel((i , j-1)) == 255 and 
        image.getpixel((i+1 , j-1)) == 255 and image.getpixel((i+2 , j-1)) == 255 and image.getpixel((i-2 , j)) == 255 and
        image.getpixel((i-1 , j)) == 255 and image.getpixel((i , j)) == 255 and image.getpixel((i+1 , j)) == 255 and 
        image.getpixel((i+2 , j)) == 255 and image.getpixel((i-2 , j+1)) == 255 and image.getpixel((i-1 , j+1)) == 255 and
        image.getpixel((i , j+1)) == 255 and image.getpixel((i+1 , j+1)) == 255 and image.getpixel((i+2 , j+1)) == 255 and 
        image.getpixel((i-1 , j+2)) == 255 and image.getpixel((i , j+2)) == 255 and image.getpixel((i+1 , j+2)) == 255):
      map_record[i+2][j+2] += 1
        

for i in range(h):
  for j in range(w):
    if map_record[i+2][j+2] != 0:
      erosion.putpixel((i , j) , 255)
    else:
      erosion.putpixel((i , j) , 0)

map_record = [[0 for i in range(h+4)] for j in range(w+4)]

for i in range(h):
  for j in range(w):
    if erosion.getpixel((i , j)) == 255:
      map_record[i+1][j] += 1 ; map_record[i+3][j] += 1 ; map_record[i+2][j] += 1
      map_record[i][j+1] += 1 ; map_record[i+1][j+1] += 1 ; map_record[i+2][j+1] += 1 ; map_record[i+3][j+1] += 1 ; map_record[i+4][j+1] += 1 ;
      map_record[i][j+2] += 1 ; map_record[i+1][j+2] += 1 ; map_record[i+2][j+2] += 1 ; map_record[i+3][j+2] += 1 ; map_record[i+4][j+2] += 1 ;
      map_record[i][j+3] += 1 ; map_record[i+1][j+3] += 1 ; map_record[i+2][j+3] += 1 ; map_record[i+3][j+3] += 1 ; map_record[i+4][j+3] += 1 ;
      map_record[i+1][j+4] += 1 ; map_record[i+3][j+4] += 1 ; map_record[i+2][j+4] += 1

      

for i in range(h):
  for j in range(w):
    if map_record[i+2][j+2] != 0:
      opening.putpixel((i , j) , 255)
    else:
      opening.putpixel((i , j) , 0)

opening.show()
opening.save('opening.bmp')

#closing
map_record = [[0 for i in range(h+4)] for j in range(w+4)]

for i in range(h):
  for j in range(w):
    if image.getpixel((i , j)) == 255:
      map_record[i+1][j] += 1 ; map_record[i+3][j] += 1 ; map_record[i+2][j] += 1
      map_record[i][j+1] += 1 ; map_record[i+1][j+1] += 1 ; map_record[i+2][j+1] += 1 ; map_record[i+3][j+1] += 1 ; map_record[i+4][j+1] += 1 ;
      map_record[i][j+2] += 1 ; map_record[i+1][j+2] += 1 ; map_record[i+2][j+2] += 1 ; map_record[i+3][j+2] += 1 ; map_record[i+4][j+2] += 1 ;
      map_record[i][j+3] += 1 ; map_record[i+1][j+3] += 1 ; map_record[i+2][j+3] += 1 ; map_record[i+3][j+3] += 1 ; map_record[i+4][j+3] += 1 ;
      map_record[i+1][j+4] += 1 ; map_record[i+3][j+4] += 1 ; map_record[i+2][j+4] += 1

for i in range(h):
  for j in range(w):
    if map_record[i+2][j+2] != 0:
      dilation.putpixel((i , j) , 255)
    else:
      dilation.putpixel((i , j) , 0)

map_record = [[0 for i in range(h+4)] for j in range(w+4)]

for i in range(2 , h-2):
  for j in range(2 , w-2):
    if (dilation.getpixel((i-1 , j-2)) == 255 and dilation.getpixel((i , j-2)) == 255 and dilation.getpixel((i+1 , j-2)) == 255 and 
        dilation.getpixel((i-2 , j-1)) == 255 and dilation.getpixel((i-1 , j-1)) == 255 and dilation.getpixel((i , j-1)) == 255 and 
        dilation.getpixel((i+1 , j-1)) == 255 and dilation.getpixel((i+2 , j-1)) == 255 and dilation.getpixel((i-2 , j)) == 255 and
        dilation.getpixel((i-1 , j)) == 255 and dilation.getpixel((i , j)) == 255 and dilation.getpixel((i+1 , j)) == 255 and 
        dilation.getpixel((i+2 , j)) == 255 and dilation.getpixel((i-2 , j+1)) == 255 and dilation.getpixel((i-1 , j+1)) == 255 and
        dilation.getpixel((i , j+1)) == 255 and dilation.getpixel((i+1 , j+1)) == 255 and dilation.getpixel((i+2 , j+1)) == 255 and 
        dilation.getpixel((i-1 , j+2)) == 255 and dilation.getpixel((i , j+2)) == 255 and dilation.getpixel((i+1 , j+2)) == 255):
      map_record[i+2][j+2] += 1
        

for i in range(h):
  for j in range(w):
    if map_record[i+2][j+2] != 0:
      closing.putpixel((i , j) , 255)
    else:
      closing.putpixel((i , j) , 0)

closing.show()
closing.save('closing.bmp')