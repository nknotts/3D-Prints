#!/usr/bin/env python3

import argparse

import qrcode
import numpy as np
import openpyscad as ops

WIDTH_MM = 50
BORDER_MM = 5
THICKNESS_MM = 4
CORNER_RADIUS_MM = 5
QR_OFFSET_MM = 0.4
CYLINDER_RESOLUTION = 100


def main(qr_payload):
    qrcode.make(qr_payload).save('keychain_qr_code.png')
    qr = qrcode.QRCode(version=1,
                       box_size=1,
                       error_correction=qrcode.ERROR_CORRECT_M,
                       border=0)
    qr.add_data(qr_payload)
    qr.make(fit=True)
    img = qr.make_image(fill_color='black',
                        back_color='white')
    img_array = np.array(img)

    # generate qr code
    qr_raw = ops.Union()
    for i in range(img.width):
        for j in range(img.width):
            if not img_array[i, j]:
                qr_raw.append(ops.Cube([1, 1, 1]).translate([i, j, 0]))

    # scale qr code to desired size
    qr_width_mm = WIDTH_MM - 2*BORDER_MM
    qr_sf = qr_width_mm / img.width
    qr_scaled = qr_raw.scale([qr_sf, qr_sf, QR_OFFSET_MM*2]
                             ).translate([BORDER_MM, BORDER_MM, THICKNESS_MM-QR_OFFSET_MM])

    # generate base
    base = ops.Hull()
    base.append(ops.Cylinder(h=THICKNESS_MM, r=CORNER_RADIUS_MM, _fn=CYLINDER_RESOLUTION)
                .translate([CORNER_RADIUS_MM, CORNER_RADIUS_MM, 0]))
    base.append(ops.Cylinder(h=THICKNESS_MM, r=CORNER_RADIUS_MM, _fn=CYLINDER_RESOLUTION)
                .translate([CORNER_RADIUS_MM, WIDTH_MM-CORNER_RADIUS_MM, 0]))
    base.append(ops.Cylinder(h=THICKNESS_MM, r=CORNER_RADIUS_MM, _fn=CYLINDER_RESOLUTION)
                .translate([WIDTH_MM-CORNER_RADIUS_MM, WIDTH_MM-CORNER_RADIUS_MM, 0]))
    base.append(ops.Cylinder(h=THICKNESS_MM, r=CORNER_RADIUS_MM, _fn=CYLINDER_RESOLUTION)
                .translate([WIDTH_MM-CORNER_RADIUS_MM, CORNER_RADIUS_MM, 0]))

    # combined together and add key chain corner
    result = (base - qr_scaled) + \
        ops.Cylinder(h=THICKNESS_MM, r=CORNER_RADIUS_MM, _fn=CYLINDER_RESOLUTION) - \
        ops.Cylinder(h=THICKNESS_MM*3, r=CORNER_RADIUS_MM *
                     0.5, _fn=CYLINDER_RESOLUTION).translate([0, 0, -THICKNESS_MM])

    result.write('keychain_qr_code.scad')


if __name__ == '__main__':
    parser = argparse.ArgumentParser('Generate QR Code openscad keychain')
    parser.add_argument('payload')
    args = parser.parse_args()

    main(args.payload)
