import numpy as np
from keras.preprocessing.image import img_to_array, load_img
from os.path import join
from lib import augmentations

def image_generator(images_dir, masks_dir, images, masks, batch_size, img_width = None, num_colors = 256):
    '''
    images: Array of image names
    masks: Array of mask names
    batch_size: The number of images to be consider in one batch.
    num_colors = target number of colors for kmeans algorithm. (Default = 256)
    img_width: The width to which the original image is resized while maintaining aspect ratio. Does not resize if no parameters passed.
    '''
    
    img_dim = [int((1280 / 1918) * img_width), img_width] if img_width is not None else None
    
    while True:
        random_indices = np.random.choice(len(images), batch_size)
        i = []
        m = []
        
        for index in random_indices:
            
            img = load_img(join(images_dir, images[index]), target_size = img_dim)
            img_array = img_to_array(img) / 255
            
            mask = load_img(join(masks_dir, masks[index]), target_size = img_dim)
            mask_array = img_to_array(mask) / 255
            
            img_array, mask_array = augmentations.random_augmentation(img_array, mask_array)
            
            i.append(img_array)
            m.append(mask_array)
            
        yield np.array(i), np.array(m)