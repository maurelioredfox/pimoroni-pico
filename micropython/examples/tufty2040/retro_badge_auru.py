# A retro badge with photo and QR code.
# Copy your image to your Tufty alongside this example - it should be a 120 x 120 jpg.

import retro_badge_base

badge = retro_badge_base.Badge()

# 2bit Demichrome colour palette by Space Sandwich - https://lospec.com/palette-list/2bit-demichrome
badge.LIGHTEST = (233, 239, 236)
badge.LIGHT = (160, 160, 139)
badge.DARK = (85, 85, 104)
badge.DARKEST = (33, 30, 32)

badge.set_colors(badge.LIGHTEST, badge.LIGHT, badge.DARK, badge.DARKEST)

badge.COMPANY_NAME = "Belka MNT factory"
badge.NAME = "Aurunemaru" 
badge.BLURB1 = "RP2040 plus 320x240 TFT LCD"
badge.BLURB2 = "C# / Python dev, maker of nomrpbot"
badge.BLURB3 = "Will work for Yorkshire Gold"

badge.QR_TEXT = "t.me/aurunemaru"

badge.IMAGE_NAME = "auru.jpg"

badge.main_loop()
