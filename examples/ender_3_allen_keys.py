import cadquery as cq
import gridfinity
from math import pow, e, cos, pi, sin, floor

tolerance = 0.25

# Radius of the fillets on the allen key holes.
# NOTE: If you get command not done errors, those almost always are the result
# of a chamfer or fillet operation failing because the geometry makes no sense
# to CADQuery. There's actually three ways I've seen fillets fail:
# 
# 1. The fillet radius is high enough to join two holes together
# 2. The logistic spiral code is putting holes on top of one another
# 3. The allen key holes are so far from the center they are cutting into the
#    Gridfinity stacking lip, which confuses everything
# 
# When in doubt set this to the lowest nonzero value you can make it handle
# or delete all the fillet calls that use this.
fillet_radius = 0.75

def allen_key_profile(across_flat_dia):
    """Generate the profile of an allen key wrench with a given across-flats
    diameter."""

    return cq.Workplane("XY")\
        .polygon(6, across_flat_dia / cos(360 / 6 / 2 * pi / 180) + tolerance)\
        .extrude(100)\
        .val()

def optimal_point_distance(physical_widths):
    """Calculate the optimal distance between points on a polygon with as many
    points/sides as there are allen keys to accomodate."""
    return physical_widths[0] + 5.5 * len(physical_widths)

def allen_key_cutout_generator(points, depth, distance):
    """Create an allen key cutout generator function for use with cuteach.
    
    Each generator should only be used once as there is internal closure state
    that may not reset properly if reused."""
    i = 0

    def inner(p):
        nonlocal i

        key_dia = points[i % len(points)]

        old_p = list(p.toTuple()[0])
        phi = ((i % len(points))) / len(points)

        beta = 25 * pi / 180 #Increasing this constant ROTATES all the labels CLOCKWISE in DEGREES

        p = [
            cos(beta) * old_p[0] - sin(beta) * old_p[1],
            sin(beta) * old_p[0] + cos(beta) * old_p[1],
            old_p[2]
        ]

        # Ok, here's how the logarithmic spiral logic works:
        # The distance parameter is divided by a constant; that determines how
        # far to pull the point into the spiral.
        # 
        # The second division scales all the points by a constant.
        p[0] = (p[0] / pow(e, phi) - distance / 15) / 1.5
        p[1] = (p[1] / pow(e, phi) - distance / 15) / 1.5
        
        i += 1

        return allen_key_profile(key_dia)\
            .translate(tuple(p))\
            .translate((0, 0, -gridfinity.block_cut_limit(depth)))

    return inner

def decimal_to_binary_fraction(val):
    """Convert a decimal value into a binary fraction.

    Fractions are returned as a 3-tuple of (whole, numerator, denominator).
    
    This works by trial division; we try every power of two up to 256 and
    accept the lowest value with no remainder. If there is no fractional
    representation of the value, we return the original value."""

    whole = floor(val)
    frac = val - whole
    denominator = 2
    while denominator < 512:
        numerator = frac * denominator

        if abs(numerator - floor(numerator)) < 0.0001:
            return (whole, floor(numerator), floor(denominator))
        
        denominator *= 2
    
    return val

def frac_text(self, whole_txt, numerator_txt, denominator_txt, fontsize,
        distance, cut=True, combine=False, clean=True, font="Arial",
        fontPath=None, kind='regular', halign='center', valign='center'):
    """Generate a solid for a fractional quantity with a whole part, numerator,
    and denominator."""
    
    if whole_txt.strip() != "":
        whole = cq.Compound.makeText(whole_txt, fontsize, distance, font=font,
            fontPath=fontPath, kind=kind, halign='left', valign='top',
            position=self.plane)

        #TODO: the space width is a guess because Compound.makeText trims strings
        whole_width = whole.BoundingBox().xlen + fontsize / 6
    else:
        whole = cq.Compound.makeCompound([])
        whole_width = 0
    
    numerator = cq.Compound.makeText(numerator_txt, fontsize / 2, distance,
        font=font, fontPath=fontPath, kind=kind, halign='left', valign='top',
        position=self.plane)
    
    numerator_bb = numerator.BoundingBox()
    numerator_width = numerator_bb.xmin * 2 + numerator_bb.xlen
    #TODO: Check self.plane to see if the coordinates get reversed or not like
    #in here
    numerator_height = abs(numerator_bb.ymax - numerator_bb.ylen)
    
    denominator = cq.Compound.makeText(denominator_txt, fontsize / 2, distance,
        font=font, fontPath=fontPath, kind=kind, halign='left', valign='top',
        position=self.plane)
    
    denominator_bb = denominator.BoundingBox()
    denominator_width = denominator_bb.xmin * 2 + denominator_bb.xlen

    fraction_width = max(numerator_width, denominator_width)

    numerator_offset = (fraction_width - numerator_width) / 2
    denominator_offset = (fraction_width - denominator_width) / 2

    #TODO: Figure out how to use the - or emdash from a font without having
    #really weird positioning issues.
    bar_height = fontsize / 16
    bar_spacing = fontsize / 32
    bar_y = numerator_height
    bar = cq.Workplane(self.plane)\
        .moveTo(0, -bar_y + bar_height / 2)\
        .lineTo(fraction_width, -bar_y + bar_height / 2)\
        .lineTo(fraction_width, -bar_y - bar_height / 2)\
        .lineTo(0, -bar_y - bar_height / 2)\
        .close()\
        .extrude(distance)\
        .val()
    
    numerator_y = bar_height / 2 + bar_spacing
    denominator_y = -numerator_height - bar_height / 2 - bar_spacing
    
    together = whole\
        .fuse(bar.move(cq.Location(cq.Vector(whole_width, 0, 0))))\
        .fuse(numerator.move(cq.Location(cq.Vector(whole_width + numerator_offset, numerator_y, 0))))\
        .fuse(denominator.move(cq.Location(cq.Vector(whole_width + denominator_offset, denominator_y, 0))))\
        .move(cq.Location(cq.Vector(0, -numerator_y, 0)))
    
    #TODO: Again, check the workplane for coordinate reversals at some point
    together_bb = together.BoundingBox()
    together_x = 0
    together_y = 0

    if halign == 'center':
        together_x = (together_bb.xmin + together_bb.xlen) / 2
    elif halign == 'right':
        together_x = together_bb.xmin + together_bb.xlen
    
    if valign == 'center':
        together_y = abs(together_bb.ymax + together_bb.ylen) / 2
    elif valign == 'right':
        together_y = abs(together_bb.ymax + together_bb.ylen)
    
    together = together.move(cq.Location(cq.Vector(-together_x, together_y, 0)))
    
    if cut:
        combine = 'cut'
    
    return self._combineWithBase(together, combine, clean)

cq.Workplane.frac_text = frac_text

def allen_key_label_generator(points, distance, square_block_size, imperial = False):
    """Create an allen key label generator function for use with eachpoint.
    
    Each generator should only be used once as there is internal closure state
    that may not reset properly if reused."""

    i = 0

    def inner(p):
        nonlocal i

        key_dia = points[i % len(points)]

        if imperial:
            label_dia = decimal_to_binary_fraction(key_dia)
        else:
            label_dia = key_dia

        label_base_scale = 0.91 #Increasing this constant pulls numbers at the start of the spiral IN
        label_falloff = 0.07 / (len(points) / 5) #Increasing this constant pulls numbers towards the center of the spiral OUT
        beta = 65 * pi / 180 #Increasing this constant ROTATES all the labels CLOCKWISE in DEGREES

        #We have a separate spiral scale for big blocks
        if square_block_size > 1:
            label_base_scale = 0.95 + max(0, 0.045 * (len(points) - 12))

            #Increasing this constant pulls numbers towards the center of the spiral OUT
            label_falloff = 0.01

            #We rotate the big blocks differently because the rotation causes problems with the Ender set
            beta = 25 * pi / 180 #Increasing this constant ROTATES all the labels CLOCKWISE in DEGREES

        # Works like the above, except we have an extra scaling term because
        # the spiral is too strong
        old_p = list(p.toTuple()[0])
        phi = ((i % len(points))) / len(points)

        p = [
            cos(beta) * old_p[0] - sin(beta) * old_p[1],
            sin(beta) * old_p[0] + cos(beta) * old_p[1],
            old_p[2]
        ]

        p[0] = (p[0] / pow(e, phi) - distance / 15) / (label_base_scale - (label_falloff * i))
        p[1] = (p[1] / pow(e, phi) - distance / 15) / (label_base_scale - (label_falloff * i))

        i += 1

        if type(label_dia) is tuple:
            whole = label_dia[0]
            if whole == 0:
                whole = ""
            else:
                whole = str(whole)

            nom = str(label_dia[1])
            denom = str(label_dia[2])
            
            return cq.Workplane("XY")\
                .frac_text(whole, nom, denom, 10, 2.0, font="Ubuntu", combine="a", halign='left')\
                .val()\
                .translate((p[0], p[1], p[2]))
        else:
            return cq.Workplane("XY")\
                .text(str(label_dia), 6 - 0.2 * (len(str(label_dia)) - 1), 2.0, font="Ubuntu", combine="a", halign='left')\
                .val()\
                .translate((p[0], p[1], p[2]))

    return inner

def allen_key_holder(widths, square_block_size, depth, imperial = False):
    """Generate a holder for allen keys that can hold one of each listed width
    and is a given number of Gridfinity units big and deep.
    
    The imperial flag does two things:
    
     * It converts inches to millimeters
     * It prints nice-looking binary fractions for the labels"""

    physical_widths = widths
    if imperial:
        widths.sort(reverse = True)
        physical_widths = [width * 25.4 for width in widths]
    else:
        widths.sort(reverse = True)
        physical_widths = widths
    
    distance = optimal_point_distance(physical_widths)

    return cq.Workplane("XY")\
        .gridfinity_block(square_block_size, square_block_size, depth)\
        .gridfinity_block_stack(square_block_size, square_block_size)\
        .gridfinity_block_lip(square_block_size, square_block_size)\
        .faces(cq.NearestToPointSelector((0, 0, gridfinity.block_top_surface(depth))))\
        .workplane()\
        .polygon(len(physical_widths), distance, forConstruction=True)\
        .vertices()\
        .cutEach(allen_key_cutout_generator(physical_widths, depth, distance))\
        .faces(cq.NearestToPointSelector((0, 0, gridfinity.block_top_surface(depth))))\
        .wires(cq.selectors.InverseSelector(cq.NearestToPointSelector((0, 0, 0))))\
        .fillet(fillet_radius)\
        .faces(cq.NearestToPointSelector((0, 0, gridfinity.block_top_surface(depth))))\
        .workplane()\
        .polygon(len(widths), distance, forConstruction=True)\
        .vertices()\
        .eachpoint(allen_key_label_generator(widths, distance, square_block_size, imperial=imperial), combine="a")

# Ender 3 ships with an Allen Key set with the following across-flat key sizes:
# 4mm, 3mm, 2.5mm, 2mm, and 1.5mm
# The other sets are all various tool sets I found on Amazon; pick one that
# best matches your current set of keys or add one to the list.
Ender3Set = allen_key_holder([4, 3, 2.5, 2, 1.5], 1, 3)
AmazonBasicsMetric = allen_key_holder([10, 8, 6, 5.5, 5, 4.5, 4, 3.5, 3, 2.5, 2, 1.5, 1.27], 2, 3)
AmazonBasicsImperial = allen_key_holder([3/8, 5/16, 1/4, 7/32, 3/16, 5/32, 9/64, 1/8, 7/64, 3/32, 5/64, 1/16, 0.05], 2, 3, imperial=True)
EPAutoMetric = allen_key_holder([10, 8, 7, 6, 5.5, 5, 4.5, 4, 3, 2.5, 2, 1.5, 1.3, 0.9, 0.7], 2, 3)
EPAutoImperial = allen_key_holder([3/8, 5/16, 1/4, 7/32, 3/16, 5/32, 9/64, 1/8, 7/64, 3/32, 5/64, 1/16, 0.05, 0.035, 0.028], 2, 3, imperial=True)
CraftsmanMetric = allen_key_holder([10, 8, 7, 6, 5, 4, 3, 2.5, 2, 1.5], 2, 3)
CraftsmanImperial = allen_key_holder([3/8, 5/16, 1/4, 7/32, 3/16, 5/32, 1/8, 3/32, 5/64, 1/16], 2, 3, imperial=True)
LichampMetric = allen_key_holder([10, 8, 6, 5, 4, 3, 2.5, 2, 1.5], 2, 3)
LichampImperial = allen_key_holder([3/8, 5/16, 1/4, 3/16, 5/32, 1/8, 3/32, 5/64, 1/16], 2, 3, imperial=True)

asm = cq.Assembly()\
    .add(Ender3Set, name="Ender3Set")\
    .add(AmazonBasicsMetric, name="AmazonBasicsMetric")\
    .add(AmazonBasicsImperial, name="AmazonBasicsImperial")\
    .add(EPAutoMetric, name="EPAutoMetric")\
    .add(EPAutoImperial, name="EPAutoImperial")\
    .add(CraftsmanMetric, name="CraftsmanMetric")\
    .add(CraftsmanImperial, name="CraftsmanImperial")\
    .add(LichampMetric, name="LichampMetric")\
    .add(LichampImperial, name="LichampImperial")\
    .constrain("Ender3Set@faces@<Z", "FixedPoint", (0, 0, 0))\
    .constrain("Ender3Set@faces@<Z", "FixedRotation", (0, 0, 0))\
    .constrain("AmazonBasicsMetric@faces@<Z", "FixedPoint", (gridfinity.grid_unit * 3, 0, 0))\
    .constrain("AmazonBasicsMetric@faces@<Z", "FixedRotation", (0, 0, 0))\
    .constrain("AmazonBasicsImperial@faces@<Z", "FixedPoint", (gridfinity.grid_unit * -3, 0, 0))\
    .constrain("AmazonBasicsImperial@faces@<Z", "FixedRotation", (0, 0, 0))\
    .constrain("EPAutoMetric@faces@<Z", "FixedPoint", (0, gridfinity.grid_unit * 3, 0))\
    .constrain("EPAutoMetric@faces@<Z", "FixedRotation", (0, 0, 0))\
    .constrain("EPAutoImperial@faces@<Z", "FixedPoint", (0, gridfinity.grid_unit * -3, 0))\
    .constrain("EPAutoImperial@faces@<Z", "FixedRotation", (0, 0, 0))\
    .constrain("CraftsmanMetric@faces@<Z", "FixedPoint", (gridfinity.grid_unit * 3, gridfinity.grid_unit * 3, 0))\
    .constrain("CraftsmanMetric@faces@<Z", "FixedRotation", (0, 0, 0))\
    .constrain("CraftsmanImperial@faces@<Z", "FixedPoint", (gridfinity.grid_unit * 3, gridfinity.grid_unit * -3, 0))\
    .constrain("CraftsmanImperial@faces@<Z", "FixedRotation", (0, 0, 0))\
    .constrain("LichampMetric@faces@<Z", "FixedPoint", (gridfinity.grid_unit * -3, gridfinity.grid_unit * 3, 0))\
    .constrain("LichampMetric@faces@<Z", "FixedRotation", (0, 0, 0))\
    .constrain("LichampImperial@faces@<Z", "FixedPoint", (gridfinity.grid_unit * -3, gridfinity.grid_unit * -3, 0))\
    .constrain("LichampImperial@faces@<Z", "FixedRotation", (0, 0, 0))\
    .solve()