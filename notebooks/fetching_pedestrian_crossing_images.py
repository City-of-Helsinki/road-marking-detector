# %% [markdown]
# # Fetching the pedestrian crossing of selected region from helsinki city. https://kartta.hel.fi/
#
#
# %% [markdown]
# ### Follow the steps to get the images from the database
# - Go to the lnk above. And go to **layers** ==> **Pedestrian and bicycle paths** ==>  **Routes** ==> click on **Pedestrian crossings**
# - Click on **Download** button which takes you to **Data Exporter**. Select **Draw Search Area** and **Inside Search Area**.     Draw the box of desired size on map.
# - Finally select the format you need. For example **GeoPackage** and click **Download**
#    (**Note:** Excel file don't retrive any coordinates information)

# %%
# Import the required geopandas library and dependencies(fiona). I am importing pandas which is handy for data cleaning
import geopandas
import fiona
import pandas as pd


# %%
# Reading geaopakage file format
file = geopandas.read_file(
    "C:/Users/35841/Downloads/_20191205_145349/klinj_suojatie.gpkg"
)
df = pd.DataFrame(file)
df.geometry = df.geometry.astype("str")
df["geometry"] = (
    df["geometry"]
    .str.replace("LINESTRING ", "")
    .str.replace(",", "")
    .str.replace("(", "")
    .str.replace(")", "")
)
print(df.loc[0, "geometry"])
print(df.loc[1, "geometry"])
print(df.loc[2, "geometry"])
print(df.loc[3, "geometry"])
# insconsistent order of minx and maxx
# inconsistent order of miny and maxy


# %%
df[["min_x", "max_y", "max_x", "min_y", "a", "b"]] = df["geometry"].str.split(
    " ", expand=True
)
df = df.drop(columns=["a", "b", "geometry"])
df["id"] = df["gml_id"].str.replace("klinj_suojatie.", "")


# %%
df["min_x"] = df["min_x"].astype(float)
df["min_y"] = df["min_y"].astype(float)
df["max_x"] = df["max_x"].astype(float)
df["max_y"] = df["max_y"].astype(float)
df


# %%
# Fixing inconsistencies
df.min_x, df.max_x = np.where(
    df.min_x > df.max_x, [df.max_x, df.min_x], [df.min_x, df.max_x]
)
df.min_y, df.max_y = np.where(
    df.min_y > df.max_y, [df.max_y, df.min_y], [df.min_y, df.max_y]
)


# %%
# WMS api allows you to download the images
from owslib.wms import WebMapService
import os

wms = WebMapService("https://kartta.hel.fi/ws/geoserver/avoindata/wms", version="1.3.0")
for i in range(0, len(df)):
    img = wms.getmap(
        layers=["Ortoilmakuva_2019_5cm"],
        srs="EPSG:3879",
        bbox=(
            df.loc[i, "min_x"],
            df.loc[i, "min_y"],
            df.loc[i, "max_x"],
            df.loc[i, "max_y"],
        ),
        size=(100, 100),
        format="image/png",
        transparent=True,
    )
    out = open(
        "images/phase2_crossroad_images_1/" + str(df.loc[i, "id"]) + ".png", "wb"
    )
    out.write(img.read())
    out.close()


# %%
