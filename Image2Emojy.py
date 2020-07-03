# image to emojy
from PIL import Image
import numpy as np
import sys

# Global

# Pixels of an icon
ICON_SIZE = 20

#Functions

# Func that crop the image
def crop_icon(img, row, col):
    return img.crop((col * ICON_SIZE, row * ICON_SIZE,(col + 1) * ICON_SIZE, (row + 1) * ICON_SIZE))

# Get a three dimensional histogram from the image
def img_hist(img):
    arr = np.array(img.getdata(), np.uint8)
    return np.histogramdd(arr[:,:-1], bins = 6, range = [[0, 256]] * 3, weights = arr[:,3])[0]

# Determine simple euclidean distance (by subtructig one hist from the other)
def hist_distance(hist1, hist2):
    return np.linalg.norm(hist1 - hist2)


# open image - emojy
icons_image = Image.open("C:/Users/15108/Downloads/emoji_sprite.png")
#"C:\Users\15108\Downloads\all-emoji.png"
# Determine how many icons in the image (height and whidth)
x_size, y_size = icons_image.size
x_icons = x_size // ICON_SIZE
y_icons = y_size // ICON_SIZE



# Crop the image into icons 
#icons = [crop_icon(icons_image, row, col) for col in range(x_icons) for row in range(y_icons)]
icons = []
for row in range (y_icons):
    for col in range (x_icons):
        icons.append(crop_icon(icons_image, row, col))

# Calculate histogram of every icon
icon_hists = list(map(img_hist, icons))

# Open image - original (and convert to RGBA)
# img_filename = sys.argv[1]
img = Image.open("C:/Users/15108/Downloads/1195384.jpg").convert('RGBA')
#img = Image.open("C:/Users/15108/Downloads/emoticon.jpg").convert('RGBA')

# Get height and whidth of the image
x_size, y_size = img.size

# Round down the size of the image to accommodate a round number of icons 
x_size -= (x_size % ICON_SIZE)
y_size -= (y_size % ICON_SIZE)

# Creatig the new image (white backround)
new_img = Image.new("RGB", (x_size, y_size), "white")

# let's paste the icons in the right place
for row in range(y_size // ICON_SIZE):
    for col in range(x_size // ICON_SIZE):
        region_hist = img_hist(crop_icon(img, row, col))
        icon = min(enumerate(icons),
            key = lambda icon: hist_distance(icon_hists[icon[0]], region_hist))[1]
        new_img.paste(icon, (col * ICON_SIZE, row * ICON_SIZE),
            mask = icon.split()[3])

# save the new image
#new_img.save(img_filename + '.out.png')
im1 = new_img.save('C:/Users/15108/Downloads/finally.out.png')
# show the new image
new_img.show()






