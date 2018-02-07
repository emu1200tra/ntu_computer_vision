from PIL import Image

binary_resample_list = [[0 for i in range(68)] for j in range(68)]
result = [[' ' for i in range(64)] for j in range(64)]

def h_func(b , c , d , e):
  #print b , c , d , e
  b_pix = binary_resample_list[b[0]+2][b[1]+2]
  c_pix = binary_resample_list[c[0]+2][c[1]+2]
  d_pix = binary_resample_list[d[0]+2][d[1]+2]
  e_pix = binary_resample_list[e[0]+2][e[1]+2]
  if b_pix == c_pix and (d_pix != b_pix or e_pix != b_pix):
    return 'q'
  elif b_pix == c_pix and (d_pix == b_pix and e_pix == b_pix):
    return 'r'
  else:
    return 's'

image = Image.open('lena.bmp')
binary = image.copy()
binary_resample = Image.new('L' , (64 , 64) , color = 0)


(h , w) = image.size

for i in range(0 , h):
  for j in range(0 , w):
    if image.getpixel((i , j)) > 128:
      binary.putpixel((i , j) , 255)
    else:
      binary.putpixel((i , j) , 0)

(h_resample , w_resample) = binary_resample.size

test = open('test.txt' , 'w')

for j in range(h_resample):
  for i in range(w_resample):
    binary_resample.putpixel((i , j) , binary.getpixel((i*8 , j*8)))
    binary_resample_list[i+2][j+2] = binary.getpixel((i*8 , j*8))
    if binary_resample_list[i+2][j+2] == 255:
      test.write('#')
    else:
      test.write(' ')
  test.write('\n')
test.close


for i in range(h_resample):
  for j in range(w_resample):
    if binary_resample_list[i+2][j+2] == 255:
      a = [[i , j] , [i , j+1] , [i-1 , j+1] , [i-1 , j]]
      check = ['a']*4
      check[0] = h_func(a[0] , a[1] , a[2] , a[3])
      a = [[i , j] , [i-1 , j] , [i-1 , j-1] , [i , j-1]]
      check[1] = h_func(a[0] , a[1] , a[2] , a[3])
      a = [[i , j] , [i , j-1] , [i+1 , j-1] , [i+1 , j]]
      check[2] = h_func(a[0] , a[1] , a[2] , a[3])
      a = [[i , j] , [i+1 , j] , [i+1 , j+1] , [i , j+1]]
      check[3] = h_func(a[0] , a[1] , a[2] , a[3])
      counter_r = 0
      counter_q = 0
      for k in range(4):
        if check[k] == 'r':
          counter_r += 1
        elif check[k] == 'q':
          counter_q += 1
      if counter_r == 4:
        result[i][j] = '5'
      else:
        result[i][j] = str(counter_q)


result_file = open('result.txt' , 'w')
for j in range(w_resample):
  for i in range(h_resample):
    result_file.write(result[i][j])
  result_file.write('\n')    
result_file.close