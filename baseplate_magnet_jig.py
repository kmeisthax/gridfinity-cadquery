import cadquery as cq
import gridfinity

jig_separator_pin_radius = 13

jig_handle = cq.Workplane("XY")\
    .rect(12, 1.5)\
    .extrude(2)\
    .faces(">Z")\
    .rect(12, 4)\
    .extrude(1)

jig_carrier = cq.Workplane("XY")\
    .placeSketch(gridfinity.inset_profile(1, 1, gridfinity.block_spacing / 2))\
    .extrude(gridfinity.magnet_depth + 0.5)\
    .faces("<Z")\
    .chamfer(gridfinity.block_mating_inset - gridfinity.block_spacing * 0.5)\
    .faces(">Z")\
    .rect(gridfinity.grid_unit - gridfinity.magnet_inset * 2, gridfinity.grid_unit - gridfinity.magnet_inset * 2, forConstruction=True)\
    .vertices()\
    .hole(gridfinity.magnet_diameter, gridfinity.magnet_depth)\
    .faces(">Z")\
    .hole(20, gridfinity.magnet_depth + 0.5)\
    .union(jig_handle.val().moved(cq.Location(cq.Vector([0, 13, gridfinity.magnet_depth + 0.5]))))\
    .union(jig_handle.val().moved(cq.Location(cq.Vector([0, -13, gridfinity.magnet_depth + 0.5]))))\
    .faces(">Z")\
    .polarArray(jig_separator_pin_radius, 0, 360, 4)\
    .cutEach(lambda c: cq.Solid.makeCylinder(2.25, 2.5, cq.Vector(), cq.Vector(0, 0, 1)).moved(c), True, clean=True)

jig_separator = cq.Workplane("XY")\
    .placeSketch(gridfinity.inset_profile(1, 1, gridfinity.block_mating_inset))\
    .extrude(-1.25)\
    .faces(">Z")\
    .polarArray(jig_separator_pin_radius, 0, 360, 4)\
    .eachpoint(lambda c: cq.Solid.makeCylinder(1, 1.75, cq.Vector(), cq.Vector(0, 0, 1)).moved(c), combine="a", clean=True)\
    .faces(">Z")\
    .cylinder(1, 1.5, cq.Vector(0,0,1))\
    .faces("<Z")\
    .chamfer(0.75)\
    .faces("<Z")\
    .wires().toPending()\
    .extrude(-.25)\
    .faces("<Z")\
    .rect(gridfinity.grid_unit - gridfinity.magnet_inset - 1, gridfinity.grid_unit - gridfinity.magnet_inset -1)\
    .cutBlind(.25)\

del jig_handle