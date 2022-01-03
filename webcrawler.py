import requests
image_url='https://p0.ssl.qhimg.com/t01e890e06c93018fa8.jpg'
r = requests.get(image_url)
with open('./img1/image1.png','wb') as f:
  f.write(r.content)