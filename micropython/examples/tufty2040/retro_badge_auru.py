# A retro badge with photo and QR code.
# Copy your image to your Tufty alongside this example - it should be a 120 x 120 jpg.

import retro_badge_base

badge = retro_badge_base.Badge()

# 2bit Demichrome colour palette by Space Sandwich - https://lospec.com/palette-list/2bit-demichrome
badge.LIGHTEST = (239, 249, 214)
badge.LIGHT = (122, 28, 75)
badge.DARK = (186, 80, 68)
badge.DARKEST = (27, 3, 38)

badge.set_colors(badge.DARKEST, badge.DARK, badge.LIGHT, badge.LIGHTEST)

badge.COMPANY_NAME = "Belka MNT factory"
badge.NAME = "Aurunemaru" 
badge.BLURB1 = "RP2040 plus 320x240 TFT LCD"
badge.BLURB2 = "C# / Python dev, nomrpbot creator"
badge.BLURB3 = "Will work for Coffee"

badge.QR_TEXT = "t.me/aurunemaru"

badge.IMAGE_NAME = "auru.jpg"

badge.main_loop()
