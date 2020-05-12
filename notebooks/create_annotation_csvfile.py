# %% [markdown]
# ### Creating annotation.csv and arranging the images in corresponding folders of our needs

# %%
import os
import pandas as pd
import numpy as np
import shutil
import zipfile
import urllib
import xml.etree.ElementTree as ET
import csv


# %%
# After labelling the images using labelImg "https://github.com/tzutalin/labelImg", the code below creates the annotaion file
ANNOTATIONS_FILE = "annotations.csv"
CLASSES_FILE = "classes.csv"

annotations = []
classes = set([])
DATASET_DIR = "C:/Users/35841/rcnn/images_annotation/annots/"
for xml_file in [f for f in os.listdir(DATASET_DIR) if f.endswith(".xml")]:
    tree = ET.parse(os.path.join(DATASET_DIR, xml_file))
    root = tree.getroot()

    file_name = None

    for elem in root:
        if elem.tag == "filename":
            file_name = os.path.join(DATASET_DIR, elem.text)

        if elem.tag == "object":
            obj_name = None
            coords = []
            for subelem in elem:
                if subelem.tag == "name":
                    obj_name = subelem.text
                if subelem.tag == "bndbox":
                    for subsubelem in subelem:
                        coords.append(subsubelem.text)
            item = [file_name] + coords + [obj_name]
            annotations.append(item)
            classes.add(obj_name)

with open(ANNOTATIONS_FILE, "w") as f:
    writer = csv.writer(f)
    writer.writerows(annotations)

with open(CLASSES_FILE, "w") as f:
    for i, line in enumerate(classes):
        f.write("{},{}\n".format(line, i))

print("Files created")


# %%
annot_df = pd.read_csv("annotations.csv", header=None)
annot_df.head(5)


# %%
annot_df.info()


# %%
annot_df[0] = annot_df[0].str.replace(
    "C:/Users/35841/rcnn/images_annotation/annots/", ""
)
cross_labelled = annot_df[annot_df[5] == "c"]
cross_labelled.head()


# %%
image_files = [f for f in os.listdir("C:/Users/35841/rcnn/images_annotation/images/")]


# %%
cross_labelled.shape[0]


# %%
if not [f for f in os.listdir("C:/Users/35841/rcnn/images_annotation/c_images/")]:
    for i in range(0, cross_labelled.shape[0]):
        if cross_labelled.iloc[i, 0] in image_files:
            forename = cross_labelled.iloc[i, 0].split(".")[0]

            # print(cross_labelled.iloc[i,0])
            # print(forename)
            shutil.copyfile(
                "C:/Users/35841/rcnn/images_annotation/annots/" + forename + ".xml",
                "C:/Users/35841/rcnn/images_annotation/c_annots/" + forename + ".xml",
            )
            shutil.copyfile(
                "C:/Users/35841/rcnn/images_annotation/images/"
                + cross_labelled.iloc[i, 0],
                "C:/Users/35841/rcnn/images_annotation/c_images/"
                + cross_labelled.iloc[i, 0],
            )


# %%
