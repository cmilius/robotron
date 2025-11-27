import os
import pygame
import logging
from pathlib import Path

logger = logging.getLogger(__name__)

BASE_DIR = Path(__file__).resolve().parent
ASSET_DIR = BASE_DIR / "data" / "images"


def load_image(relative_path):
    """
    Load the image at the given file path.

    :param str relative_path: File path to a specific image
    :return: Pygame image
    """
    img_path = ASSET_DIR / relative_path
    img = pygame.image.load(img_path).convert()
    img.set_colorkey((0, 0, 0))
    return img


def load_images(path):
    """
    Load multiple images at a given file path.

    :param str path: File path to an image folder
    :return: List of pygame image
    """
    images = []
    for img_name in os.listdir(os.path.join(ASSET_DIR, path)):
        images.append(load_image(os.path.join(path, img_name)))
    return images
