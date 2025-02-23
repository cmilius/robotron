import pygame
import json

class SpriteSheet:
    def __init__(self, filename):
        self.sprite_sheet = pygame.image.load(filename).convert()

        # Load the meta data for the sprite sheet
        self.meta_data = filename.replace('png', 'json')
        with open(self.meta_data) as f:
            self.data = json.load(f)
        f.close()

    def get_sprite(self, x, y, width, height):
        """Get a single sprite from the sprite sheet.
        
        :return: Sprite surface
        """

        sprite = pygame.Surface((width, height)).convert()              # define an empty surface
        sprite.set_colorkey((255, 255, 255))                            # set the color key for transparency
        sprite.blit(self.sprite_sheet, (0, 0), (x, y, width, height))   # copy the sprite from the sprite sheet to the surface
        return sprite                                                   # return the surface
    
    def get_sprites(self, x, y, width, height, rows, cols, x_padding=0, y_padding=0):
        """Get a grid of sprites from the sprite sheet.
        
        :return: List of sprite surfaces
        """

        # TODO: Right now this only works for a grid of same-size sprites. This may need updated if the sprites in the sheet aren't uniform in size.
        sprites = []        
        for row in range(rows):
            #row padding
            if row > 0:
                    y += y_padding

            for col in range(cols):
                #column padding
                if col > 0:
                    x += x_padding

                sprite = self.get_sprite(x + col * width, y + row * height, width, height)
                sprites.append(sprite)
        return sprites

    def parse_sprites(self, entity_name):
        """Parse the sprite sheet for a specific entity.
        
        :return: List of sprite surfaces
        """

        sprite = self.data[self.meta_data.rsplit('/', 1)[1]][entity_name]
        sprite_frame = sprite['frame']
        return self.get_sprites(sprite_frame['x'], sprite_frame['y'], sprite_frame['w'], sprite_frame['h'], sprite['rows'], sprite['cols'], sprite['padding']['x'], sprite['padding']['y'])
