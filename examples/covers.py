import cadquery as cq
import gridfinity

#The height of the label lip on divider bins.
label_lip_height = 11.75 - 2#mm

#How deep we want our covers to be.
depth = 3.5#mm

extra_depth = gridfinity.block_mating_depth - depth

##TODO: Cutting holes in the illustration breaks CADQuery something fierce.
illustration = cq.Workplane("XY")\
    .gridfinity_block(1, 1, 3)\
    .gridfinity_block_stack(1, 1)\
    .gridfinity_block_lip(1, 1)\
    .translate((0, 0, -gridfinity.block_extrusion(3) - gridfinity.stacking_clearance_depth))\

def giant_block_lip(w, h):
    """Generate a block lip *without* the usual divisions between grid units.

    e.g. for a 3x2 block, it will generate one large solid shape that mates
    with it, rather than six arranged in a grid.
    
    This block lip will not mate to a baseplate but it will mate to a stacking
    lip."""
    x = -(w * gridfinity.grid_unit / 2) + gridfinity.block_mating_inset
    y = -(h * gridfinity.grid_unit / 2) + gridfinity.block_mating_inset
    
    return cq.Workplane("XY")\
        .gridfinity_block(w, h, 1)\
        .faces("<Z")\
        .placeSketch(gridfinity.inset_profile(w, h, gridfinity.block_mating_inset))\
        .extrude(gridfinity.block_mating_depth * -1)\
        .edges("<Z")\
        .chamfer(gridfinity.block_mating_chamfer)\
        .edges(cq.NearestToPointSelector([x, y, 0]))\
        .chamfer(gridfinity.block_mating_inset - gridfinity.block_spacing * 0.5 - 0.01)

def cover(w, h):
    return giant_block_lip(w, h)\
        .faces(">Y")\
        .workplane()\
        .transformed((0,0,0), (0, -extra_depth, 0))\
        .rect(gridfinity.grid_unit * w, gridfinity.block_extrusion(1) + extra_depth, centered = [True, False])\
        .cutBlind(-100)\
        .faces(">Z")\
        .workplane(centerOption='CenterOfBoundBox')\
        .transformed((0,0,0), (0, -gridfinity.top_surface_length(h) / 2 - 20, 0))\
        .rect(gridfinity.grid_unit * w, label_lip_height + 20, centered = [True, False])\
        .cutBlind(-100)\
        .faces("<Y")\
        .edges("<Z")\
        .chamfer(2.5)\
        .faces("<Y")\
        .edges(">Z")\
        .fillet(0.25)

cover = cover(1, 1)