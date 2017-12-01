import numpy as np
from keras.preprocessing import image

def __flip__(x, axis=1):
    return np.flip(x, 1)

def __rotate__(x, theta, row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest', cval=0.):
    rotation_matrix = np.array([[np.cos(theta), -np.sin(theta), 0],
                                [np.sin(theta), np.cos(theta), 0],
                                [0, 0, 1]])
    h, w = x.shape[row_axis], x.shape[col_axis]
    transform_matrix = image.transform_matrix_offset_center(rotation_matrix, h, w)
    x = image.apply_transform(x, transform_matrix, channel_axis, fill_mode, cval)
    return x

def __shift__(x, wshift, hshift, row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest', cval=0.):
    h, w = x.shape[row_axis], x.shape[col_axis]
    tx = hshift * h
    ty = wshift * w
    translation_matrix = np.array([[1, 0, tx],
                                   [0, 1, ty],
                                   [0, 0, 1]])
    x = image.apply_transform(x, translation_matrix, channel_axis, fill_mode, cval)
    return x

def __zoom__(x, zx, zy, row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest', cval=0.):
    zoom_matrix = np.array([[zx, 0, 0],
                            [0, zy, 0],
                            [0, 0, 1]])
    h, w = x.shape[row_axis], x.shape[col_axis]
    transform_matrix = image.transform_matrix_offset_center(zoom_matrix, h, w)
    x = image.apply_transform(x, transform_matrix, channel_axis, fill_mode, cval)
    return x

def __shear__(x, shear, row_axis=0, col_axis=1, channel_axis=2, fill_mode='nearest', cval=0.):
    shear_matrix = np.array([[1, -np.sin(shear), 0],
                             [0, np.cos(shear), 0],
                             [0, 0, 1]])
    h, w = x.shape[row_axis], x.shape[col_axis]
    transform_matrix = image.transform_matrix_offset_center(shear_matrix, h, w)
    x = image.apply_transform(x, transform_matrix, channel_axis, fill_mode, cval)
    return x

def __random_flip__(img, mask, u=0.5):
    if np.random.random() < u:
        img = __flip__(img, 1)
        mask = __flip__(mask, 1)
    return img, mask

def __random_rotate__(img, mask, rotate_limit=(-20, 20), u=0.5):
    if np.random.random() < u:
        theta = np.pi / 180 * np.random.uniform(rotate_limit[0], rotate_limit[1])
        img = __rotate__(img, theta)
        mask = __rotate__(mask, theta)
    return img, mask

def __random_shift__(img, mask, w_limit=(-0.1, 0.1), h_limit=(-0.1, 0.1), u=0.5):
    if np.random.random() < u:
        wshift = np.random.uniform(w_limit[0], w_limit[1])
        hshift = np.random.uniform(h_limit[0], h_limit[1])
        img = __shift__(img, wshift, hshift)
        mask = __shift__(mask, wshift, hshift)
    return img, mask

def __random_zoom__(img, mask, zoom_range=(0.8, 1), u=0.5):
    if np.random.random() < u:
        zx, zy = np.random.uniform(zoom_range[0], zoom_range[1], 2)
        img = __zoom__(img, zx, zy)
        mask = __zoom__(mask, zx, zy)
    return img, mask

def __random_shear__(img, mask, intensity_range=(-0.5, 0.5), u=0.5):
    if np.random.random() < u:
        sh = np.random.uniform(-intensity_range[0], intensity_range[1])
        img = __shear__(img, sh)
        mask = __shear__(mask, sh)
    return img, mask

def random_augmentation(img, 
                        mask, 
                        flip_chance=0, 
                        rotate_chance=0,
                        rotate_limit=(-20,20), 
                        shift_chance=0, 
                        shift_limit_w=(-0.1, 0.1), 
                        shift_limit_h=(-0.1, 0.1),
                        zoom_chance=0, 
                        zoom_range=(0.8, 1), 
                        shear_chance=0, 
                        shear_range=(-0.5, 0.5)):

    new_img = np.empty_like(img)
    new_mask = np.empty_like(mask)

    for ind in range(img.shape[0]):

        new_img[ind,:,:,:],new_mask[ind,:,:,:] = __random_flip__(img[ind], 
                                                                 mask[ind], 
                                                                 u=flip_chance)

        new_img[ind,:,:,:],new_mask[ind,:,:,:] = __random_rotate__(new_img[ind], 
                                                                   new_mask[ind], 
                                                                   rotate_limit=rotate_limit,
                                                                   u=rotate_chance)

        new_img[ind,:,:,:],new_mask[ind,:,:,:] = __random_shift__(new_img[ind], 
                                                                  new_mask[ind], 
                                                                  w_limit = shift_limit_w,
                                                                  h_limit=shift_limit_h, 
                                                                  u=shift_chance)

        new_img[ind,:,:,:],new_mask[ind,:,:,:] = __random_zoom__(new_img[ind], 
                                                                 new_mask[ind], 
                                                                 zoom_range=zoom_range,
                                                                 u=zoom_chance)

        new_img[ind,:,:,:],new_mask[ind,:,:,:] = __random_shear__(new_img[ind], 
                                                                  new_mask[ind], 
                                                                  intensity_range=shear_range, u=shear_chance)

    return new_img, new_mask