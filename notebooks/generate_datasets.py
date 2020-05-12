# %% [markdown]
# ### The code below fetches the image patches of helsinki region.

# %%
# Importing the required libraries
from owslib.wms import WebMapService
import os


# %%
# api for extracting the aerial image
wms = WebMapService("https://kartta.hel.fi/ws/geoserver/avoindata/wms", version="1.3.0")


# %%
## minX,minY,maxX,maxY are the geographical latitudes and longitudes of interset
minX = 24.94516252
minY = 60.18375355
maxX = 24.97737761
maxY = 60.19965233
min_x_cord = []
max_x_cord = []
min_y_cord = []
max_y_cord = []
img_name = []
a = np.linspace(minX, maxX, 30)
b = np.linspace(minY, maxY, 30)
counter = 0
imgpath = "C:/Users/35841/images/moredata4/"
image_files = [f for f in os.listdir(imgpath)]

##Creating patches for the image. Number of images = 29*29
for i in range(0, len(a) - 1):
    for j in range(0, len(b) - 1):
        image_name = "train_" + str(counter)
        if not image_files:
            img = wms.getmap(
                layers=["Ortoilmakuva_2019_5cm"],
                srs="EPSG:4123",
                bbox=(a[i], b[j], a[i + 1], b[j + 1]),
                size=(500, 500),
                format="image/png",
                transparent=True,
            )
            out = open("C:/Users/35841/images/moredata4/" + image_name + ".png", "wb")
            out.write(img.read())
            out.close()
        min_x_cord.append(a[i])
        min_y_cord.append(b[j])
        max_x_cord.append(a[i + 1])
        max_y_cord.append(b[j + 1])
        img_name.append(image_name)
        counter += 1


# %%
