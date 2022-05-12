import cadquery as cq
import gridfinity
import math

#All units are mm
#TODO: Adding the tolerance in the later calculations breaks all the cutout math

tolerance = 0.75 #used to loosen fit with DS cards
ds_cart_width = 32.85
ds_cart_height = 34.96
ds_cart_depth = 3.80

ds_pcb_depth = 2.52
ds_pins_width = 25
ds_pins_height = 10.56

ds_pins_x_left = 3.12
ds_pins_x_right = 4.18

ds_fillet_radius = 0.5
ds_wide_fillet_radius = 3

#3DS carts have an extra tab on the top right to prevent insertion into a DS/DSi
#We construct a 3DS profile purely so I can make sure the tab doesn't intersect
#with the holder.
threeds_tab_width = 34.92 - ds_cart_width
threeds_tab_height = 6.45

threeds_cart_profile = cq.Sketch()\
    .segment(((ds_cart_width + tolerance) / 2 + threeds_tab_width, (ds_cart_height + tolerance) / 2),
             ((ds_cart_width + tolerance) / 2 + threeds_tab_width, (ds_cart_height + tolerance) / 2 - threeds_tab_height))\
    .segment(((ds_cart_width + tolerance) / 2, (ds_cart_height + tolerance) / 2 - threeds_tab_height))\
    .segment(((ds_cart_width + tolerance) / 2, (ds_cart_height + tolerance) / -2))\
    .segment(((ds_cart_width + tolerance) / -2, (ds_cart_height + tolerance) / -2))\
    .segment(((ds_cart_width + tolerance) / -2, (ds_cart_height + tolerance) / 2))\
    .close()\
    .assemble(tag='face')\
    .vertices(">(-10, -10, 0)")\
    .fillet(ds_wide_fillet_radius)\
    .faces()\
    .vertices()\
    .fillet(ds_fillet_radius)

threeds_pins_profile = cq.Sketch()\
    .rect(ds_pins_width - tolerance, ds_pins_height + tolerance)\
    .moved(cq.Location(cq.Vector(ds_pins_width / -2 - ds_cart_width / -2 - ds_pins_x_left, ds_pins_height / 2 - ds_cart_height / 2 - tolerance)))

threeds_cart = cq.Workplane("XZ")\
    .placeSketch(threeds_cart_profile)\
    .extrude(ds_cart_depth)\
    .faces("|Y and <Z")\
    .workplane()\
    .placeSketch(threeds_pins_profile)\
    .cutBlind(ds_cart_depth - ds_pcb_depth)

ds_cart_holder = cq.Workplane("XY")\
    .gridfinity_block(1, 1, 4)\
    .gridfinity_block_stack(1, 1)\
    .gridfinity_block_lip(1, 1)

rows = 1
cols = 3

row_spacing = 4.5
col_spacing = 8.5

row_offset = 6.5

depth_base = 20
depth_offset = 6.5

angle = 20

pick_cutout_lip = 5

pick_cutout = cq.Workplane("XZ")\
    .rect(ds_cart_width, ds_cart_height - pick_cutout_lip)\
    .extrude(row_spacing * 2)\
    .translate([0, ds_cart_depth / -2, ds_cart_height / 2 + pick_cutout_lip])

illustration = cq.Workplane("XY")

for r in range(0, rows):
    for c in range(0, cols):
        r_ctrd = r - rows / 2
        c_ctrd = c - cols / 2
        
        positioned_cart = threeds_cart\
             .rotate([0, 0, 0], [-1, 0, 0], angle)\
             .translate([
                r_ctrd * (ds_cart_width + row_spacing) + ds_cart_width / 2 + row_spacing / 2,
                c_ctrd * (ds_cart_depth + col_spacing) + ds_cart_depth / 2 + col_spacing / 2 + row_offset,
                depth_base + c * depth_offset
             ])
        
        ds_cart_holder = ds_cart_holder.cut(positioned_cart)
        
        x = r_ctrd * (ds_cart_width + row_spacing) + ds_cart_width / 2 + row_spacing / 2
        y = c_ctrd * (ds_cart_depth + col_spacing) + ds_cart_depth / 2 + col_spacing / 2 + row_offset
        z = depth_base + c * depth_offset
        
        cart_sin = math.sin(angle / 180 * math.pi)
        cart_cos = math.cos(angle / 180 * math.pi)
        cart_o = cart_sin * (ds_cart_depth + tolerance) / 2
        cart_a = cart_cos * (ds_cart_depth + tolerance) / 2
        
        cart_upper_depth = gridfinity.grid_depth * 2 - gridfinity.block_mating_depth - 0.15
        
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
                .extrude(ds_cart_width + tolerance)\
                .translate([x - (ds_cart_width + tolerance) / 2, y - ds_cart_depth * 3, z - ds_cart_height / 2 + tolerance * 2])
            
            lip = cq.Workplane("YZ")\
                .moveTo(-row_spacing * 2.5, pick_cutout_lip)\
                .lineTo(opposite_o, pick_cutout_lip)\
                .lineTo(opposite_o, 0)\
                .lineTo(-row_spacing * 2.5, 0)\
                .close()\
                .extrude(ds_cart_width + tolerance)\
                .translate([x - (ds_cart_width + tolerance) / 2, y - ds_cart_depth * 3, z - ds_cart_height / 2 + tolerance * 2])
            
            positioned_triangle = positioned_triangle.cut(lip)
        else:
            positioned_triangle = cq.Workplane("YZ")\
                .moveTo(cart_a, cart_o)\
                .lineTo(cart_a, cart_o + cart_upper_depth)\
                .lineTo(cart_a + opposite_o, cart_o + cart_upper_depth)\
                .close()\
                .extrude(ds_cart_width + tolerance)\
                .translate([x - (ds_cart_width + tolerance) / 2, y - ds_cart_depth * 3, z - ds_cart_height / 2 + tolerance * 2])
        
        ds_cart_holder = ds_cart_holder.cut(positioned_triangle)
        
        illustration = illustration.union(positioned_cart)

test_jig = cq.Workplane("XY")\
    .rect(ds_cart_width + tolerance + 2, ds_cart_depth + tolerance + 2)\
    .extrude(12)\
    .translate([0, 0, -2])\
    .cut(threeds_cart.translate([0, ds_cart_depth / 2, ds_cart_height / 2]))

del pick_cutout
del positioned_cart
del lip
del positioned_triangle
del threeds_cart