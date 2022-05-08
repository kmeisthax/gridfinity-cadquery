import cadquery as cq
from math import sqrt, pow

## CADQuery helper utilities for designing Gridfinity blocks
## Gridfinity is a storage block system designed by Zach Freedman.

## Gridfinity basic parameters - don't touch unless you really want a custom
## grid that won't mate with anything on Thingiverse!
## 
## All dimensions derived from original Zach STLs with Blender.

# The size of a 1x1 baseplate.
grid_unit = 42 #mm

# The margin between two 1x1 storage blocks placed next to each other on a
# baseplate.
block_spacing = 0.5 #mm

## Mating surface

# Master radius for all fillets on the mating surfaces of a baseplate and
# block.
# 
# Fillet radius decreases in concert with the rectangle being rounded off
# such that all fillets have the same origin.
fillet_radius = 4 #mm

# The total depth of the block mating surface.
block_mating_depth = 4.75 #mm

# The total depth of the baseplate mating surface.
baseplate_mating_depth = 4.4 #mm

# Inset of the XY profile for the non-chamfered part of the mating surface.
# Used for both block and baseplate.
mating_inset = 2.4 #mm

# Chamfer radius for the block mating lip's bottom chamfer.
block_mating_chamfer = 0.8 #mm

## MAG-a-nets
##
## Gridfinity blocks have holes for optional magnets. Weighted baseplates, too.
## The holes are actually counterbores that also support M5 screws.

# Offset from the edge of the grid to the center of each magnet.
magnet_inset = 8 #mm

# The diameter of the magnets 
magnet_diameter = 6.5 #mm

magnet_depth = 2.4 #mm

## Screw boreholes

# Diameter of the counterbore hole for screws.
screw_diameter = 3.5 #mm

# Maximum depth of the screw borehole.
# 
# Gridfinity isn't entirely consistent with the depth of the screw bore; some
# blocks go all the way to the base of the block interior. IDK why lol
screw_depth = 6 #mm

## Utilities
def inset_profile(width, height, inset):
    """Generate a sketch for a rectangle of some size, inset by some amount.
    
    Amount must not exceed twice the Gridfinity fillet radius."""
    return cq.Sketch()\
        .rect(width * grid_unit - inset * 2, height * grid_unit - inset * 2)\
        .vertices()\
        .fillet(fillet_radius - inset)

def gridfinity_block_lip(self, width, height, screw_depth=screw_depth):
    """Extrude Gridfinity block mating lip out of the <Z face.
    
    Face dimensions must match the width and height given here.
    
    Set `screw_depth=None` to allow the block lip's screw holes to go straight
    through."""
    
    #TODO: Can we recover the Gridfinity units from the selected face's dimensions?
    mating_profile = inset_profile(1, 1, mating_inset)
    lip = cq.Workplane("XY")\
        .placeSketch(mating_profile)\
        .extrude(block_mating_depth * -1)\
        .edges("<Z")\
        .chamfer(block_mating_chamfer)
    
    with_lips = self.faces("<Z")\
        .rarray(grid_unit, grid_unit, width, height)\
        .eachpoint(lambda c: lip.val().moved(c), combine="a", clean=True)
    
    filleted = with_lips
    
    for i in range(0, width):
        for j in range(0, height):
            x = (i * grid_unit) - (width * grid_unit / 2) + mating_inset
            y = (j * grid_unit) - (height * grid_unit / 2) + mating_inset
            
            try:
                filleted = filleted\
                    .edges(cq.NearestToPointSelector([x, y, 0]))\
                    .chamfer(mating_inset - block_spacing * 0.5 - 0.01)
            except:
                continue
    
    with_counterbore = filleted.faces("<Z")\
        .workplane()\
        .rarray(grid_unit, grid_unit, width, height)\
        .rect(grid_unit - magnet_inset * 2, grid_unit - magnet_inset * 2)\
        .vertices()\
        .cboreHole(screw_diameter, magnet_diameter, magnet_depth, screw_depth)
    
    return with_counterbore

cq.Workplane.gridfinity_block_lip = gridfinity_block_lip