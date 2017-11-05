pheight = 4719
pwidth = 928

# coordinates for bottom platform of tower
onelevelx = 339
onelevely = 3039
onelevelw = 250
onelevelh = 65

# these are the changes in coordinates for each level in the tower
# the drawing starts with the bottom platform and add these to get the next platform
deltax = 12.5
deltay = -495
deltaw = -25
deltah = -5

# each platform has a fence-like barrier to prevent people from falling off :)
barrierh = 43
barrierbaseh = 8



# the cartesian coordinates of each basket in the WTC tower
# the program converts cartesian to regular coordinates for SVG
# x     y      width height
# of each of the bottoms of the baskets; drawlevelbase shapes
clevels = [
(339,   1615,  250,  65),
(351.5, 2115,  225,  60),
(364,   2615,  200,  55),
(376.5, 3115,  175,  50),
(389,   3615,  150,  45),
]

# TODO delete these 4 lines:
twolevelx = 351.5
twolevely = pheight - 2115 - 60
twolevelw = 225
twolevelh = 60

twolevelx = onelevelx + deltax
twolevely = onelevely + deltay
twolevelw = onelevelw + deltaw
twolevelh = onelevelh + deltah



def barrier(clevel, color):
    squarex = clevel[0]
    squarew = clevel[2]
    squareh = clevel[3]
    squarey = pheight - clevel[1] - squareh
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

    #print"""
    #<rect id="clevel1" x="{}" y="{}" width="{}" height="{}" fill="{}" stroke="{}" stroke-width="{}"></rect>
    #""".format(x, y, width, height, fill, stroke, stroke_width)

    # starting with x2, y1 we draw this going clockwise around the polygon.
    # starting point was just picked arbitrarily, I chose the leftmost top visible point
    # clockwise is just arbitrary, it just needs to be contiguous
    print """
      <polyline fill="{}" points="{} {}, {} {},  {} {}, {} {},    {} {},  {}, {},      {} {},   {} {}" />

    """.format(
        fill,
        x2, y1, x3, y1,
        x4, y2, x4, y3,
        x3, y4, x2, y4,
        x1, y3, x1, y2
    )

    # end of octagon()






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

for clevel in clevels:
    print """
    <xqzrect id="clevel1" x="{}" y="{}" width="{}" height="{}"></xqzrect>""".format(
        clevel[0], pheight - clevel[1] - clevel[3], clevel[2], clevel[3]
        )
    bigclevel = (clevel[0], clevel[1], clevel[2], clevel[3] + 6)
    drawlevelbase(bigclevel, "#777")
    drawlevelbase(clevel, "#222")
    barrier(clevel, "#333")


# draw levels 2 and 5 in rectangles just to see if deltas are working
rect(twolevelx + 300, twolevely, twolevelw, twolevelh, "red", "green", "5")
rect(389       + 300, 1059,      150,       45,        "red", "green", "5")

# draw all levels in rectangles on the left to see if sizes are ok
for i in range(5):
    rect(onelevelx - 250, onelevely + i * deltay, onelevelw + i * deltaw, onelevelh + i * deltah, "blue", "none", "0")

# draw levels 2 and 5 in octagons to test octagon function
octagon(twolevelx + 50, twolevely, twolevelw, twolevelh, "green", "red", "5")
octagon(389       + 50, 1059,      150,       45,        "green", "red", "5")


print """
  </svg>
</body>
</html>

"""
