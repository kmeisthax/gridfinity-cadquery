import cadquery as cq
import gridfinity

G_FOOT_WIDTH = 15.81
R_FOOT_WIDTH = 15.95
X_FOOT_WIDTH = 16.90
I_FOOT_WIDTH = 17.48
M_FOOT_WIDTH = 17.66
N_FOOT_WIDTH = 19.60

# Measured on the "R" foot, which is the thickest.
# Rounded up for 3D printing tolerance.
# Other feet are closer to 8mm.
FOOT_THICKNESS = 11 #10.15

# R foot has a piece of metal that sticks beyond the profile of the foot,
# so we have to make a cutout for it.
R_FOOT_FIN_CUTOUT_X = 8.11
R_FOOT_FIN_CUTOUT_WIDTH = 2.5

G_FOOT_FIN_CUTOUT_WIDTH = 6.2 #5.86

sewing_foot_block = cq.Workplane("XY")\
    .gridfinity_block(2, 1, 3)\
    .gridfinity_block_stack(2, 1)\
    .gridfinity_block_lip(2, 1)

SPACING_X = 8
SPACING_Y = 6

SLOT_FILLET = 1

for i in range(0, 3):
    for j in range(0, 2):
        if i == 0 and j == 1:
            FOOT_WIDTH = N_FOOT_WIDTH + 0.5
        elif i == 2:
            FOOT_WIDTH = R_FOOT_WIDTH + 0.5
        else:
            FOOT_WIDTH = M_FOOT_WIDTH + 0.5
        
        z_coord = 3 * j
        
        sewing_foot = cq.Workplane("XY")\
            .rect(FOOT_WIDTH, FOOT_THICKNESS)\
            .extrude(FOOT_WIDTH * 2)\
            .translate([0, 0, 2])
        
        x_coord = (M_FOOT_WIDTH + SPACING_X) * (i - 1)
        y_coord = (FOOT_THICKNESS + SPACING_Y) * (j - 0.5)

        if i == 0 and j == 1: #N foot compartment
            x_coord -= (M_FOOT_WIDTH - FOOT_WIDTH) / 2
        
        sewing_foot_block = sewing_foot_block.cut(
            sewing_foot.translate(
                [x_coord,
                y_coord,
                z_coord]
            )
        ).edges(
            cq.NearestToPointSelector((x_coord + 8,
                                    y_coord,
                                    gridfinity.block_top_surface(3)))
        ).fillet(SLOT_FILLET)\
        .edges(
            cq.NearestToPointSelector((x_coord - 8,
                                    y_coord,
                                    gridfinity.block_top_surface(3)))
        ).fillet(SLOT_FILLET)\
        .edges(
            cq.NearestToPointSelector((x_coord,
                                    y_coord + 4,
                                    gridfinity.block_top_surface(3)))
        ).fillet(SLOT_FILLET)\
        .edges(
            cq.NearestToPointSelector((x_coord,
                                    y_coord - 4,
                                    gridfinity.block_top_surface(3)))
        ).fillet(SLOT_FILLET)\
        .edges(
            cq.NearestToPointSelector((x_coord,
                                    y_coord + 0.5,
                                    3 * j))
        ).fillet(FOOT_THICKNESS - SLOT_FILLET)

        if i == 2 and j == 0:
            #The R foot's metal fin is near enough to the center that
            #I don't feel like doing the parametric math to properly
            #offset it.
            cutout_block = cq.Workplane("XY")\
                .rect(R_FOOT_FIN_CUTOUT_WIDTH, FOOT_THICKNESS + 2.5)\
                .extrude(FOOT_WIDTH * 2)\
                .translate([x_coord, y_coord - 1.25, 0])
            
            sewing_foot_block = sewing_foot_block.cut(cutout_block)\
                .edges(
                    cq.NearestToPointSelector((x_coord + 1, y_coord - 6, gridfinity.block_top_surface(3)))                    
                )\
                .fillet(SLOT_FILLET)\
                .edges(
                    cq.NearestToPointSelector((x_coord - 1, y_coord - 6, gridfinity.block_top_surface(3)))                    
                )\
                .fillet(SLOT_FILLET)\
                .edges(
                    cq.NearestToPointSelector((x_coord, y_coord - 7, gridfinity.block_top_surface(3)))                    
                )\
                .fillet(SLOT_FILLET)
        
        if i == 2 and j == 1:
            #The G foot is only half-curved at the front.
            cutout_block = cq.Workplane("XY")\
                .rect(G_FOOT_FIN_CUTOUT_WIDTH, FOOT_THICKNESS)\
                .extrude(FOOT_WIDTH * 2)\
                .translate([x_coord + FOOT_WIDTH / 2 - G_FOOT_FIN_CUTOUT_WIDTH / 2, y_coord, 1.75])
            
            sewing_foot_block = sewing_foot_block.cut(cutout_block)

del cutout_block
del sewing_foot