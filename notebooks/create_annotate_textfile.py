# %% [markdown]
# ### Creating a text file with "filepath,x1,y1,x2,y2,class_name" format for each bounding box

# %%
import os
import pandas as pd
import numpy as np
import shutil
import csv


# %%
# Reading annotation.csv
annot_df = pd.read_csv("annotations.csv", header=None)
annot_df.head()


# %%
annot_df[0] = annot_df[0].str.replace(
    "C:/Users/35841/rcnn/images_annotation/annots/", ""
)
cross_labelled = annot_df[annot_df[5] == "c"]
cross_labelled = cross_labelled.reset_index(drop=True)
cross_labelled.head()


# %%
data = pd.DataFrame()
data["format"] = cross_labelled[0]
data.head()


# %%
data.head()


# %%
# As the images are in train_images folder, add train_images before the image name
for i in range(data.shape[0]):
    data.iloc[i, 0] = "train_images/" + data.iloc[i, 0]
data.head()


# %%
# Add xmin, ymin, xmax, ymax and class as per the format required and write into annotate.txt
for i in range(data.shape[0]):
    # print(data.iloc[i,0]+str(data.iloc[i,0]))
    data.iloc[i, 0] = (
        data.iloc[i, 0]
        + ","
        + str(cross_labelled.iloc[i, 1])
        + ","
        + str(cross_labelled.iloc[i, 2])
        + ","
        + str(cross_labelled.iloc[i, 3])
        + ","
        + str(cross_labelled.iloc[i, 4])
        + ","
        + str(cross_labelled.iloc[i, 5])
    )

data.to_csv("annotate.txt", header=None, index=None, sep=" ")


# %%
data.shape
