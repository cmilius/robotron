import pygame

class SpriteSheet:
    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename).convert()

    def get_sprite(self, x, y, width, height):
        """Get a single sprite from the sprite sheet.
        
        :return: Sprite surface
        """

        sprite = pygame.Surface((width, height)).convert()              # define an empty surface
        #sprite.set_colorkey((0, 0, 0))                                 # set the color key for transparency
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))   # copy the sprite from the sprite sheet to the surface
        return sprite                                                   # return the surface
    
    def get_sprites(self, x, y, width, height, rows, cols):
        """Get a grid of sprites from the sprite sheet.
        
        :return: List of sprite surfaces
        """

        # TODO: Right now this only works for a grid of same-size sprites. This may need updated if the sprites in the sheet aren't uniform in size.
        sprites = []
        for row in range(rows):
            for col in range(cols):
                sprite = self.get_sprite(x + col * width, y + row * height, width, height)
                sprites.append(sprite)
        return sprites

