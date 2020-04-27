# Helsinki city: Detect pedestrian crossing
This project is done in collaboration with the city of Helsinki to detect pedestrian crossing from the images

## Get started with model recognizer

```bash
git clone https://github.com/fizyr/keras-retinanet.git
python keras-retinanet/setup.py build_ext --inplace
pip install jupyter pandas
pip install -r keras-retinanet/requirements.txt
cd keras-retinanet && pip install . --user && cd ..
``


## Infrastructure
For details about how to use it, please check [Infra](infra/README.md)


## Problem Defination:

The continuous monitoring of street signals is important to regulate the traffic smoothly and to avoid accidents. There are challanges in maintaining such signals throughout since those involve plannning,time and labour. One of the major challanges is to maintain the pedestrian crossings. Pedestrian crossings may eventaully degrade because of increased traffic , weathering, lack of maintainace etc. It is really difficult to maintain pedestrian crossings from human source information because this causes delay in maintenance and there are high chances that several degraded signals are left out. 

City of Helsinki,Finland is also facing similar situations, which needs immediate attention. For this problem, we are using traditional machine learning approach and deep learning techniques(frcnn,mask rcnn and retinanet) to detect the pedestrian crossing and monitor it's condition from orthophotos(aerial images).


## Discussing Machine Leaning Approach:

Every machine learning task needs the data to learn from it. We fetched the pedestrian crossing data from https://kartta.hel.fi/ using wms api. The code for generating the labelled data is avilable in **fetching_pedestrian_crossing_images.ipynb**

The images fetched from their database not only contained the crossroad images but also contained the images of houses roof, anomalous gray and white stripes, and noisy images(mostly deterioted crossing paintings, shadows etc). Some of the images from the database are shown below. Several experimentation on those images data including anomaly detection and simple classification tasks are included in https://github.com/sangamdeuja/helsinki_crosswalk.

As we checked the maps, we observed some pedestrian crossing that were not actually not part of the database. This is the main motivation of implementing deep neural architecures for pedestrian crossing detection in the first place. Here we discuss about implementation of frcnn.





<img src="miscel_images/2.png" align="left" width="200" height="200">
<img src="miscel_images/3.png"  align="middle" width="200" height="200">
<img src="miscel_images/4.png" align="left" width="200" height="200">
<img src="miscel_images/1.png" align="middle" width="200" height="200">

 

## Deep Learning Approach

### Problems with Convnets 

- The length of output layer is not fixed because the occurrences of the object in an image is not fixed 

- The object could be of any size and at any spatial position, that disables the idea of taking different region of interest followed by classification. 

 

### RCNN (Regional CNN, Ross Girshick et al. https://arxiv.org/abs/1311.2524) 

 

- Uses selective search algorithm to extract just 2000 regions from the image as region proposals 

- The regions from the selective search are fed to CNN to extract the features 

- The extracted features are fed to SVM classifier (Hinge loss/ huber loss) and Bounding box regressor (sum of square error SSE) 

 

### Fast RCNN ,Ross Girshick et al. https://arxiv.org/abs/1504.08083  

- Faster than RCNN 

- Images are fed to convnets to obtain features, identify the region of proposal, apply ROI pooling layer to convert to fixed size for each proposal, apply fully connected layers with SoftMax and bounding box regressor 

 

### Faster RCNN ,Shaoqing Ren et al. https://arxiv.org/abs/1506.01497 

- Faster than both above variations 

- Eliminates the selective search from Fast RCNN, and adds region proposal network (RPN) 

- RPN ranks region boxes(anchors) and proposes the most likely object containing region 

- By default, there are 9 anchors at a position in an image(eg: 3 scales 128,256,512 and 3 aspect ratios of 1:1,1:2,2:1) generates 9 anchors. 

- There are a huge number of anchors generated. In order to reduce them, cross boundary anchors are ignored and the non-maximum suppression(IOU) is applied. 

## Dataset generation and labelling

Image patches of helsinki city were generated using the code **generate_datasets.ipynb**. The training images were manually labelled using labelImg (https://github.com/tzutalin/labelImg)



## FRCNN Implementation And Results

Frcnn implementation is based on https://github.com/kbardool/keras-frcnn . Annotation file was parsed in the form of text file. The xml file generated from labelImg is converted to csv file using **create_annotate_csvfile.ipynb**. The code to generate the annotation file in my context(csv to txt) is available in **create_annotate_textfile.ipynb**. The parameters settings is available in **config.pickle**

<img src="test_images/test_0.png" align="left" width="300" height="300">
<img src="results_imgs/0.png" align="middle" width="300" height="300">


<img src="test_images/test_1.png" align="left" width="300" height="300">
<img src="results_imgs/1.png" align="middle" width="300" height="300">

<img src="test_images/test_2.png" align="left" width="300" height="300">
<img src="results_imgs/2.png" align="middle" width="300" height="300">

<img src="test_images/test_3.png" align="left" width="300" height="300">
<img src="results_imgs/3.png" align="middle" width="300" height="300">


## MaskRCNN (https://arxiv.org/abs/1703.06870)
-Extension of Faster R-CNN that adds an output model for predicting a mask for each detected object.
the annoted image is trained with the maskRCNN and the Some sample pedestrian crossing detection result from Mask R-CNN model are shown below.

<img src="results_imgs/outside_12.png" align="left" width="300" height="300">
<img src="results_imgs/result1.png" align="middle" width="300" height="300">
<img src="results_imgs/train_2340.png" align="left" width="300" height="300">
<img src="results_imgs/result2.png" align="middle" width="300" height="300">

## RetinaNet(https://arxiv.org/abs/1708.02002)

- RetinaNet, an one-stage detector, by using focal loss, 
- lower loss is contributed by “easy” negative samples so that the loss is focusing on “hard” samples, which improves the prediction accuracy.
- a backbone network called Feature Pyramid Net, which is built on top of ResNet and is responisble for computing convolutional feature maps of an entire image
- a subnetwork responsible for performing object classification using the backbone’s output
- a subnetwork responsible for performing bounding box regression using the backbone’s output.

<img src="results_imgs/fig_1.jpg"  width="500" height="300">

the annoted image is trained with the Retinanet and the Some sample pedestrian crossing detection result from RetinaNet model are shown below.


<img src="results_imgs/pred.png"  width="300" height="300">
<img src="results_imgs/Screenshot from 2020-01-16 09-23-49.png"  align="left" width="300" height="300">
<img src="results_imgs/ret.png"  align="middle" width="300" height="300">





## Extracting latitude and longitude 

If we have the geo-coordinates of image of interest and the size of image, it is easy to extract the cordinates of the pedestrian crossing by mapping the predicted bounding box. The code for extracting the coordinates of crossing is available in 
**extract_coordinate.ipynb**



## Applications
- Identification of unlablled pedestrian crossing. This helps keeping database update.
- Monitor the conditions if the painting is required.
- Estimating the price incurring for repainting within specific area/city

