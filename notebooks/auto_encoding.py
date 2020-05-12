
# %%
from PIL import Image
import os, numpy as np

folder = 'C:/Users/35841/images/phase2_crossroad_images_1/'
filelist=os.listdir(folder)
for fichier in filelist:
    if not(fichier.endswith(".png")):
        filelist.remove(fichier)
read = lambda imname: np.asarray(Image.open(imname).convert("RGB"))
ims = [read(os.path.join(folder, filename)) for filename in filelist]
im_array = np.array(ims, dtype='uint8')


# %%
X = im_array.astype('float32') / 255.0 - 0.5


# %%
from sklearn.model_selection import train_test_split
X_train, X_test = train_test_split(X, test_size=0.5, random_state=42)


# %%
from keras.layers import Dense, Flatten, Reshape, Input, InputLayer
from keras.models import Sequential, Model

def build_autoencoder(img_shape, code_size):
    # The encoder
    encoder = Sequential()
    encoder.add(InputLayer(img_shape))
    encoder.add(Flatten())
    encoder.add(Dense(code_size))

    # The decoder
    decoder = Sequential()
    decoder.add(InputLayer((code_size,)))
    decoder.add(Dense(np.prod(img_shape))) # np.prod(img_shape) is the same as 32*32*3, it's more generic than saying 3072
    decoder.add(Reshape(img_shape))

    return encoder, decoder


# %%
im_array.shape


# %%
IMG_SHAPE = im_array.shape[1:]
IMG_SHAPE


# %%
IMG_SHAPE = im_array.shape[1:]
encoder, decoder = build_autoencoder(IMG_SHAPE, 2)

inp = Input(IMG_SHAPE)
code = encoder(inp)
reconstruction = decoder(code)

autoencoder = Model(inp,reconstruction)
autoencoder.compile(optimizer='adamax', loss='mse')

print(autoencoder.summary())


# %%
history = autoencoder.fit(x=X_train, y=X_train, epochs=100,
                validation_data=[X_test, X_test])


# %%
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


# %%
import matplotlib.pyplot as plt
def show_image(x):
    plt.imshow(np.clip(x + 0.5, 0, 1))


# %%
def visualize(img,encoder,decoder):
    """Draws original, encoded and decoded images"""
    # img[None] will have shape of (1, 32, 32, 3) which is the same as the model input
    code = encoder.predict(img[None])[0]
    reco = decoder.predict(code[None])[0]

    plt.subplot(1,3,1)
    plt.title("Original")
    show_image(img)

    plt.subplot(1,3,2)
    plt.title("Code")
    plt.imshow(code.reshape([code.shape[-1]//2,-1]))

    plt.subplot(1,3,3)
    plt.title("Reconstructed")
    show_image(reco)
    plt.show()

for i in range(5):
    img = X_test[i]
    #print(img[None][0])
    print(img[None])
    #visualize(img,encoder,decoder)


# %%
nrsamples = im_array.shape[0]
print(nrsamples)
code_vectors = np.zeros((nrsamples,2))

for i in range(nrsamples):
    img = X[i]
    code = encoder.predict(img[None])[0]
    
    #print(code)
    code_vectors[i,:]=code
    
code_vectors.shape


# %%
plt.scatter(code_vectors[:,0], code_vectors[:,1])
plt.show()


# %%
#!pip install mahalanobis


# %%
import mahalanobis
m_dist = mahalanobis.Mahalanobis(code_vectors,code_vectors.shape[0])


# %%
arr=np.zeros(len(code_vectors))
non_crossroad=np.where(m_dist.distances>2.0)
indices=non_crossroad[0]
len(indices)


# %%
arr[indices]=-1


# %%
fig=plt.figure(figsize=(50,50))
for i in range(1,len(indices)+1):
    plt.subplot(12,7,i)
    plt.imshow(im_array[indices[i-1]])


# %%
plt.scatter(code_vectors[:,0], code_vectors[:,1],c=arr)
plt.show()


# %%
#It seems from above results that the noise are basically the shadows
# The preprocessing needs histogram equilization?


# %%
#Let's implement DBSCAN to identify the noises and see if the result matches with above


# %%
from sklearn.cluster import DBSCAN


# %%
code_vectors


# %%
clustering = DBSCAN(eps=1, min_samples=4).fit(code_vectors)


# %%
np.unique(clustering.labels_)


# %%
plt.scatter(code_vectors[:,0], code_vectors[:,1], c=clustering.labels_);


# %%
noise_index=[]
points=code_vectors[clustering.labels_==-1]
for item in points:
    a=np.where(code_vectors==item)
    noise_index.append(a[0][0])
len(noise_index)    


# %%
fig=plt.figure(figsize=(50,50))
for i in range(1,len(noise_index)+1):
    plt.subplot(10,5,i)
    plt.imshow(im_array[noise_index[i-1]])


# %%



# %%
a


# %%
a[0].shape


# %%



