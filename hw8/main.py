from PIL import Image
import math
import random

file = open('SNR.txt' , 'w')

def init():
  image = Image.open('lena.bmp')
  return image

def SNR(original_image , noise_image):
  sigma = 0.0
  (h , w) = original_image.size
  for i in range(h):
    for j in range(w):
      sigma += original_image.getpixel((i , j))
  mius = float(sigma / (h*w))
  print 'mius:' , mius

  sigma = 0.0
  for i in range(h):
    for j in range(w):
      sigma += ((original_image.getpixel((i , j)) - mius)**2)
  vs = float(sigma / (h*w))
  print 'vs:' , vs

  sigma = 0.0
  for i in range(h):
    for j in range(w):
      sigma += (noise_image.getpixel((i , j)) - original_image.getpixel((i , j)))
  miun = float(sigma / (h*w))
  print 'miun:' , miun

  sigma = 0.0
  for i in range(h):
    for j in range(w):
      sigma += ((noise_image.getpixel((i , j)) - original_image.getpixel((i , j)) - miun)**2)
  vn = float(sigma / (w*h))
  snr = 20 * math.log((math.sqrt(vs) / math.sqrt(vn)) , 10)
  print 'SNR:' , snr
  return snr

def gaussian(original_image , amp):
  print 'gaussian amp:' , amp
  (h , w) = original_image.size
  gaussian_image = original_image.copy()
  for i in range(h):
    for j in range(w):
      value = original_image.getpixel((i , j)) + amp * random.gauss(0 , 1)
      if value >= 255:
        value = 255
      gaussian_image.putpixel((i , j) , int(value))

  return gaussian_image

def saltandpepper(original_image , thres):
  print 'salt and pepper threshold:' , thres
  (h , w) = original_image.size
  salt_image = original_image.copy()
  for i in range(h):
    for j in range(w):
      value = random.uniform(0 , 1)
      if value < thres:
        salt_image.putpixel((i , j) , 0)
      elif value > (1 - thres):
        salt_image.putpixel((i , j) , 255)

  return salt_image

def box_filter(noise_image , b_w , b_h):
  (h , w) = noise_image.size
  box_filt_image = noise_image.copy()
  for i in range(h):
    for j in range(w):
      counter = 0
      sum_pixel = 0
      for k in range(-(b_h/2) , (b_h/2)+1):
        for l in range(-(b_w/2) ,( b_w/2)+1):
          if (i + k) >= 0 and (i + k) < h and (j + l) >= 0 and (j + l) < w:
            counter += 1
            sum_pixel += box_filt_image.getpixel((i+k , j+l))
      box_filt_image.putpixel((i , j) , sum_pixel / counter)

  return box_filt_image

def median_filter(noise_image , b_w , b_h):
  (h , w) = noise_image.size
  median_filt_image = noise_image.copy()
  for i in range(h):
    for j in range(w):
      list_arr = []
      for k in range(-(b_h/2) , (b_h/2)+1):
        for l in range(-(b_w/2) , (b_w/2)+1):
          if (i + k) >= 0 and (i + k) < h and (j + l) >= 0 and (j + l) < w:
            list_arr.append(median_filt_image.getpixel((i+k , j+l)))
      list_arr.sort()
      value = 0
      place = len(list_arr)/2
      if len(list_arr) % 2 == 0:
        value = (list_arr[place-1] + list_arr[place]) / 2
      else:
        value = list_arr[place]
      median_filt_image.putpixel((i , j) , value)

  return median_filt_image

def dilation(image):
  (h , w) = image.size
  map_record = [[-1 for i in range(h+4)] for j in range(w+4)]
  for i in range(h):
    for j in range(w):
      map_record[i+2][j+2] = image.getpixel((i , j))
  dilation = image.copy()
  for i in range(h):
    for j in range(w):
      tmp = max(map_record[i+1][j] , map_record[i+3][j] , map_record[i+2][j] , map_record[i][j+1] , map_record[i+1][j+1] , map_record[i+2][j+1] ,
                map_record[i+3][j+1] , map_record[i+4][j+1] , map_record[i][j+2] , map_record[i+1][j+2] , map_record[i+2][j+2] , map_record[i+3][j+2] ,
                map_record[i+4][j+2] , map_record[i][j+3] , map_record[i+1][j+3] , map_record[i+2][j+3] , map_record[i+3][j+3] , map_record[i+4][j+3] ,
                map_record[i+1][j+4] , map_record[i+3][j+4] , map_record[i+2][j+4])
      dilation.putpixel((i , j) , tmp)
  return dilation

def erosion(image):
  (h , w) = image.size
  map_record = [[-1 for i in range(h+4)] for j in range(w+4)]
  for i in range(h):
    for j in range(w):
      map_record[i+2][j+2] = image.getpixel((i , j))
  erosion = image.copy()
  for i in range(h):
    for j in range(w):
      tmp = min(map_record[i+1][j] , map_record[i+3][j] , map_record[i+2][j] , map_record[i][j+1] , map_record[i+1][j+1] , map_record[i+2][j+1] ,
                map_record[i+3][j+1] , map_record[i+4][j+1] , map_record[i][j+2] , map_record[i+1][j+2] , map_record[i+2][j+2] , map_record[i+3][j+2] ,
                map_record[i+4][j+2] , map_record[i][j+3] , map_record[i+1][j+3] , map_record[i+2][j+3] , map_record[i+3][j+3] , map_record[i+4][j+3] ,
                map_record[i+1][j+4] , map_record[i+3][j+4] , map_record[i+2][j+4])
      erosion.putpixel((i , j) , tmp)

  return erosion


def opening(image):
  opening_image = image.copy()
  image = erosion(image)
  opening_image = dilation(image)
  return opening_image

def closing(image):
  closing_image = image.copy()
  image = dilation(image)
  closing_image = erosion(image)
  return  closing_image

def open_then_close(image):
  return closing(opening(image))

def close_then_open(image):
  return  opening(closing(image))

def write_snr(name , snr):
  file.write(name + ': ' + str(snr) + '\n')

if __name__=='__main__':
  image = init()
  #1
  gaussian_10 = gaussian(image , 10)
  write_snr('gaussian with apt = 10' , SNR(image , gaussian_10))
  gaussian_10.save('gaussian_10.png')
  #2
  gaussian_30 = gaussian(image , 30)
  write_snr('gaussian with apt = 30' , SNR(image , gaussian_30))
  gaussian_30.save('gaussian_30.png')
  #3
  salt_01 = saltandpepper(image , 0.1)
  write_snr('salt-and-pepper with threshold = 0.1' , SNR(image , salt_01))
  salt_01.save('salt_01.png')
  #4
  salt_005 = saltandpepper(image , 0.05)
  write_snr('salt-and-pepper with threshold = 0.5' , SNR(image , salt_005))
  salt_005.save('salt_005.png')
  #5
  gaussian_10_33 = box_filter(gaussian_10 , 3 , 3)
  write_snr('box filter with gaussian(apt = 10) and 3 x 3' , SNR(image , gaussian_10_33))
  gaussian_10_33.save('box_gaussian_10_33.png')
  #6
  gaussian_30_33 = box_filter(gaussian_30 , 3 , 3)
  write_snr('box filter with gaussian(apt = 30) and 3 x 3' , SNR(image , gaussian_30_33))
  gaussian_30_33.save('box_gaussian_30_33.png')
  #7
  gaussain_10_55 = box_filter(gaussian_10 , 5 , 5)
  write_snr('box filter with gaussian(apt = 10) and 5 x 5' , SNR(image , gaussain_10_55))
  gaussain_10_55.save('box_gaussian_10_55.png')
  #8
  gaussian_30_55 = box_filter(gaussian_30 , 5 , 5)
  write_snr('box filter with gaussian(apt = 30) and 5 x 5' , SNR(image , gaussian_30_55))
  gaussian_30_55.save('box_gaussian_30_55.png')
  #9
  gaussian_10_33 = median_filter(gaussian_10 , 3 , 3)
  write_snr('median filter with gaussian(apt = 10) and 3 x 3' , SNR(image , gaussian_10_33))
  gaussian_10_33.save('median_gaussian_10_33.png')
  #10
  gaussian_30_33 = median_filter(gaussian_30 , 3 , 3)
  write_snr('median filter with gaussian(apt = 30) and 3 x 3' , SNR(image , gaussian_30_33))
  gaussian_30_33.save('median_gaussian_30_33.png')
  #11
  gaussain_10_55 = median_filter(gaussian_10 , 5 , 5)
  write_snr('median filter with gaussian(apt = 10) and 5 x 5' , SNR(image , gaussain_10_55))
  gaussain_10_55.save('median_gaussian_10_55.png')
  #12
  gaussian_30_55 = median_filter(gaussian_30 , 5 , 5)
  write_snr('median filter with gaussian(apt = 30) and 5 x 5' , SNR(image , gaussian_30_55))
  gaussian_30_55.save('median_gaussian_30_55.png')
  #13
  gaussian_10_otc = open_then_close(gaussian_10)
  write_snr('open then close with gaussian(apt = 10)' , SNR(image , gaussian_10_otc))
  gaussian_10_otc.save('otc_gaussian_10.png')
  #14
  gaussian_30_otc = open_then_close(gaussian_30)
  write_snr('open then close with gaussian(apt = 30)' , SNR(image , gaussian_30_otc))
  gaussian_30_otc.save('otc_gaussian_30.png')
  #15
  gaussian_10_cto = close_then_open(gaussian_10)
  write_snr('close then open with gaussian(apt = 10)' , SNR(image , gaussian_10_cto))
  gaussian_10_cto.save('cto_gaussian_10.png')
  #16
  gaussian_30_cto = close_then_open(gaussian_30)
  write_snr('close then open with gaussian(apt = 30)' , SNR(image , gaussian_30_cto))
  gaussian_30_cto.save('cto_gaussian_30.png')
  #17
  salt_01_33 = box_filter(salt_01 , 3 , 3)
  write_snr('box filter with salt and pepper(threshold = 0.1) and 3 x 3' , SNR(image , salt_01_33))
  salt_01_33.save('box_salt_01_33.png')
  #18
  salt_005_33 = box_filter(salt_005 , 3 , 3)
  write_snr('box filter with salt and pepper(threshold = 0.05) and 3 x 3' , SNR(image , salt_005_33))
  salt_005_33.save('box_salt_005_33.png')
  #19
  salt_01_55 = box_filter(salt_01 , 5 , 5)
  write_snr('box filter with salt and pepper(threshold = 0.1) and 5 x 5' , SNR(image , salt_01_55))
  salt_01_55.save('box_salt_01_55.png')
  #20
  salt_005_55 = box_filter(salt_005 , 5 , 5)
  write_snr('box filter with salt and pepper(threshold = 0.05) and 5 x 5' , SNR(image , salt_005_55))
  salt_005_55.save('box_salt_005_55.png')
  #21
  salt_01_33 = median_filter(salt_01 , 3 , 3)
  write_snr('median filter with salt and pepper(threshold = 0.1) and 3 x 3' , SNR(image , salt_01_33))
  salt_01_33.save('median_salt_01_33.png')
  #22
  salt_005_33 = median_filter(salt_005 , 3 , 3)
  write_snr('median filter with salt and pepper(threshold = 0.05) and 3 x 3' , SNR(image , salt_005_33))
  salt_005_33.save('median_salt_005_33.png')
  #23
  salt_01_55 = median_filter(salt_01 , 5 , 5)
  write_snr('median filter with salt and pepper(threshold = 0.1) and 5 x 5' , SNR(image , salt_01_55))
  salt_01_55.save('median_salt_01_55.png')
  #24
  salt_005_55 = median_filter(salt_005 , 5 , 5)
  write_snr('median filter with salt and pepper(threshold = 0.05) and 5 x 5' , SNR(image , salt_005_55))
  salt_005_55.save('median_salt_005_55.png')
  #25
  salt_01_otc = open_then_close(salt_01)
  write_snr('open then close with salt and pepper(threshold = 0.1)' , SNR(image , salt_01_otc))
  salt_01_otc.save('otc_salt_01.png')
  #26
  salt_005_otc = open_then_close(salt_005)
  write_snr('open then close with salt and pepper(threshold = 0.05)' , SNR(image , salt_005_otc))
  salt_005_otc.save('otc_salt_005.png')
  #27
  salt_01_cto = close_then_open(salt_01)
  write_snr('close then open with salt and pepper(threshold = 0.1)' , SNR(image , salt_01_cto))
  salt_01_cto.save('cto_salt_01.png')
  #28
  salt_005_cto = close_then_open(salt_005)
  write_snr('close then open with salt and pepper(threshold = 0.05)' , SNR(image , salt_005_cto))
  salt_005_cto.save('cto_salt_005.png')

  file.close()