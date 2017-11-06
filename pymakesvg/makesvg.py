pheight = 4719
pwidth = 928
spire_height = 460
spire_color = "#283250"

# coordinates for bottom platform of tower
onelevelx = 339 - 12.5
onelevely = 3039 + 495
onelevelw = 250 + 25
onelevelh = 65 + 5

# these are the changes in coordinates for each level in the tower
# the drawing starts with the bottom platform and add these to get the next platform
deltax = 12.5
deltay = -495
deltaw = -25
deltah = -5


# each platform has a fence-like barrier to prevent people from falling off :)
barrierh = 43
barrierbaseh = 8

nplatforms = 7

platform_underside = "#0a1326"

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
    width = onelevelw + i * deltaw
    height = onelevelh + i * deltah
    # each platform
    level = (x, y, width, height)
    levels.append(level)
    # each spire supporting that platform
    #spires on lower levels have same dimensions
    spire = (x + width / 4, -1, width / 2, spire_height)
    if i < 3:
        spire = (onelevelx + deltax + (onelevelw + deltaw) / 4, -1, (onelevelw + deltaw) / 2, spire_height)
    spires.append(spire)


def barrier(clevel, color):
    squarex = clevel[0]
    squarew = clevel[2]
    squareh = clevel[3]
    squarey = clevel[1]
    x2 = squarex + 1 * squarew / 3

    barriery = squarey - barrierbaseh - barrierh
    print """
    <rect id="clevel1" x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" stroke-width="4px"></rect>""".format(
        x2, barriery, squarew / 3, barrierh,
        color
        )
    # end of barrier()


def drawlevelbase(clevel, color):
    squarex = clevel[0]
    squarew = clevel[2]
    squareh = clevel[3]
    squarey = pheight - clevel[1] - squareh
    x1 = squarex
    x2 = squarex + 1 * squarew / 3
    x3 = squarex + 2 * squarew / 3
    x4 = squarex +     squarew

    y1 = squarey
    y2 = squarey + 1 * squareh / 3
    y3 = squarey + 2 * squareh / 3
    y4 = squarey + squareh

    print """
      <polyline fill="{}" points="{} {}, {} {},  {} {}, {} {},    {} {},  {}, {},      {} {},   {} {}" />

    """.format(
        color,
        x2, y1, x3, y1,
        x4, y2, x4, y3,
        x3, y4, x2, y4,
        x1, y3, x1, y2
    )

    # I really don't know why this line is here
    print "<".format()
    # end of drawlevelbase()


# draw a svg rectangle by printing out the <rect> code
def rect(x, y, width, height, fill, stroke, stroke_width):
    print"""
    <rect id="clevel1" x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="{}" stroke-width="{}"></rect>
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
def spire_for_level(level, spire):
    x = level[0]
    y = level[1]
    width = level[2]
    height = level[3]
    spire_x = spire[0]
    spire_y = y + height / 2   # note this overrides any passed y of spire
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

    #drawlevelbase(bigclevel, "#777")
    #drawlevelbase(clevel, "#222")
    #barrier(clevel, "#333")


# draw all levels in octagons
for i in range(nplatforms):
    octagon(onelevelx + i * deltax, onelevely + i * deltay, onelevelw + i * deltaw, onelevelh + i * deltah, platform_underside, "none", "0")

# draw an ellipse below 1st base where wires meet octagon
# TODO find out what these three lines do; later remove them somehow
fill = spire_color
stroke = "none"
stroke_width = "0";
for i in range(nplatforms):
    spire_for_level(levels[i], spires[i])

# barriers so people don't fall off platform
for i in range(nplatforms):
    barrier(levels[i], "yellow") # TODO #333

draw_wires(wires, "none", wire_stroke, wire_width)

print """
  </svg>
</body>
</html>

"""
