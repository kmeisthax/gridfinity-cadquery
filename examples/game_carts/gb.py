import cadquery as cq
import gridfinity
import math

# Since we're using the cartridge model to cut slots out of a block, we make
# the cartridge slightly thicker than it should be. If you want an accurate
# model of just the cart, set this to 0 (or copy the `gb_cart` into another
# file and remove the `tolerance`)
# 
# A tolerance of 0.75 gives you a fit about as snug as the actual handheld's
# cartridge slot. This is too snug for a storage device, IMO, but if you want
# your cart holder to feel like an actual slot then reduce this back down.
tolerance = 0.9
slot_tolerance = 0.25

#Base dimensions of a Game Boy cart.
gb_cart_width = 57.10
gb_cart_height = 64.50
gb_cart_depth = 7.85

gb_slot_cutout_width = 52.30
gb_slot_cutout_depth = 3.90
gb_slot_cutout_height = 10.47
gb_pcb_depth = 2.19

gb_chamfer_radius = 2.10
gb_chamfer_length = 38.01

#Game Boy carts (and *only* Game Boy carts) have a cutout that prevents removal
#of the cartridge while the system is powered up. For some reason, this feature
#was removed on the Color, and Color-exclusive carts actually lack this cutout
#specifically to prohibit play on DMG/MGB units.
gb_cutout_height = gb_cart_height - 62
gb_cutout_width = gb_cart_width - 51.90

gb_cart = cq.Workplane("YZ")\
    .rect(gb_cart_width + tolerance, gb_chamfer_length + tolerance)\
    .extrude(gb_cart_depth)\
    .faces(">X")\
    .edges("|Z")\
    .chamfer(gb_chamfer_radius)\
    .faces(">Z")\
    .workplane()\
    .center(gb_cart_depth / 2, 0)\
    .rect(gb_cart_depth, gb_cart_width + tolerance)\
    .extrude(gb_cart_height - gb_chamfer_length)\
    .faces("<Z")\
    .workplane()\
    .center(-gb_cart_depth / 2 + gb_slot_cutout_depth + tolerance, 0)\
    .rect(gb_slot_cutout_depth + tolerance - slot_tolerance, gb_slot_cutout_width - tolerance)\
    .cutBlind(-gb_slot_cutout_height - tolerance)\
    .faces(">X")\
    .workplane()\
    .center((gb_cart_width + tolerance) / 2 - gb_cutout_width / 2, gb_cart_height + tolerance - gb_cutout_height / 2)\
    .rect(gb_cutout_width, gb_cutout_height)\
    .cutThruAll()\
    .translate([-gb_cart_depth, 0, 0])\
    .rotate([0, 0, 0], [0, 0, 1], 270)

gba_cart_height = 34.70

# GBA has a slightly narrowed inner slot cutout to prevent insertion into
# earlier consoles.
gba_narrow_slot_width = 51.28 # measured inside the slot
gba_narrow_slot_depth = 4.05 # measured from back of cartridge to slot

# GBA cartridges also have a top lip which makes the cartridge slightly wider
# at the top.
gba_lip_width = 60.10
gba_lip_height = 7.11

gba_cart = cq.Workplane("YZ")\
    .moveTo((gba_lip_width + tolerance) / 2, (gba_cart_height + tolerance) / 2)\
    .lineTo((gba_lip_width + tolerance) / 2, (gba_cart_height + tolerance) / 2 - gba_lip_height)\
    .lineTo((gb_cart_width + tolerance) / 2, (gba_cart_height + tolerance) / 2 - gba_lip_height)\
    .lineTo((gb_cart_width + tolerance) / 2, (gba_cart_height + tolerance) / -2)\
    .lineTo((gb_cart_width + tolerance) / -2, (gba_cart_height + tolerance) / -2)\
    .lineTo((gb_cart_width + tolerance) / -2, (gba_cart_height + tolerance) / 2 - gba_lip_height)\
    .lineTo((gba_lip_width + tolerance) / -2, (gba_cart_height + tolerance) / 2 - gba_lip_height)\
    .lineTo((gba_lip_width + tolerance) / -2, (gba_cart_height + tolerance) / 2)\
    .close()\
    .extrude(gb_cart_depth)\
    .faces("<Z")\
    .workplane()\
    .center(gb_slot_cutout_depth + tolerance, 0)\
    .moveTo((gb_slot_cutout_depth - tolerance - slot_tolerance) / 2, (gb_slot_cutout_width - tolerance) / -2)\
    .lineTo((gb_slot_cutout_depth - tolerance - slot_tolerance) / 2, (gb_slot_cutout_width - tolerance) / 2)\
    .lineTo((gb_slot_cutout_depth + tolerance) / -2 + (gb_slot_cutout_depth - gba_narrow_slot_depth + gb_pcb_depth), (gb_slot_cutout_width - tolerance) / 2)\
    .lineTo((gb_slot_cutout_depth + tolerance) / -2 + (gb_slot_cutout_depth - gba_narrow_slot_depth + gb_pcb_depth), (gba_narrow_slot_width - tolerance) / 2)\
    .lineTo((gb_slot_cutout_depth + tolerance - slot_tolerance) / -2, (gba_narrow_slot_width - tolerance) / 2)\
    .lineTo((gb_slot_cutout_depth + tolerance - slot_tolerance) / -2, (gba_narrow_slot_width - tolerance) / -2)\
    .lineTo((gb_slot_cutout_depth + tolerance) / -2 + (gb_slot_cutout_depth - gba_narrow_slot_depth + gb_pcb_depth), (gba_narrow_slot_width - tolerance) / -2)\
    .lineTo((gb_slot_cutout_depth + tolerance) / -2 + (gb_slot_cutout_depth - gba_narrow_slot_depth + gb_pcb_depth), (gb_slot_cutout_width - tolerance) / -2)\
    .close()\
    .cutBlind(-gb_slot_cutout_height - tolerance)\
    .faces(">X")\
    .edges(">(0, 1, -1) or >(0, -1, -1)")\
    .chamfer(gb_chamfer_radius)\
    .edges("#Y and >Z")\
    .fillet(gb_chamfer_radius)\
    .faces(">X")\
    .edges(">Y or <Y or >Z")\
    .chamfer(gb_chamfer_radius)\
    .translate([-gb_cart_depth, 0, (gb_chamfer_length + tolerance) / -2 + (gba_cart_height + tolerance) / 2])\
    .rotate([0, 0, 0], [0, 0, 1], 270)

# The above models are nice for illustrations... but if I just cut them
# straight into a block, we'll get a nice impression of the chamfers that I
# don't want.
# 
# Instead, here's a 'simplified' version that lacks the chamfers.
union_cart = cq.Workplane("YZ")\
    .moveTo((gba_lip_width + tolerance) / 2, (gba_cart_height + tolerance) / 2)\
    .lineTo((gba_lip_width + tolerance) / 2, (gba_cart_height + tolerance) / 2 - gba_lip_height)\
    .lineTo((gb_cart_width + tolerance) / 2, (gba_cart_height + tolerance) / 2 - gba_lip_height)\
    .lineTo((gb_cart_width + tolerance) / 2, (gba_cart_height + tolerance) / -2)\
    .lineTo((gb_cart_width + tolerance) / -2, (gba_cart_height + tolerance) / -2)\
    .lineTo((gb_cart_width + tolerance) / -2, (gba_cart_height + tolerance) / 2 - gba_lip_height)\
    .lineTo((gba_lip_width + tolerance) / -2, (gba_cart_height + tolerance) / 2 - gba_lip_height)\
    .lineTo((gba_lip_width + tolerance) / -2, (gba_cart_height + tolerance) / 2)\
    .close()\
    .extrude(gb_cart_depth)\
    .faces("<Z")\
    .workplane()\
    .center(gb_slot_cutout_depth + tolerance, 0)\
    .moveTo((gb_slot_cutout_depth - tolerance - slot_tolerance) / 2, (gb_slot_cutout_width - tolerance) / -2)\
    .lineTo((gb_slot_cutout_depth - tolerance - slot_tolerance) / 2, (gb_slot_cutout_width - tolerance) / 2)\
    .lineTo((gb_slot_cutout_depth + tolerance) / -2 + (gb_slot_cutout_depth - gba_narrow_slot_depth + gb_pcb_depth), (gb_slot_cutout_width - tolerance) / 2)\
    .lineTo((gb_slot_cutout_depth + tolerance) / -2 + (gb_slot_cutout_depth - gba_narrow_slot_depth + gb_pcb_depth), (gba_narrow_slot_width - tolerance) / 2)\
    .lineTo((gb_slot_cutout_depth + tolerance - slot_tolerance) / -2, (gba_narrow_slot_width - tolerance) / 2)\
    .lineTo((gb_slot_cutout_depth + tolerance - slot_tolerance) / -2, (gba_narrow_slot_width - tolerance) / -2)\
    .lineTo((gb_slot_cutout_depth + tolerance) / -2 + (gb_slot_cutout_depth - gba_narrow_slot_depth + gb_pcb_depth), (gba_narrow_slot_width - tolerance) / -2)\
    .lineTo((gb_slot_cutout_depth + tolerance) / -2 + (gb_slot_cutout_depth - gba_narrow_slot_depth + gb_pcb_depth), (gb_slot_cutout_width - tolerance) / -2)\
    .close()\
    .cutBlind(-gb_slot_cutout_height - tolerance)\
    .translate([-gb_cart_depth, 0, (gb_chamfer_length + tolerance) / -2 + (gba_cart_height + tolerance) / 2])\
    .rotate([0, 0, 0], [0, 0, 1], 270)

gb_cart_holder = cq.Workplane("XY")\
    .gridfinity_block(3, 1, 4)\
    .gridfinity_block_stack(3, 1)\
    .gridfinity_block_lip(3, 1)

rows = 2
cols = 2

row_spacing = 4.0
col_spacing = 12.5

row_offset = 0

depth_base = 23
depth_offset = 8.0

angle = 20

pick_cutout_lip = 10

pick_cutout = cq.Workplane("XZ")\
    .rect(gb_cart_width, gb_cart_height - pick_cutout_lip)\
    .extrude(row_spacing * 2)\
    .translate([0, gb_cart_depth / -2, gb_cart_height / 2 + pick_cutout_lip])

illustration = cq.Workplane("XY")

for r in range(0, rows):
    r_ctrd = r - rows / 2

    for c in range(0, cols):
        c_ctrd = c - cols / 2
        
        positioned_cart = union_cart\
             .rotate([0, 0, 0], [-1, 0, 0], angle)\
             .translate([
                r_ctrd * (gb_cart_width + row_spacing) + gb_cart_width / 2 + row_spacing / 2,
                c_ctrd * (gb_cart_depth + col_spacing) + gb_cart_depth / 2 + col_spacing / 2 + row_offset,
                depth_base + c * depth_offset
             ])
        
        gb_cart_holder = gb_cart_holder.cut(positioned_cart)
        
        x = r_ctrd * (gb_cart_width + row_spacing) + gb_cart_width / 2 + row_spacing / 2
        y = c_ctrd * (gb_cart_depth + col_spacing) + gb_cart_depth / 2 + col_spacing / 2 + row_offset
        z = depth_base + c * depth_offset
        
        cart_sin = math.sin(angle / 180 * math.pi)
        cart_cos = math.cos(angle / 180 * math.pi)
        cart_o = cart_sin * (gb_cart_depth + tolerance) / 2
        cart_a = cart_cos * (gb_cart_depth + tolerance) / 2
        
        cart_upper_depth = gridfinity.grid_depth * 4 - gridfinity.block_mating_depth - 0.15
        
        opposite_angle = 180 - (90 - angle) - 90
        opposite_sin = math.tan(opposite_angle / 180 * math.pi)
        opposite_o = opposite_sin * cart_upper_depth
        
        if c != 0:
            positioned_triangle = cq.Workplane("YZ")\
                .moveTo(cart_a - row_spacing * 2.5, cart_o)\
                .lineTo(cart_a - row_spacing * 2.5, cart_o + cart_upper_depth)\
                .lineTo(cart_a + opposite_o, cart_o + cart_upper_depth)\
                .lineTo(cart_a, cart_o)\
                .close()\
                .extrude(gb_cart_width + tolerance)\
                .translate([x - (gb_cart_width + tolerance) / 2, y - gb_cart_depth * 1.36, z - gb_cart_height / 3 + tolerance * 2])
        else:
            positioned_triangle = cq.Workplane("YZ")\
                .moveTo(cart_a, cart_o)\
                .lineTo(cart_a, cart_o + cart_upper_depth)\
                .lineTo(cart_a + opposite_o, cart_o + cart_upper_depth)\
                .close()\
                .extrude(gb_cart_width + tolerance)\
                .translate([x - (gb_cart_width + tolerance) / 2, y - gb_cart_depth * 1.36, z - gb_cart_height / 3 + tolerance * 2])
        
        lip = cq.Workplane("YZ")\
            .moveTo(-row_spacing * 2.5, pick_cutout_lip)\
            .lineTo(opposite_o, pick_cutout_lip)\
            .lineTo(opposite_o, 0)\
            .lineTo(-row_spacing * 2.5, 0)\
            .close()\
            .extrude(gb_cart_width + tolerance)\
            .translate([x - (gb_cart_width + tolerance) / 2, y - gb_cart_depth * 1.36, z - gb_cart_height / 3 + tolerance * 2])
        
        positioned_triangle = positioned_triangle.cut(lip)
        
        gb_cart_holder = gb_cart_holder.cut(positioned_triangle)
        
        if c != 0:
            illustration = illustration.union(gb_cart\
                .rotate([0, 0, 0], [-1, 0, 0], angle)\
                .translate([
                    r_ctrd * (gb_cart_width + row_spacing) + gb_cart_width / 2 + row_spacing / 2,
                    c_ctrd * (gb_cart_depth + col_spacing) + gb_cart_depth / 2 + col_spacing / 2 + row_offset,
                    depth_base + c * depth_offset
                ])
            )
        else:
            illustration = illustration.union(gba_cart\
                .rotate([0, 0, 0], [-1, 0, 0], angle)\
                .translate([
                    r_ctrd * (gb_cart_width + row_spacing) + gb_cart_width / 2 + row_spacing / 2,
                    c_ctrd * (gb_cart_depth + col_spacing) + gb_cart_depth / 2 + col_spacing / 2 + row_offset,
                    depth_base + c * depth_offset
                ])
            )

test_jig = cq.Workplane("XY")\
    .rect(gb_cart_width + tolerance + 2, gb_cart_depth + tolerance + 2)\
    .extrude(gb_slot_cutout_height + 4)\
    .translate([0, 0, -2])\
    .cut(union_cart.translate([0, gb_cart_depth / -2, gb_chamfer_length / 2]))

del gb_cart
del gba_cart
del union_cart
del pick_cutout
del positioned_cart
del positioned_triangle
del lip