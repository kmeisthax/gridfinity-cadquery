import gridfinity
from ds import ds_cart_holder, illustration as ds_illustration
from gb import gb_cart_holder, illustration as gb_illustration
from switch import switch_cart_holder, illustration as switch_illustration

ds_cart_holder = ds_cart_holder\
    .rotate([0, 0, 0], [0, 0, -1], 270)\
    .translate([gridfinity.grid_unit * 0.5, gridfinity.grid_unit * 0, 0])

ds_illustration = ds_illustration\
    .rotate([0, 0, 0], [0, 0, -1], 270)\
    .translate([gridfinity.grid_unit * 0.5, gridfinity.grid_unit * 0, 0])

gb_cart_holder = gb_cart_holder\
    .rotate([0, 0, 0], [0, 0, -1], 30)\
    .translate([gridfinity.grid_unit * -2, gridfinity.grid_unit * -1.5, 0])

gb_illustration = gb_illustration\
    .rotate([0, 0, 0], [0, 0, -1], 30)\
    .translate([gridfinity.grid_unit * -2, gridfinity.grid_unit * -1.5, 0])

switch_cart_holder = switch_cart_holder\
    .rotate([0, 0, 0], [0, 0, -1], 150)\
    .translate([gridfinity.grid_unit * -2, gridfinity.grid_unit * 1.5, 0])

switch_illustration = switch_illustration\
    .rotate([0, 0, 0], [0, 0, -1], 150)\
    .translate([gridfinity.grid_unit * -2, gridfinity.grid_unit * 1.5, 0])