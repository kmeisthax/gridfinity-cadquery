"""Holder for the walking foot that came with my Brother CS7000X"""

import cadquery as cq
import gridfinity

walking_foot_block = cq.Workplane("XY")\
    .gridfinity_block(1, 1, 3)\
    .gridfinity_block_stack(1, 1)\
    .gridfinity_block_lip(1, 1)

FUDGE_FACTOR = 0.5

WALKING_FOOT_WIDTH = 19.62 + FUDGE_FACTOR
WALKING_FOOT_HEIGHT = 27.35 + FUDGE_FACTOR
WALKING_FOOT_DEPTH = 42.56 + FUDGE_FACTOR

walking_foot = cq.Workplane("XY")\
    .rect(WALKING_FOOT_WIDTH, WALKING_FOOT_HEIGHT)\
    .extrude(WALKING_FOOT_DEPTH)\
    .edges(">Y")\
    .edges("<Z")\
    .fillet(WALKING_FOOT_HEIGHT / 2.5)\
    .edges("<Y")\
    .edges("<Z")\
    .chamfer(WALKING_FOOT_HEIGHT / 4, WALKING_FOOT_DEPTH / 3)\
    .edges("<Y")\
    .edges("<Z")\
    .fillet(40)\
    .edges("<Z")\
    .edges("<Y")\
    .fillet(1)

walking_foot_block = walking_foot_block.cut(walking_foot)\
    .edges(cq.NearestToPointSelector([4,0,gridfinity.block_top_surface(3)]))\
    .fillet(1)\
    .edges(cq.NearestToPointSelector([0,4,gridfinity.block_top_surface(3)]))\
    .fillet(1)\
    .edges(cq.NearestToPointSelector([-4,0,gridfinity.block_top_surface(3)]))\
    .fillet(1)\
    .edges(cq.NearestToPointSelector([0,-4,gridfinity.block_top_surface(3)]))\
    .fillet(1)

del walking_foot