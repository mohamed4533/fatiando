"""
Simple prism model
------------------

Create a simple geologic model using rectangular prisms and plot it in 3D with
:mod:`fatiando.vis.myv`.

"""
from fatiando.mesher import Prism
from fatiando.vis import myv

# Models in Fatiando are basically sequences of geometric elements from
# fatiando.mesher
model = [
    Prism(0, 1000, 0, 2000, 2000, 2500, {'density': 500}),
    ]

bounds = [-5000, 5000, -5000, 5000, 0, 5000]

myv.figure()
myv.prisms(model)
myv.axes(myv.outline(bounds))
myv.wall_north(bounds)
myv.wall_bottom(bounds)
myv.show()
