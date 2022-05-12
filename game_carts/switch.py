from cadquery import cq
import gridfinity
import math

switch_cart_holder = cq.Workplane("XY")\
    .gridfinity_block(2, 1, 4)\
    .gridfinity_block_stack(2, 1)\
    .gridfinity_block_lip(2, 1)

tolerance = 0.75 #used to loosen fit with actual Switch carts
switch_cart_width = 20.8 + tolerance
switch_cart_height = 31.2 + tolerance
switch_cart_depth = 3.675 + tolerance
switch_cart_pin_depth = 0.7
switch_cart_pin_height = 12.7
switch_cart_pin_width = 2
switch_cart_pin_center = 6.725

switch_cart = cq.Workplane("XZ")\
    .rect(switch_cart_width, switch_cart_height)\
    .extrude(switch_cart_depth)\
    .edges("|Y")\
    .fillet(3)\
    .translate([0, switch_cart_depth / 2, switch_cart_height / 2])

#This "pin" is intended to mesh with the backside of the Switch cartridge
#and ensures the cartridge can only go in one way.
switch_cart_pin = cq.Workplane("XZ")\
    .rect(switch_cart_pin_width, switch_cart_pin_height)\
    .extrude(switch_cart_pin_depth)\
    .translate([switch_cart_width / 2 - switch_cart_pin_center, switch_cart_depth / 2, switch_cart_pin_height / 2])

switch_cart = switch_cart.cut(switch_cart_pin)

rows = 3
cols = 3

row_spacing = 2.5
col_spacing = 8.5

row_offset = -1.5

depth_base = 2
depth_offset = 6.5

angle = 20

pick_cutout_lip = 3

pick_cutout = cq.Workplane("XZ")\
    .rect(switch_cart_width, switch_cart_height - pick_cutout_lip)\
    .extrude(row_spacing * 2)\
    .translate([0, switch_cart_depth / -2, switch_cart_height / 2 + pick_cutout_lip])

illustration = cq.Workplane("XY")

for r in range(0, rows):
    for c in range(0, cols):
        r_ctrd = r - rows / 2
        c_ctrd = c - cols / 2
        
        positioned_cart = switch_cart\
             .rotate([0, 0, 0], [-1, 0, 0], angle)\
             .translate([
                r_ctrd * (switch_cart_width + row_spacing) + switch_cart_width / 2 + row_spacing / 2,
                c_ctrd * (switch_cart_depth + col_spacing) + switch_cart_depth / 2 + col_spacing / 2 + row_offset,
                depth_base + c * depth_offset
             ])
        
        switch_cart_holder = switch_cart_holder.cut(positioned_cart)
        
        x = r_ctrd * (switch_cart_width + row_spacing) + switch_cart_width / 2 + row_spacing / 2
        y = c_ctrd * (switch_cart_depth + col_spacing) + switch_cart_depth / 2 + col_spacing / 2 + row_offset
        z = depth_base + c * depth_offset
        
        if c != 0:
            positioned_lip = pick_cutout\
                .rotate([0, 0, 0], [-1, 0, 0], angle)\
                .translate([
                    x,
                    y,
                    z
                ])
            
            switch_cart_holder = switch_cart_holder.cut(positioned_lip)
        else:
            cart_sin = math.sin(angle / 180 * math.pi)
            cart_cos = math.cos(angle / 180 * math.pi)
            cart_o = cart_sin * switch_cart_depth / 2
            cart_a = cart_cos * switch_cart_depth / 2
            
            cart_upper_depth = gridfinity.grid_depth * 2 - gridfinity.block_mating_depth - 0.15
            
            opposite_angle = 180 - (90 - angle) - 90
            opposite_sin = math.tan(opposite_angle / 180 * math.pi)
            opposite_o = opposite_sin * cart_upper_depth
            
            positioned_triangle = cq.Workplane("YZ")\
                .moveTo(y - cart_a, z + cart_o)\
                .lineTo(y - cart_a, z + cart_o + cart_upper_depth)\
                .lineTo(y - cart_a + opposite_o, z + cart_o + cart_upper_depth)\
                .close()\
                .extrude(switch_cart_width)\
                .translate([x - switch_cart_width / 2, 0, 0])
            
            switch_cart_holder = switch_cart_holder.cut(positioned_triangle)
        
        illustration = illustration.union(positioned_cart)

test_jig = cq.Workplane("XY")\
    .rect(switch_cart_width + 2, switch_cart_depth + 2)\
    .extrude(12)\
    .translate([0, 0, -2])\
    .cut(switch_cart)

del switch_cart
del switch_cart_pin
del pick_cutout
del positioned_cart
del positioned_lip
del positioned_triangle