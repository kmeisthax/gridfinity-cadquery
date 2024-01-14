"""Holder for the 'other feet' that came with my Brother CS7000X

The 'other feet' include:

 * Buttonhole foot
 * Quilting foot
 * Two random pieces of metal that probably also do quilting things"""

import cadquery as cq
import gridfinity

FUDGE_FACTOR = 0.5

BUTTONHOLE_WIDTH = 20.30 + FUDGE_FACTOR
BUTTONHOLE_DEPTH = 5.06
BUTTONHOLE_HEIGHT = 100.70

# The buttonhole foot has a protrusion on the front for a 'gimp thread' to be
# threaded through. This is intended for stretchy fabrics.
BUTTONHOLE_GIMP_HEIGHT = 3.74
BUTTONHOLE_GIMP_WIDTH = 6.62 + FUDGE_FACTOR
BUTTONHOLE_GIMP_DEPTH = 2.37

BUTTONHOLE_GIMP_OFFSET_Y = 1

BUTTONHOLE_SPRING_WIDTH = 10.65 + FUDGE_FACTOR
BUTTONHOLE_SPRING_HEIGHT = 12.06
BUTTONHOLE_SPRING_DEPTH = 6.95

BUTTONHOLE_SPRING_OFFSET_Z = 4

buttonhole_foot = cq.Workplane("XY")\
    .rect(BUTTONHOLE_WIDTH, BUTTONHOLE_DEPTH)\
    .extrude(BUTTONHOLE_HEIGHT)\
    .edges("<Z")\
    .edges("|Y")\
    .fillet(BUTTONHOLE_WIDTH / 3.5)\
    .faces("<Z")\
    .workplane(origin=(0, BUTTONHOLE_DEPTH / 2 - BUTTONHOLE_GIMP_DEPTH / 2 - BUTTONHOLE_GIMP_OFFSET_Y, 0))\
    .sketch()\
    .rect(BUTTONHOLE_GIMP_WIDTH,BUTTONHOLE_GIMP_DEPTH)\
    .finalize()\
    .extrude(BUTTONHOLE_GIMP_HEIGHT)\
    .faces("<Y")\
    .workplane(origin=(0,0, BUTTONHOLE_SPRING_WIDTH / 2 + BUTTONHOLE_SPRING_OFFSET_Z))\
    .sketch()\
    .rect(BUTTONHOLE_SPRING_WIDTH, BUTTONHOLE_SPRING_HEIGHT)\
    .vertices()\
    .fillet(1.5)\
    .finalize()\
    .extrude(BUTTONHOLE_SPRING_DEPTH - BUTTONHOLE_DEPTH)\
    .translate((0,0,BUTTONHOLE_GIMP_HEIGHT))

QUILTING_HOOK_ROD_DIAMETER = 1.25 #2.5mm / 2

quilting_hook_rod = cq.Workplane("XY")\
    .circle(QUILTING_HOOK_ROD_DIAMETER)\
    .extrude(100)\
    .edges("<Z")\
    .chamfer(3, .75)

etc_holder = cq.Workplane("XY")\
    .gridfinity_block(2, 1, 3)\
    .gridfinity_block_stack(2, 1)\
    .gridfinity_block_lip(2, 1)

#I have no idea what this metal slab does, but it was in the accessory pack for
#the CS7000X, sooooo
METAL_SLAB_WIDTH = 16 + FUDGE_FACTOR #15.95mm
METAL_SLAB_DEPTH = 2.5 #2.02mm

metal_slab = cq.Workplane("XY")\
    .rect(METAL_SLAB_WIDTH, METAL_SLAB_DEPTH)\
    .extrude(50)\
    .edges("<Z")\
    .edges("|Y")\
    .chamfer(1, METAL_SLAB_WIDTH / 2.5)\
    .edges("<Z")\
    .edges("|Y")\
    .fillet(16)\
    .edges("|Y")\
    .fillet(2)

#The quilting foot is... very irregularly shaped.
#There's several plastic and metal parts which I'm just going to identify
#by color. Our goal is to construct a profile for a holder slot, not a 1:1
#clone of the shape, so this isn't super accurate.
QUILTING_FOOT_WIDTH = 24.67
QUILTING_FOOT_HEIGHT = 27.83
QUILTING_FOOT_WHITE_WIDTH = 19.90
QUILTING_FOOT_WHITE_HEIGHT = 14.55

QUILTING_FOOT_HOOK_PART_WIDTH = 15.82

quilting_foot = cq.Workplane("XY")\
    .placeSketch(
        cq.Sketch()\
            .segment((0, 0), (0, QUILTING_FOOT_HEIGHT))\
            .segment((QUILTING_FOOT_WIDTH, QUILTING_FOOT_HEIGHT))\
            .segment((QUILTING_FOOT_WIDTH, QUILTING_FOOT_WHITE_HEIGHT))\
            .segment((QUILTING_FOOT_WHITE_WIDTH, QUILTING_FOOT_WHITE_HEIGHT))\
            .segment((QUILTING_FOOT_WHITE_WIDTH, 0))\
            .close()\
            .assemble()
    )\
    .extrude(50)\
    .edges("|Z")\
    .edges("<X")\
    .edges(">Y")\
    .chamfer(QUILTING_FOOT_WIDTH - QUILTING_FOOT_HOOK_PART_WIDTH)\
    .edges("|Z")\
    .edges(">Y")\
    .fillet(4)\
    .edges("|Z")\
    .edges(">X")\
    .fillet(4)

etc_holder = etc_holder.cut(
    buttonhole_foot.translate((4.5,11,gridfinity.block_top_surface(1)))
).cut(
    quilting_hook_rod.translate((34,-13,gridfinity.block_top_surface(1)))
).cut(
    metal_slab.translate((27,12.25,gridfinity.block_top_surface(1)))
).cut(
    quilting_foot.rotate((0,0,0), (0,0,1), 180)\
        .translate((-10, 13.5, gridfinity.block_top_surface(1)))
)

#IT'S FILLETING TIME!
#I swear, fillets are the most painful thing you can do in CQ
etc_holder = etc_holder.edges(
    cq.NearestToPointSelector((4.5 + 5, 11, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((4.5 + 7, 11, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((4.5 + 9, 11, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((4.5 - 5, 11, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((4.5 - 9, 11, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((4.5, 11 - 3, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((4.5, 11 + 3, gridfinity.block_top_surface(3)))
).fillet(1)

etc_holder = etc_holder.edges(
    cq.NearestToPointSelector((34, -13, gridfinity.block_top_surface(3)))
).fillet(1)

etc_holder = etc_holder.edges(
    cq.NearestToPointSelector((27, 12.25 + 2, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((27, 12.25 - 2, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((27 + 8.5, 12.25, gridfinity.block_top_surface(3)))
).fillet(.99).edges(
    cq.NearestToPointSelector((27 - 8.5, 12.25, gridfinity.block_top_surface(3)))
).fillet(.99)

# The quilting foot fillets are doubly annoying because we don't even have
# plausible coords for the top edges.
etc_holder = etc_holder.edges(
    cq.NearestToPointSelector((-10, 0, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((-20, 0, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((-20, 10, gridfinity.block_top_surface(3)))
).fillet(1).edges(
    cq.NearestToPointSelector((-25, 10, gridfinity.block_top_surface(3)))
).fillet(.99) #For some reason, this fillet breaks.

etc_holder = etc_holder.edges(
    cq.NearestToPointSelector((-10, 0, gridfinity.block_top_surface(1)))
).fillet(2).edges(
    cq.NearestToPointSelector((-25, -5, gridfinity.block_top_surface(1)))
).fillet(2).edges(
    cq.NearestToPointSelector((-19, 15, gridfinity.block_top_surface(1)))
).fillet(2)

del buttonhole_foot
del quilting_hook_rod
del metal_slab
del quilting_foot