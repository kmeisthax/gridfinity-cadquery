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
    .fillet(0.5)\
    .translate((gridfinity.grid_unit * 1, 0, 0))

#Test jig for the ruler profile fit
staedtler_test = cq.Workplane("XY")\
    .rect(gridfinity.grid_unit, gridfinity.grid_unit)\
    .extrude(1)\
    .faces(">Z")\
    .placeSketch(staedtler_profile.moved(cq.Location(cq.Vector((3,0,0)))))\
    .cutBlind(-10)\
    .translate((gridfinity.grid_unit * 2.5, 0, 0))

#It's called the "china ruler" because that's the only identifying mark on the
#tool. It's a thin ruler with a big square lip in the middle of the profile for
#what I presume is making it easier to grab.
china_ruler_width = 30 + tolerance #mm

china_ruler_thickness = 2.40 + tolerance #mm

china_ruler_lip_width = 8.74 + tolerance #mm

china_ruler_lip_thickness = 11.75 + tolerance #mm

china_ruler_lip_width_top = 5.5 + tolerance #mm

china_profile = cq.Sketch()\
    .segment((china_ruler_width / -2, 0), (china_ruler_width / 2, 0))\
    .segment((china_ruler_width / 2, china_ruler_thickness))\
    .segment((china_ruler_lip_width / 2, china_ruler_thickness))\
    .segment((china_ruler_lip_width_top / 2, china_ruler_lip_thickness))\
    .segment((china_ruler_lip_width_top / -2, china_ruler_lip_thickness))\
    .segment((china_ruler_lip_width / -2, china_ruler_thickness))\
    .segment((china_ruler_width / -2, china_ruler_thickness))\
    .close()\
    .assemble()\
    .vertices(cq.NearestToPointSelector((china_ruler_width / 2, 0)))\
    .fillet(1)\
    .reset()\
    .vertices(cq.NearestToPointSelector((china_ruler_width / -2, 0)))\
    .fillet(1)\
    .reset()\
    .vertices(cq.NearestToPointSelector((china_ruler_width / 2, china_ruler_thickness)))\
    .fillet(1)\
    .reset()\
    .vertices(cq.NearestToPointSelector((china_ruler_width / -2, china_ruler_thickness)))\
    .fillet(1)\
    .reset()\
    .vertices(cq.NearestToPointSelector((china_ruler_lip_width_top / 2, china_ruler_lip_thickness)))\
    .fillet(0.75)\
    .reset()\
    .vertices(cq.NearestToPointSelector((china_ruler_lip_width_top / -2, china_ruler_lip_thickness)))\
    .fillet(0.75)\
    .reset()\
    .vertices(cq.NearestToPointSelector((china_ruler_lip_width / 2, 0)))\
    .fillet(3)\
    .reset()\
    .vertices(cq.NearestToPointSelector((china_ruler_lip_width_top / -2, china_ruler_thickness)))\
    .fillet(3)\
    .reset()

china_ruler = cq.Workplane("XY")\
    .gridfinity_block(1, 1, 6)\
    .gridfinity_block_stack(1, 1)\
    .gridfinity_block_lip(1, 1)\
    .gridfinity_top_face(6)\
    .workplane()\
    .transformed(offset=(-2, 2, 0), rotate=(0, 0, 45))\
    .placeSketch(china_profile.moved(cq.Location(cq.Vector((0,0,0)))))\
    .cutBlind(gridfinity.block_cut_limit(6) * -1)\
    .transformed(rotate=(0, 0, -45))\
    .transformed(offset=(2, -2, 0))\
    .transformed(offset=(2, -2, 0), rotate=(0, 0, -135))\
    .placeSketch(china_profile.moved(cq.Location(cq.Vector((0,0,0)))))\
    .cutBlind(gridfinity.block_cut_limit(6) * -1)\
    .edges(cq.NearestToPointSelector((5,0,gridfinity.block_top_surface(6))))\
    .fillet(1.5)\
    .edges(cq.NearestToPointSelector((-5,0,gridfinity.block_top_surface(6))))\
    .fillet(1.5)\
    .edges(cq.NearestToPointSelector((5,0,gridfinity.block_top_surface(6) - gridfinity.block_cut_limit(6))))\
    .fillet(0.5)\
    .edges(cq.NearestToPointSelector((-5,0,gridfinity.block_top_surface(6) - gridfinity.block_cut_limit(6))))\
    .fillet(0.5)\
    .translate((gridfinity.grid_unit * -1, 0, 0))

#Test jig for the china ruler profile fit
china_test = cq.Workplane("XY")\
    .rect(china_ruler_width + 5, china_ruler_lip_thickness + 5)\
    .extrude(1)\
    .faces(">Z")\
    .placeSketch(china_profile
        .moved(cq.Location(cq.Vector((0, -china_ruler_lip_thickness / 2,0))))
    )\
    .cutBlind(-10)\
    .translate((gridfinity.grid_unit * -2.5, 0, 0))