import cadquery as cq
import gridfinity
from math import pow, e

# Ender 3 ships with an Allen Key set with the following across-flat key sizes:
# 4mm, 3mm, 2.5mm, 2mm, and 1.5mm
ender_set = [4, 3, 2.5, 2, 1.5]
tolerance = 0.25

def allen_key_profile(across_flat_dia):
    return cq.Workplane("XY")\
        .polygon(6, across_flat_dia)\
        .extrude(100)\
        .val()

def allen_key_cutout_generator(points, depth, distance):
    i = 0

    def inner(p):
        nonlocal i

        key_dia = points[i % len(points)]

        p = list(p.toTuple()[0])
        phi = ((i % len(points))) / len(points)
        p[0] = (p[0] / pow(e, phi) - distance / 10) / 1.5
        p[1] = (p[1] / pow(e, phi) - distance / 10) / 1.5
        
        i += 1

        return allen_key_profile(key_dia + tolerance)\
            .translate(tuple(p))\
            .translate((0, 0, -gridfinity.block_cut_limit(depth)))

    return inner

def allen_key_label_generator(points):
    i = 0

    def inner(p):
        nonlocal i

        key_dia = points[i % len(points)]

        p = list(p.toTuple()[0])
        i += 1

        return cq.Workplane("XY")\
            .text(str(key_dia), 5, 2.0, font="Ubuntu", combine="a")\
            .val()\
            .translate((p[0], p[1], p[2] - 2))

    return inner

def allen_key_holder(widths, depth):
    widths.sort(reverse = True)
    distance = widths[0] + 5 * len(widths)

    return cq.Workplane("XY")\
        .gridfinity_block(1, 1, depth)\
        .gridfinity_block_stack(1, 1)\
        .gridfinity_block_lip(1, 1)\
        .faces(cq.NearestToPointSelector((0, 0, gridfinity.block_top_surface(depth))))\
        .workplane()\
        .polygon(len(widths), distance, forConstruction=True)\
        .vertices()\
        .cutEach(allen_key_cutout_generator(widths, depth, distance))\
        .faces(cq.NearestToPointSelector((0, 0, gridfinity.block_top_surface(depth))))\
        .wires(cq.selectors.InverseSelector(cq.NearestToPointSelector((0, 0, 0))))\
        .fillet(0.5)\
        .faces(cq.NearestToPointSelector((0, 0, gridfinity.block_top_surface(depth))))\
        .workplane()\
        .polygon(len(widths), distance, forConstruction=True)\
        .vertices()\
        .eachpoint(allen_key_label_generator(widths), combine="cut")

ender_key_holder = allen_key_holder(ender_set, 3)
