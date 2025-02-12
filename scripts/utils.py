import os
import pygame
import logging

logger = logging.getLogger(__name__)

BASE_IMG_PATH = "data/images/"


def load_image(path):
    """
    Load the image at the given file path.

    :param str path: File path to a specific image
    :return: Pygame image
    """
    img = pygame.image.load(os.path.join(BASE_IMG_PATH, path)).convert()  # .convert() for efficient rendering
    img.set_colorkey((0, 0, 0))  # erase black background
    return img


def load_images(path):
    """
    Load multiple images at a given file path.

    :param str path: File path to an image folder
    :return: List of pygame image
    """
    images = []
    for img_name in os.listdir(os.path.join(BASE_IMG_PATH, path)):
        images.append(load_image(os.path.join(path, img_name)))
    return images
