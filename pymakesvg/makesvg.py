pheight = 4719
pwidth = 928

barrierh = 43
barrierbaseh = 8


def barrier(level, color):
    squarex = level[0]
    squarew = level[2]
    squareh = level[3]
    squarey = pheight - level[1] - squareh
    x2 = squarex + 1 * squarew / 3

    barriery = squarey - barrierbaseh - barrierh
    print """
    <rect id="level1" x="{}" y="{}" width="{}" height="{}" fill="none" stroke="{}" stroke-width="4px"></rect>""".format(
        x2, barriery, squarew / 3, barrierh,
        color
        )


def octagon(level, color):
    squarex = level[0]
    squarew = level[2]
    squareh = level[3]
    squarey = pheight - level[1] - squareh
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

    print "<".format()





# the cartesian coordinates of each basket in the WTC tower
# the program converts cartesian to regular coordinates for SVG
# x     y      width height
# of each of the bottoms of the baskets; octagon shapes
levels = [
(339,   1615,  250,  65),
(351.5, 2115,  225,  60),
(364,   2615,  200,  55),
(376.5, 3115,  175,  50),
(389,   3615,  150,  45),
]



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

for level in levels:
    print """
    <xqzrect id="level1" x="{}" y="{}" width="{}" height="{}"></xqzrect>""".format(
        level[0], pheight - level[1] - level[3], level[2], level[3]
        )
    biglevel = (level[0], level[1], level[2], level[3] + 6)
    octagon(biglevel, "#777")
    octagon(level, "#222")
    barrier(level, "#333")


print """
  </svg>
</body>
</html>

"""
