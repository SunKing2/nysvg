pheight = 4719
pwidth = 928
pcenter = pwidth / 2.0

barrier_color = "yellow"

# coordinates for bottom platform of tower
onelevelx = 339 - 12.5
onelevely = 3039 + 495
onelevelw = 250 + 25
onelevelh = 65 + 5

spire_height = 460
# a spire's width is the platform's width * spire_width_multiplier
spire_width_multiplier = 0.4
spire_taper_top_y = onelevely + onelevelh / 2.0 + spire_height * 1.09
spire_taper_top_width = onelevelw * spire_width_multiplier
spire_taper_height = spire_height * .73609
spire_taper_middle_y = spire_taper_top_y + spire_taper_height
spire_taper_middle_width = spire_taper_top_width * 1.86364
# this .75 is just arbitrary, change it to what looks good:
spire_taper_bottom_height = spire_height * .75
spire_color = "#283250"


# these are the changes in coordinates for each level in the tower
# the drawing starts with the bottom platform and add these to get the next platform
deltax = 12.5
deltay = -495
deltaw = -25
deltah = -5

# all platforms are deltay apart, but
# top platform is nearer to the previous platform
deltay_top_level = deltay * .8


# each platform has a fence-like barrier to prevent people from falling off :)
barrierh = 43
barrierbaseh = 8

peakh = 469

nplatforms = 7

platform_underside = "#0a1326"

subplatform_color = "green"

wire_width = "7";
wire_stroke = "red"
wire_y = 3690.38
wire_out = 286.046
wire_delta = 24.3
wire_in = wire_out + wire_delta
win_out = 394.27
win_delta = 10.0
win_bottom = 275.414
win_in = win_out + win_delta
wires = [
    #outer
    (wire_out,           wire_y, 0,     pheight),
    (pwidth - wire_out, wire_y, pwidth, pheight),
    (wire_in,           wire_y, 0 + wire_delta,     pheight),
    (pwidth - wire_in, wire_y, pwidth - wire_delta, pheight),
    #inner
    (win_out,           wire_y, win_bottom,     pheight),
    (pwidth - win_out, wire_y, pwidth - win_bottom, pheight),
    (win_in,           wire_y, win_bottom + win_delta,     pheight),
    (pwidth - win_in, wire_y, pwidth - win_bottom - win_delta, pheight),
]

# platforms
# platforms on WTC tower
# each level of levels is a 4-tuple of x, y, width, height
levels = []

spires = []
for i in range(nplatforms):
    x = onelevelx + i * deltax
    y = onelevely + i * deltay
    if i == 6:
        y -= deltay - deltay_top_level
    width = onelevelw + i * deltaw
    height = onelevelh + i * deltah
    # each platform
    level = (x, y, width, height)
    levels.append(level)
    # each spire supporting that platform
    # spires on lower levels (0 to 3) have same dimensions
    # but I'm going to ignore that reality, this looks better!
    spire_width = width * spire_width_multiplier
    spire_x = pcenter - spire_width / 2.0
    spire_y = onelevely + i * deltay + height / 2.0
    modified_spire_height = spire_height
    if (i == 0):
        modified_spire_height *= 1.09  # TODO magic number
    spire = (spire_x, spire_y, spire_width, modified_spire_height)
    spires.append(spire)


def barrier(level, color):
    squarex = level[0]
    squarew = level[2]
    squareh = level[3]
    squarey = level[1]
    x2 = squarex + 1 * squarew / 3

    barriery = squarey - barrierbaseh - barrierh
    print """
    <rect id="level1" x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" stroke-width="4px"></rect>""".format(
        x2, barriery, squarew / 3, barrierh,
        color
        )
    # end of barrier()

def draw_peak(level, color):
    squarex = level[0]
    squarey = level[1]
    squarew = level[2]
    squareh = level[3]
    # y location of base of peak
    # this corresponds to y location of top leftmost corner of octagon
    baseline = squarey + squareh / 3.0
    # TODO this looks like a magic number
    baseline_width = .85 * squarew

    # the following peak dimensions were determined by eyeballing a picture
    # I use multiples rather than absolutes to allow for scaling
    # delete me squareh_multiplier = 14 #12.75
    peakx = squarex
    # height of peak is the same as the deltay (the distance between bases of two octagons)
    peakh = -deltay
    peaky = baseline - peakh
    peakw = squarew

    #triangle under peak pointing downwards
    # center of square vertically is where the triangle starts:
    tundery = baseline
    tunderw = squarew * .85
    tunderx = pcenter - tunderw / 2.0
    tunderh = tunderw
    color="blue"
    print """
      <polygon fill="{}" points="{} {}, {} {},  {} {}" />
    """.format(
        color,
        tunderx, tundery, tunderx + tunderw, tundery, pcenter, tundery + tunderh
    )

    color = "green"
    print """
      <polygon fill="{}" points="{} {}, {} {},  {} {}" />
    """.format(
        color,
        tunderx, tundery, tunderx + tunderw, tundery, pcenter, tundery - peakh
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

def draw_wires(wires, fill, stroke, stroke_width):
    for wire in wires:
        print """
            <line x1="{}" y1="{}" x2="{}" y2="{}"  fill="{}" stroke="{}" stroke-width="{}"></line>
        """.format(wire[0], wire[1], wire[2], wire[3], fill, stroke, stroke_width)

def draw_platform(level, fill, stroke, stroke_width):
    x = level[0]
    y = level[1]
    width = level[2]
    height = level[3]
    # base of platform:
    octagon(x, y, width, height, fill, stroke, stroke_width)
    # barrier so people don't fall off platform :)
    barrier(level, barrier_color) # TODO #333
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
    x0 = wire_out
    x1 = x
    x2 = x + 1 * width / 3
    x3 = x + 2 * width / 3
    x4 = x +     width
    x5 = pwidth - wire_out

    y1 = y
    y2 = y + 1 * height / 3
    y3 = wire_y
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
    top_right_x = pcenter + top_width / 2.0
    top_left_x  = pcenter - top_width / 2.0
    middle_right_x = pcenter + middle_width / 2.0
    middle_left_x  = pcenter - middle_width / 2.0
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
peak_level = (levels[6][0], levels[5][1] + deltay, levels[6][2], levels[6][3] )
draw_peak(peak_level, "red")


for i in range(nplatforms):
    draw_spire_for_level(levels[i], spires[i], spire_color, "none", "0")

# draw each platform
for level in levels:
    # TODO color should be platform_underside (maybe)
    draw_platform(level, "red", "none", "0")


# draw the 8 wires that support the tower at the base
draw_wires(wires, "none", wire_stroke, wire_width)

draw_subplatform(levels[0], "green", "none", "0")

draw_big_fat_base(spire_taper_top_y, spire_taper_top_width, spire_taper_middle_y, spire_taper_middle_width, spire_taper_bottom_height, "blue", "none", "0")
#draw_big_fat_base(spire_taper_top_y, 20, 340, 40, 200, "blue", "none", "0")

print """
  </svg>
</body>
</html>

"""
