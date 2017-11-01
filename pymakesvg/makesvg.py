pheight = 4719
pwidth = 928

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
    <rect id="level1" x="{}" y="{}" width="{}" height="{}"></rect>""".format(
        level[0], pheight - level[1] - level[3], level[2], level[3]
        )


print """
  </svg>
</body>
</html>

"""
