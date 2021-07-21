class SoundBar:
    def __init__(self, sprite_sheet):
        self.sprite = sprite_sheet.VOLUME[10]
        self.non_blank_chunks = 20

    def user_click(self, mouse_x, mouse_y, sprite_sheet, sounds):
        if sprite_sheet.TILE_SIZE * 12 <= mouse_y <= sprite_sheet.TILE_SIZE * 12 + sprite_sheet.TILE_SIZE:
            if sprite_sheet.TILE_SIZE * 20.5 <= mouse_x <= sprite_sheet.TILE_SIZE * 20.5 + sprite_sheet.TILE_SIZE * 4:
                numerator = mouse_x - sprite_sheet.TILE_SIZE * 20.5
                index = ((numerator / (sprite_sheet.TILE_SIZE * 4)) * self.non_blank_chunks)
                if index <= .4:
                    index = index.__floor__()
                else:
                    index = index.__ceil__()
                self.sprite = sprite_sheet.VOLUME[index]
                sounds.set_volume(index * .05)

    def my_sprite(self):
        return self.sprite
