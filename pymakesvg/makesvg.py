p_height = 4719
p_width = 928
p_center = p_width / 2.0

sil_color = "black"

# coordinates for bottom platform of tower
level_one_x = 339 - 12.5
level_one_y = 3039 + 495
level_one_width = 250 + 25
level_one_height = 65 + 5

# spire below 0th platform is taller
spire_zero_multiplier = 1.09
spire_height = 465
# a spire's width is the platform's width * spire_width_multiplier
spire_width_multiplier = 0.4
spire_taper_top_y = level_one_y + level_one_height / 2.0 + spire_height * spire_zero_multiplier
spire_taper_top_width = level_one_width * spire_width_multiplier
spire_taper_height = spire_height * .73609
spire_taper_middle_y = spire_taper_top_y + spire_taper_height
spire_taper_middle_width = spire_taper_top_width * 1.86364
# this .75 is just arbitrary, change it to what looks good:
spire_taper_bottom_height = spire_height * .75
spire_color = sil_color # "#283250"

tapered_base_color = sil_color


# these are the changes in coordinates for each level in the tower
# the drawing starts with the bottom platform and add these to get the next platform
delta_x = 12.5
delta_y = -495
delta_width = -25
delta_height = -5

# all platforms are delta_y apart, but
# top platform is nearer to the previous platform
delta_y_top_level = delta_y * .75


# each platform has a fence-like barrier to prevent people from falling off :)
barrier_height = 43
barrier_base_height = 8
barrier_color = "#666" #"yellow"  # TODO #333
barrier_base_color = barrier_color # "green"

peakh = 469
peak_color = sil_color # "blue"
subpeak_color = sil_color # "yellow"

n_platforms = 7

#underside of octagon base
platform_color = sil_color # "#0a1326"

subplatform_color = sil_color #"green"

wire_width = 7;
wire_stroke = sil_color #"red"
wire_y = 3690.38
wire_out = 286.046
wire_delta = 24.3
wire_in = wire_out + wire_delta
#win is the inner set of wires
win_out = 394.27
win_delta = 10.0
win_bottom = 275.414
win_in = win_out + win_delta
wires = [
    #outer
    (wire_out,           wire_y, 0 - 13.94,     p_height + 50.14),
    (p_width - wire_out, wire_y, p_width, p_height),
    (wire_in,           wire_y, 0 + wire_delta,     p_height),
    (p_width - wire_in, wire_y, p_width - wire_delta, p_height),
    #inner
    (win_out,           wire_y, win_bottom,     p_height),
    (p_width - win_out, wire_y, p_width - win_bottom, p_height),
    (win_in,           wire_y, win_bottom + win_delta,     p_height),
    (p_width - win_in, wire_y, p_width - win_bottom - win_delta, p_height),
]

# platforms
# platforms on WTC tower
# each level of levels is a 4-tuple of x, y, width, height
levels = []

spires = []
for i in range(n_platforms):
    x = level_one_x + i * delta_x
    y = level_one_y + i * delta_y
    if i == 6:
        y -= delta_y - delta_y_top_level
    width = level_one_width + i * delta_width
    height = level_one_height + i * delta_height
    # each platform
    level = (x, y, width, height)
    levels.append(level)
    # each spire supporting that platform
    # spires on lower levels (0 to 3) have same dimensions
    # but I'm going to ignore that reality, this looks better!
    spire_width = width * spire_width_multiplier
    spire_x = p_center - spire_width / 2.0
    spire_y = level_one_y + i * delta_y + height / 2.0
    modified_spire_height = spire_height
    if (i == 0):
        # 1.1 is to make it a bit taller than it is supposed to be
        # so that there is no spaces between it and the taper spire below it
        modified_spire_height *= spire_zero_multiplier * 1.1
    spire = (spire_x, spire_y, spire_width, modified_spire_height)
    spires.append(spire)


def draw_barrier(level, fill, stroke, stroke_width):
    square_x = level[0]
    square_width = level[2]
    square_height = level[3]
    square_y = level[1]
    x2 = square_x + 1 * square_width / 3.0
    x3 = square_x + 2 * square_width / 3.0
    x4 = square_x + square_width

    barrier_y = square_y - barrier_base_height - barrier_height
    y2 = barrier_y + barrier_height + square_height / 3.0
    print """
    <rect id="level1" x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" stroke-width="4px"></rect>""".format(
        x2, barrier_y, square_width / 3.0, barrier_height,
        fill
        )
    # draw perimeter of barrier
    print """
    <polygon fill="none" stroke="{}" stroke-width="4" points="{} {} {} {}   {} {} {} {}  {} {} {} {}  {} {} {} {}"/>
    """.format(barrier_color,
               square_x, y2, square_x, y2 - barrier_height,
               x2, barrier_y, x3, barrier_y,
               x4, y2 - barrier_height, x4, y2,
               x3, barrier_y + barrier_height, x2, barrier_y + barrier_height,
               )

    # end of draw_barrier()

def draw_peak(level, fill, stroke, stroke_width):
    color = fill
    square_x = level[0]
    square_y = level[1]
    square_w = level[2]
    square_height = level[3]
    # y location of base of peak
    # this corresponds to y location of top leftmost corner of octagon
    baseline = square_y + square_height / 3.0
    # TODO this looks like a magic number
    baseline_width = .85 * square_w

    # the following peak dimensions were determined by eyeballing a picture
    # I use multiples rather than absolutes to allow for scaling
    # delete me square_height_multiplier = 14 #12.75
    peakx = square_x
    # height of peak is the same as the delta_y (the distance between bases of two octagons)
    peakh = -delta_y
    peaky = baseline - peakh
    peakw = square_w

    #triangle under peak pointing downwards
    # center of square vertically is where the triangle starts:
    tundery = baseline
    tunderw = square_w * .85
    tunderx = p_center - tunderw / 2.0
    tunderh = tunderw
    print """
      <polygon fill="{}" points="{} {}, {} {},  {} {}" />
    """.format(
        subpeak_color,
        tunderx, tundery, tunderx + tunderw, tundery, p_center, tundery + tunderh
    )

    # peak (triangle shape)
    print """
      <polygon fill="{}" points="{} {}, {} {},  {} {}" />
    """.format(
        peak_color,
        tunderx, tundery + 1, tunderx + tunderw, tundery + 1, p_center, tundery - peakh
    )


    # end of peak()


# draw a svg rectangle by printing out the <rect> code
def rect(x, y, width, height, fill, stroke, stroke_width):
    print"""
    <rect id="level1" x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="{}" stroke-width="{}"></rect>
    """.format(x, y, width, height, fill, stroke, stroke_width)
    # end of #rect()


# draw a svg octagon by printing out the <polygon> code
def octagon(x, y, width, height, fill, stroke, stroke_width):
    # the polygon coordinates will be (they are 1 indexed):
    #               x2, y1   x3, y1
    #       x1, y2                    x4, y2
    #       x1, y3                    x4, y3
    #               x2, y4   x3, y4
    x1 = x
    x2 = x + 1 * width / 3
    x3 = x + 2 * width / 3
    x4 = x +     width

    y1 = y
    y2 = y + 1 * height / 3
    y3 = y + 2 * height / 3
    y4 = y + height

    # starting with x2, y1 we draw this going clockwise around the polygon.
    # starting point was just picked arbitrarily, I chose the leftmost top visible point
    # clockwise is just arbitrary, it just needs to be contiguous
    print """
      <polygon fill="{}" points="{} {}, {} {},  {} {}, {} {},    {} {},  {}, {},      {} {},   {} {}" />
    """.format(
        fill,
        x2, y1, x3, y1,
        x4, y2, x4, y3,
        x3, y4, x2, y4,
        x1, y3, x1, y2
    )
    # end of octagon()

# note: width of spire on level 1 and two is the same
def draw_spire_for_level(level, spire, fill, stroke, stroke_width):
    x = level[0]
    y = level[1]
    width = level[2]
    height = level[3]
    spire_x = spire[0]
    spire_y = spire[1] # y + height / 2   # note this overrides any passed y of spire
    spire_width = spire[2]
    spire_height = spire[3]

    print"""
    <ellipse cx="{}" cy="{}" rx="{}" ry="{}" fill="{}" stroke="{}" stroke-width="{}"></ellipse>
    """.format(x + width / 2, y + height / 2, width/4, height /4, fill, stroke, stroke_width)
    print"""
    <rect x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="{}" stroke-width="{}"></rect>
    """.format(spire_x, spire_y, spire_width, spire_height, fill, stroke, stroke_width)

# draw a line, that goes up and down at any angle but first x is leftmost part
# width is exactly path_width all of entire line, as next node is directly horizontal right
# line is tuple of (x1, y1, x2, y2)
def angled_line_v(line, path_width, fill, stroke, stroke_width):
    # clockwise starting at top left point (which is x)
    print """
        <path d="M {} {} l{} 0 L {} {} l-{} 0 z "  fill="{}" stroke="{}" stroke-width="{}"></line>
    """.format(line[0], line[1], path_width, line[2] + path_width, line[3], path_width, fill, stroke, stroke_width)

def draw_wires(wires, fill, stroke, stroke_width):
    for wire in wires:
        print """
              <line x1="{}" y1="{}" x2="{}" y2="{}"  fill="{}" stroke="{}" stroke-width="{}"></line>
        """.format(wire[0], wire[1], wire[2], wire[3], fill, stroke, stroke_width)

    # rest of code is new transform version with paths not lines
    # TODO remove this line for wire_color
    wire_color = "red"
    wire = wires[0]
    # outer wire left
    print """
        <g id="wire_out">
        """
    angled_line_v(wires[0], wire_width, wire_color, "none", "0")
    # right of outer wire left, outer wire right, left of outer wire right
    print """
        </g>
        <use xlink:href="#wire_out" transform="translate({}, 0)"/>
        <use xlink:href="#wire_out" transform="translate({}, 0) scale(-1, 1)"/>
        <use xlink:href="#wire_out" transform="translate({}, 0) scale(-1, 1)"/>
    """.format(wire_delta, p_width - 1, p_width - 1 - wire_delta)

def draw_platform(level, fill, stroke, stroke_width):
    x = level[0]
    y = level[1]
    width = level[2]
    height = level[3]

    # draw the part between bottom of barrier and the platform underside octagon
    octagon(x, y - barrier_base_height, width, height, barrier_base_color, stroke, stroke_width)

    # draw platform base, i.e. the underside octagon of the platform
    octagon(x, y, width, height, fill, stroke, stroke_width)

    # barrier so people don't fall off platform :)
    draw_barrier(level, barrier_color, "none", "0")
    # end draw_platform()

# 8 sided polygon that is not an octagon.  Ugly?  yes!
def draw_subplatform(level, fill, stroke, stroke_width):
    x = level[0]
    y = level[1]
    width = level[2]
    height = level[3]
    # the polygon coordinates like octagon
    #TODO delete these 4 lines of comment
    #               x2, y1   x3, y1
    #       x1, y2                    x4, y2
    #x0, y3                                 x5, y3
    #               x2, y4   x3, y4
    x0 = wire_out - 7  # wire
    x1 = x
    x2 = x + 1 * width / 3
    x3 = x + 2 * width / 3
    x4 = x +     width
    x5 = p_width - wire_out + 7 # wire

    y1 = y
    y2 = y + 1 * height / 3
    y3 = wire_y + 5 #wire
    y4 = y + height * 3

    # starting with x2, y1 we draw this going clockwise around the polygon.
    print """
      <polygon fill="{}" points="{} {}, {} {},  {} {}, {} {},    {} {},  {}, {},      {} {},   {} {}" />
    """.format(
        fill,
        x2, y1, x3, y1,
        x4, y2, x5, y3,
        x3, y4, x2, y4,
        x0, y3, x1, y2
    )
    #end of draw_subplatform

# shape of house roof plus house walls  (flat on top)
# sort of like two parts: top sloping part, and bottom rectangle
def draw_big_fat_base(top_y, top_width, middle_y, middle_width, bottom_height, fill, stroke, stroke_width):
    top_right_x = p_center + top_width / 2.0
    top_left_x  = p_center - top_width / 2.0
    middle_right_x = p_center + middle_width / 2.0
    middle_left_x  = p_center - middle_width / 2.0
    bottom_right_x = middle_right_x
    bottom_left_x  = middle_left_x
    bottom_y = middle_y + bottom_height
    print """
      <polygon fill="{}" points="{} {}, {} {},  {} {}, {} {},  {} {}, {} {}" />
    """.format(
        fill,
        top_right_x, top_y,     middle_right_x, middle_y,     bottom_right_x, bottom_y,
        bottom_left_x, bottom_y, middle_left_x, middle_y,      top_left_x, top_y
    )
    #end draw_big_fat_base

#  ================= end of defs


print """
<html>
<head>
  <style>
  body {
    background-color : #ebbfbd;
  }
  .yellow {
    background-color : yellow;
  }
  </style>
</head>
<body>
  <svg class="yellow" width=500 height="10">
  </svg>


  <svg width="92.8" height="471.9" viewBox="0 0 928 4719">
  <image xlink:href="centeringtower5withreflection.png"
  x="0" y="0"
  width="928" height="4719"/>
  """

# peak
# draw shiny silver triangle thingy on top of tower
# the peak is located at a y where there is usually a platform
# the y at levels[6] is inconsistent with other levels,
# so create a tuple like levels[6] but with the same distance as other levels:
peak_level = (levels[6][0], levels[5][1] + delta_y, levels[6][2], levels[6][3] )
draw_peak(peak_level, "red", "none", "0")


for i in range(n_platforms):
    draw_spire_for_level(levels[i], spires[i], spire_color, "none", "0")

# draw the 8 wires that support the tower at the base
draw_wires(wires, "none", wire_stroke, wire_width)

draw_subplatform(levels[0], subplatform_color, "none", "0")

# draw each platform
for level in levels:
    # TODO color should be platform_underside (maybe)
    draw_platform(level, platform_color, "none", "0")


draw_big_fat_base(spire_taper_top_y, spire_taper_top_width, spire_taper_middle_y, spire_taper_middle_width, spire_taper_bottom_height, tapered_base_color, "none", "0")

print """
  </svg>
</body>
</html>

"""
