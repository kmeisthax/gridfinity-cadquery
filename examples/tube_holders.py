import cadquery as cq
import gridfinity, math

FUDGE_FACTOR = 0.25

def cut_at(tube, block, point):
    return block\
            .cut(tube.translate(point))\
            .edges(
                cq.NearestToPointSelector((point[0], point[1], gridfinity.block_top_surface(1)))
            )\
            .fillet(2)\
            .edges(
                cq.NearestToPointSelector((point[0], point[1], gridfinity.block_top_surface(3)))
            )\
            .fillet(1)

def tube_holder(dia):
    size = 1
    if dia > 35:
        size = 2
    
    if dia > 77:
        size = 3
    
    size_mm = size * gridfinity.grid_unit

    tube = cq.Workplane("XY")\
        .circle((dia + FUDGE_FACTOR) / 2)\
        .extrude(100)\
        .translate((0,0,gridfinity.block_top_surface(1)))
    
    block = cq.Workplane("XY")\
        .gridfinity_block(size,size,3)\
        .gridfinity_block_stack(size,size)\
        .gridfinity_block_lip(size,size)
    
    if dia <= 12:
        quincunx_dist = size_mm / 4

        block = cut_at(tube, block, (0, 0, 0))
        block = cut_at(tube, block, (quincunx_dist, quincunx_dist, 0))
        block = cut_at(tube, block, (-quincunx_dist, -quincunx_dist, 0))
        block = cut_at(tube, block, (-quincunx_dist, quincunx_dist, 0))
        block = cut_at(tube, block, (quincunx_dist, -quincunx_dist, 0))
    elif (size_mm - gridfinity.block_mating_inset) > dia * 2:
        quincunx_dist = size_mm / 5.5

        block = cut_at(tube, block, (quincunx_dist, quincunx_dist, 0))
        block = cut_at(tube, block, (-quincunx_dist, -quincunx_dist, 0))
    else:
        block = block\
            .cut(tube)\
            .edges(
                cq.NearestToPointSelector((0, 0, gridfinity.block_top_surface(1)))
            )\
            .fillet(2)\
            .edges(
                cq.NearestToPointSelector((0, 0, gridfinity.block_top_surface(3)))
            )\
            .fillet(1)
    
    return block

for i in range(5, 78):
    interval = 1.5
    index = i - 5
    y = 0
    xstride = 8

    if i > 35:
        interval = 2
        index = i - 36
        y = gridfinity.grid_unit * 6
        xstride = 6
    
    locals()[str(i) + "mm Tube Holder"] = tube_holder(i)\
        .translate((index % xstride * gridfinity.grid_unit * interval,
                    y + math.floor(index / xstride) * gridfinity.grid_unit * interval,
                    0))