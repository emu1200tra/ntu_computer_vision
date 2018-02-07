from PIL import Image

def init():
  image = Image.open('lena.bmp')
  (w , h) = image.size
  image_list = [[0 for i in range(h+2)] for j in range(w+2)]
  image_list_big = [[0 for i in range(h+10)] for j in range(w+10)]
  for i in range(w):
    for j in range(h):
      image_list[i+1][j+1] = image.getpixel((i , j))
      image_list_big[i+5][j+5] = image.getpixel((i , j))

  return image , image_list , image_list_big

def lapla_mask(iamge , image_list , kernel , threshold , parameter):
  counter = 0
  (w , h) = image.size
  record = [[0 for i in range(h+2)] for j in range(w+2)]
  for i in range(w):
    for j in range(h):
      for k in [-1 , 0 , 1]:
        for l in [-1 , 0 , 1]:
          counter += image_list[i+1+k][j+1+l] * kernel[1+k][1+l]
      counter *= parameter
      if counter > threshold:
        record[i+1][j+1] = 1
      elif -counter > threshold:
        record[i+1][j+1] = -1
      else:
        record[i+1][j+1] = 0
      counter = 0
  lapla_mask_image = image.copy()
  for i in range(w):
    for j in range(h):
      lapla_mask_image.putpixel((i , j) , 255)
      if record[i+1][j+1] == 1:
        for k in [-1 , 0 , 1]:
          for l in [-1 , 0 , 1]:
            if record[i+1+k][j+1+l] == -1:
              lapla_mask_image.putpixel((i , j) , 0)
  return lapla_mask_image

def lapla_mask_big(image , image_list , kernel , threshold , parameter):
  counter = 0
  (w , h) = image.size
  record = [[0 for i in range(h+10)] for j in range(w+10)]
  range_list = [i for i in range(-5 , 6)]
  for i in range(w):
    for j in range(h):
      for k in range_list:
        for l in range_list:
          counter += image_list[i+5+k][j+5+l] * kernel[5+k][5+l]
      counter *= parameter
      if counter > threshold:
        record[i+5][j+5] = 1
      elif -counter > threshold:
        record[i+5][j+5] = -1
      else:
        record[i+5][j+5] = 0
      counter = 0
  lapla_mask_image = image.copy()
  for i in range(w):
    for j in range(h):
      lapla_mask_image.putpixel((i , j) , 255)
      if record[i+5][j+5] == 1:
        for k in range_list:
          for l in range_list:
            if record[i+5+k][j+5+l] == -1:
              lapla_mask_image.putpixel((i , j) , 0)
  return lapla_mask_image


if __name__ == "__main__":

  image , image_list , image_list_big = init()
  lapla_mask_image = lapla_mask(image , image_list , [[0 , 1 , 0] , [1 , -4 , 1] , [0 , 1 , 0]] , 15 , 1)
  lapla_mask_image.save("lapla_mask_image1.png")
  lapla_mask_image2 = lapla_mask(image , image_list , [[1 , 1 , 1] , [1 , -8 , 1] , [1 , 1 , 1]] , 15 , (1.0/3.0))
  lapla_mask_image2.save("lapla_mask_image2.png")
  min_variance_lapla_image = lapla_mask(image , image_list , [[2 , -1 , 2] , [-1 , -4 , -1] , [2 , -1 , 2]] , 20 , (1.0/3.0))
  min_variance_lapla_image.save("min_variance_lapla_image.png")
  mask1 = [[0 , 0 , 0 , -1 , -1 , -2 , -1 , -1 , 0 , 0 , 0] ,
           [0 , 0 , -2 , -4 , -8 , -9 , -8 , -4 , -2 , 0 , 0] ,
           [0 , -2 , -7 , -15 , -22 , -23 , -22 , -15 , -7 , -2 , 0] ,
           [-1 , -4 , -15 , -24 , -14 , -1 , -14 , -24 , -15 , -4 , -1] ,
           [-1 , -8 , -22 , -14 , 52 , 103 , 52 , -14 , -22 , -8 , -1] ,
           [-2 , -9 , -23 , -1 , 103 , 178 , 103 , -1 , -23 , -9 , -2] ,
           [-1 , -8 , -22 , -14 , 52 , 103 , 52 , -14 , -22 , -8 , -1] ,
           [-1 , -4 , -15 , -24 , -14 , -1 , -14 , -24 , -15 , -4 , -1] ,
           [0 , -2 , -7 , -15 , -22 , -23 , -22 , -15 , -7 , -2 , 0] ,
           [0 , 0 , -2 , -4 , -8 , -9 , -8 , -4 , -2 , 0 , 0] ,
           [0 , 0 , 0 , -1 , -1 , -2 , -1 , -1 , 0 , 0 , 0]]
  Laplace_of_Gaussian_image = lapla_mask_big(image , image_list_big , mask1 , 3000 , 1)
  Laplace_of_Gaussian_image.save("Laplace_of_Gaussian_image.png")
  mask2 = [[-1 , -3 , -4 , -6 , -7 , -8 , -7 , -6 , -4 , -3 , -1] ,
           [-3 , -5 , -8 , -11 , -13 , -13 , -13 , -11 , -8 , -5 , -3] ,
           [-4 , -8 , -12 , -16 , -17 , -17 , -17 , -16 , -12 , -8 , -4] ,
           [-6 , -11 , -16 , -16 , 0 , 15 , 0 , -16 , -16 , -11 , -6] ,
           [-7 , -13 , -17 , 0 , 85 , 160 , 85 , 0 , -17 , -13 , -7] ,
           [-8 , -13 , -17 , 15 , 160 , 283 , 160 , 15 , -17 , -13 , -8] ,
           [-7 , -13 , -17 , 0 , 85 , 160 , 85 , 0 , -17 , -13 , -7] ,
           [-6 , -11 , -16 , -16 , 0 , 15 , 0 , -16 , -16 , -11 , -6] ,
           [-4 , -8 , -12 , -16 , -17 , -17 , -17 , -16 , -12 , -8 , -4] ,
           [-3 , -5 , -8 , -11 , -13 , -13 , -13 , -11 , -8 , -5 , -3] ,
           [-1 , -3 , -4 , -6 , -7 , -8 , -7 , -6 , -4 , -3 , -1]]
  Difference_of_Gaussian_image = lapla_mask_big(image , image_list_big , mask2 , 1 , 1)
  Difference_of_Gaussian_image.save("Difference_of_Gaussian_image.png")
