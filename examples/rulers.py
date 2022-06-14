import cadquery as cq
import gridfinity
from math import pi, cos, sin

def rotate_sketch_point(point, angle):
    angle = angle * pi / 180

    return (point[0] * cos(angle) + point[1] * sin(angle),
            -point[0] * sin(angle) + point[1] * cos(angle))

#Extra spacing so we don't grip the ruler firmly.
tolerance = 1#mm

#Staedtler rulers are basically an extruded triangle, so we just draw and cut that.
staedtler_profile_height = 22.00 + tolerance #mm
staedtler_profile_base_width = 24.77 + tolerance #mm

staedtler_inset = 2.5

origin_x = (staedtler_profile_base_width / 2) * sin(30 * pi / 180) / sin(60 * pi / 180)

points = ((origin_x + 0.5, staedtler_profile_base_width / -2),
          (origin_x - staedtler_inset, 0),
          (origin_x + 0.5, staedtler_profile_base_width / 2))

staedtler_profile = cq.Sketch()\
    .segment(points[0], points[1])\
    .segment(points[2])\
    .segment(rotate_sketch_point(points[0], 240))\
    .segment(rotate_sketch_point(points[1], 240))\
    .segment(rotate_sketch_point(points[2], 240))\
    .segment(rotate_sketch_point(points[0], 120))\
    .segment(rotate_sketch_point(points[1], 120))\
    .segment(rotate_sketch_point(points[2], 120))\
    .close()\
    .assemble()\
    .vertices(cq.NearestToPointSelector((-5,-5,0)))\
    .each(lambda c: cq.Sketch().circle(2.5).moved(cq.Location(cq.Vector((c.toTuple()[0][0] * 1.2, c.toTuple()[0][1] * 1.2, c.toTuple()[0][2] * 1.2)))), mode='s')\
    .reset()\
    .vertices(cq.NearestToPointSelector((10,0,0)))\
    .each(lambda c: cq.Sketch().circle(2.5).moved(cq.Location(cq.Vector((c.toTuple()[0][0] * 1.2, c.toTuple()[0][1] * 1.2, c.toTuple()[0][2] * 1.2)))), mode='s')\
    .reset()\
    .vertices(cq.NearestToPointSelector((0,5,0)))\
    .each(lambda c: cq.Sketch().circle(2.5).moved(cq.Location(cq.Vector((c.toTuple()[0][0] * 1.2, c.toTuple()[0][1] * 1.2, c.toTuple()[0][2] * 1.2)))), mode='s')\

staedtler_ruler = cq.Workplane("XY")\
    .gridfinity_block(1, 1, 6)\
    .gridfinity_block_stack(1, 1)\
    .gridfinity_block_lip(1, 1)\
    .gridfinity_top_face(6)\
    .workplane()\
    .placeSketch(staedtler_profile.moved(cq.Location(cq.Vector((3,0,0)))))\
    .cutBlind(gridfinity.block_cut_limit(6) * -1)\
    .wires(cq.NearestToPointSelector((staedtler_profile_height / 6, 0, gridfinity.block_top_surface(6))))\
    .fillet(1.5)\
    .wires(cq.NearestToPointSelector((staedtler_profile_height / 6, 0, gridfinity.block_top_surface(6) - gridfinity.block_cut_limit(6))))\
    .fillet(0.5)

#Test jig for the ruler profile fit
staedtler_test = cq.Workplane("XY")\
    .rect(gridfinity.grid_unit, gridfinity.grid_unit)\
    .extrude(1)\
    .faces(">Z")\
    .placeSketch(staedtler_profile.moved(cq.Location(cq.Vector((3,0,0)))))\
    .cutBlind(-10)