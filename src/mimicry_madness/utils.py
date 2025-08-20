import numpy as np

from PIL import Image

def tight_crop_rgba_image(img: Image.Image):
    """Images with transparent background will be tightly cropped to the bounds of the first pixels with any alpha value.
    Returns cropped image

    Args:
        img (Image.Image): RGBA image to be tightly cropped
    """
    
    masked_img = np.array(img)
    assert masked_img.shape[2] == 4, "input image must have 4 channels (RGBA)"
    
    ymin, ymax = None, None
    xmin, xmax = None, None
    for y in range(masked_img.shape[0]):
        v = masked_img[y, :, 3].sum()
        if v > 0:
            ymin = y
            break
            
    for y in range(masked_img.shape[0]-1, -1, -1):
        v = masked_img[y, :, 3].sum()
        if v > 0:
            ymax = y
            break
    
    for x in range(masked_img.shape[1]):
        v = masked_img[:, x, 3].sum()
        if v > 0:
            xmin = x
            break
            
    for x in range(masked_img.shape[1]-1 , -1, -1):
        v = masked_img[:, x, 3].sum()
        if v > 0:
            xmax = x
            break
    
    #print(f"Frame {i}: ymin={ymin}, ymax={ymax}, xmin={xmin}, xmax={xmax}")
    masked_img = masked_img[ymin:ymax, xmin:xmax, :]
    
    return Image.fromarray(masked_img)