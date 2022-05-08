from cadquery import cq
import gridfinity

width = 3
height = 3

block = cq.Workplane("XY")\
    .placeSketch(gridfinity.inset_profile(width, height, gridfinity.block_spacing / 2))\
    .extrude(20)\
    .gridfinity_block_lip(width, height)