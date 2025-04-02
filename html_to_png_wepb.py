from PIL import Image

file = 'input'

try:
    webp_img = Image.open('./cache/' + str(file) + '.png')
    webp_img.save('./cache/' + str(file) + '.webp', "WEBP", quality=84)
    print(f"Conversion successful: {'./cache/' + str(file) + '.webp'}")
except Exception as e:
    print("Error occurred during PNG to WEBP conversion.")
