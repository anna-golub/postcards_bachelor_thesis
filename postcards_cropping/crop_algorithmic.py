from skimage import io
import cv2
import numpy as np
from PIL import Image


def crop_image(filename):
    image = io.imread(filename)
    try:
        if field_type(image) == 'white':
            image_cropped = corner_cropping(image)
        elif field_type(image) == 'coloured':
            image_cropped = contrast_cropping(image)
        return image_cropped
    except IndexError:
        return image


def contrast_cropping(image):
    threshold = 2 ** 12
    sample_width_hor = 5
    head = 5
    n = 12

    height = image.shape[0]
    width = image.shape[1]
    pix = Image.fromarray(image).load()

    upper = \
        sorted(
            [get_upper_bound(pix, i * (width // n), sample_width_hor, head, threshold, height) for i in range(1, n)])[2]
    lower = \
        sorted(
            [get_lower_bound(pix, i * (width // n), sample_width_hor, head, threshold, height) for i in range(1, n)])[
            -2]
    sample_width_vert = 5
    left = \
        sorted(
            [get_left_bound(pix, i * (height // n), sample_width_vert, head, threshold, width) for i in range(1, n)])[2]
    right = \
        sorted(
            [get_right_bound(pix, i * (height // n), sample_width_vert, head, threshold, width) for i in range(1, n)])[
            -2]

    frame = 15
    upper = max(upper - frame, 0)
    lower = min(lower + frame, height - 1)
    left = max(left - frame, 0)
    right = min(right + frame, width - 1)
    crop_img = image[upper: lower, left:right]
    return crop_img


def get_average_hor(pix, i, mid, sample_width):  # average R, G, B
    R = G = B = 0
    for k in range(mid - sample_width, mid + sample_width):
        R += pix[k, i][0]
        G += pix[k, i][1]
        B += pix[k, i][2]
    R /= (2 * sample_width)
    G /= (2 * sample_width)
    B /= (2 * sample_width)
    return R, G, B


def get_average_vert(pix, i, mid, sample_width):
    R = G = B = 0
    for k in range(mid - sample_width, mid + sample_width):
        R += pix[i, k][0]
        G += pix[i, k][1]
        B += pix[i, k][2]
    R /= (2 * sample_width)
    G /= (2 * sample_width)
    B /= (2 * sample_width)
    return R, G, B


def delta(R, G, B, colours):
    return (colours[0] - R) ** 2 + (colours[1] - G) ** 2 + (colours[2] - B) ** 2


def get_upper_bound(pix, mid, sample_width, head, threshold, height):
    R = B = G = 0
    for i in range(head):
        average = get_average_hor(pix, i, mid, sample_width)
        R += average[0]
        G += average[1]
        B += average[2]
    R /= head
    G /= head
    B /= head

    H = 0
    for i in range(head, height):
        average = get_average_hor(pix, i, mid, sample_width)
        if delta(R, G, B, average) > threshold:
            if delta(R, G, B,
                     get_average_hor(pix, i + 1, mid, sample_width)) > threshold:
                H = i
                break
    return H


def get_lower_bound(pix, mid, sample_width, head, threshold, height):
    R = B = G = 0
    H = 0
    for i in range(head):
        average = get_average_hor(pix, height - i - 1, mid, sample_width)
        R += average[0]
        G += average[1]
        B += average[2]
    R /= head
    G /= head
    B /= head
    for i in range(height - 1, 0, -1):
        average = get_average_hor(pix, i, mid, sample_width)
        if delta(R, G, B, average) > threshold:
            if delta(R, G, B, get_average_hor(pix, i - 1, mid, sample_width)) > threshold:
                H = i
                break
    return H


def get_left_bound(pix, mid, sample_width, head, threshold, width):
    R = B = G = 0
    H = 0
    for i in range(head):
        average = get_average_vert(pix, i, mid, sample_width)
        R += average[0]
        G += average[1]
        B += average[2]
    R /= head
    G /= head
    B /= head
    for i in range(head, width):
        average = get_average_vert(pix, i, mid, sample_width)
        if delta(R, G, B, average) > threshold:
            if delta(R, G, B, get_average_vert(pix, i + 1, mid, sample_width)) > threshold:
                H = i
                break
    return H


def get_right_bound(pix, mid, sample_width, head, threshold, width):
    R = B = G = 0
    H = 0
    for i in range(head):
        average = get_average_vert(pix, width - i - 1, mid, sample_width)
        R += average[0]
        G += average[1]
        B += average[2]
    R /= head
    G /= head
    B /= head
    for i in range(width - 1, 0, -1):
        average = get_average_vert(pix, i, mid, sample_width)
        if delta(R, G, B, average) > threshold:
            if delta(R, G, B, get_average_vert(pix, i - 1, mid, sample_width)) > threshold:
                H = i
                break
    return H


def corner_cropping(image):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = np.float32(gray)
    dst = cv2.cornerHarris(gray, 12, 3, 0.00001)
    dst = cv2.dilate(dst, None)

    height = image.shape[0]
    width = image.shape[1]
    frame = 15
    rows = np.where(np.any(dst > 0.005 * dst.max(), axis=1))
    upper = max(rows[0][0] - frame, 0)
    lower = min(rows[0][-1] + frame, height - 1)
    columns = np.where(np.any(dst > 0.005 * dst.max(), axis=0))
    left = max(columns[0][0] - frame, 0)
    right = min(columns[0][-1] + frame, width - 1)
    image_cropped = image[upper:lower, left:right]
    return image_cropped


def field_type(image):
    left_upper = is_white(image[:20, :20])
    right_upper = is_white(image[:20, -20:])
    left_lower = is_white(image[-20:, :20])
    right_lower = is_white(image[-20:, -20:])
    if left_upper + right_upper + left_lower + right_lower > 1:
        return "white"
    else:
        return "coloured"


def is_white(image):
    height = image.shape[0]
    width = image.shape[1]
    s = 0
    for i in range(height):
        for j in range(width):
            R = image[i][j][0]
            G = image[i][j][2]
            B = image[i][j][1]
            if R > 150 and B > 150 and G > 150:
                s += 1
    if s / (height * width) > 0.9:
        return 1
    else:
        return 0


# main cropping function
def crop_algorithmic(input_filename, ouput_filename):
    cropped = crop_image(input_filename)
    cropped = Image.fromarray(cropped)
    cropped.save(ouput_filename)
