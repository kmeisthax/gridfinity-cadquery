from cadquery import cq
import gridfinity

width = 3
height = 3

block = cq.Workplane("XY")\
    .gridfinity_block(width, height, 3)\
    .gridfinity_block_stack(width, height)\
    .gridfinity_block_lip(width, height)