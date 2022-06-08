from re import X
import cadquery as cq
import gridfinity

#The height of the label lip on divider bins.
label_lip_height = 11.75 - 2#mm

#How deep we want our covers to be.
depth = 3.5#mm

extra_depth = gridfinity.block_mating_depth - depth

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

def topplate(w, h):
    """Generate a top cover for a set of height-leveled Gridfinity blocks.
    
    This is basically the inverse of a baseplate."""

    with_cutouts = cq.Workplane("XY")\
        .gridfinity_block(w, h, 0.5)\
        .gridfinity_block_lip(w, h, holes=False)\
        .faces(">Z")\
        .edges(cq.NearestToPointSelector([(w * gridfinity.grid_unit / 2), (h * gridfinity.grid_unit / 2), gridfinity.block_extrusion(1)]))\
        .fillet(gridfinity.block_stacking_lip / 2)
    
    return with_cutouts

def midplate(w, h):
    """Generate a vertical divider, which is essentially a thin baseplate that
    can be stacked on top of other storage blocks.
    
    The purpose of vertical dividers are to prevent blocks with magnets from
    magnetizing parts in divider bins stacked below them. They're sort of like
    weighted baseplates, except they are sized to stack as if they were 1x tall
    blocks."""

    with_cutouts = cq.Workplane("XY")\
        .gridfinity_block(w, h, 1)\
        .gridfinity_block_lip(w, h, holes=False)\
        .faces(">Z")\
        .rarray(gridfinity.grid_unit, gridfinity.grid_unit, w, h)\
        .eachpoint(lambda c: cq.Workplane("XY")\
                .placeSketch(gridfinity.inset_profile(1, 1, gridfinity.block_mating_inset))\
                .extrude(gridfinity.stacking_mating_depth * -1)\
                .val()\
                .moved(c)\
                .moved(cq.Location(cq.Vector(0, 0, gridfinity.block_extrusion(1)))),
            combine="cut",
            clean=True)
    
    filleted = with_cutouts
    
    for i in range(0, w):
        for j in range(0, h):
            x = (i * gridfinity.grid_unit) - (w * gridfinity.grid_unit / 2) + gridfinity.block_mating_inset
            y = (j * gridfinity.grid_unit) - (h * gridfinity.grid_unit / 2) + gridfinity.block_mating_inset
            z = gridfinity.block_extrusion(1)

            try:
                filleted = filleted\
                    .edges(cq.NearestToPointSelector([x + gridfinity.grid_unit / 2, y + gridfinity.grid_unit / 2, z]))\
                    .chamfer(gridfinity.block_mating_inset - gridfinity.block_spacing * 0.5 - gridfinity.block_stacking_lip)\
                    .edges(cq.NearestToPointSelector([x + gridfinity.grid_unit / 2, y + gridfinity.grid_unit / 2, z - gridfinity.block_mating_depth]))\
                    .chamfer(gridfinity.block_stacking_chamfer)\
                    .faces(">Z")\
                    .edges(cq.NearestToPointSelector([x, y, z]))\
                    .fillet(gridfinity.block_stacking_lip / 2)
            except:
                continue
    
    return filleted\
            .faces(">Z")\
            .edges(cq.NearestToPointSelector([(w * gridfinity.grid_unit / 2), (h * gridfinity.grid_unit / 2), gridfinity.block_extrusion(1)]))\
            .fillet(gridfinity.block_stacking_lip / 2)

cover = cover(1, 1)
divider = midplate(1, 1)
top = topplate(1, 1)