"""
Euler Deconvolution
-------------------------------------

Euler deconvolution attempts to estimate the coordinates of simple (idealized)
sources from the input potential field data.
There is a strong assumption that the sources have simple geometries, like
spheres, vertical pipes, vertical planes, etc.

"""
from __future__ import print_function
import numpy as np
import matplotlib.pyplot as plt
from fatiando.mesher import Prism
from fatiando import gridder, utils
from fatiando.gravmag import prism, transform
from fatiando.gravmag.euler import Classic, MovingWindow

###############################################################################
# Make some synthetic magnetic data to test our Euler deconvolution.

# The regional field
inc, dec = -45, 0
# Make a model of two prisms magnetized by induction only
model = [
    Prism(-1500, -500, -1500, -500, 1000, 2000,
          {'magnetization': utils.ang2vec(2, inc, dec)}),
    Prism(500, 1500, 1000, 2000, 1000, 2000,
          {'magnetization': utils.ang2vec(2, inc, dec)}),
    ]
# Generate some data from the model
shape = (100, 100)
bounds = [-5000, 5000, -5000, 5000, 0, 5000]
area = bounds[0:4]
x, y, z = gridder.regular(area, shape, z=-150)
data = prism.tf(x, y, z, model, inc, dec)
# Calculate the derivatives using FFT
xderiv = transform.derivx(x, y, data, shape)
yderiv = transform.derivy(x, y, data, shape)
zderiv = transform.derivz(x, y, data, shape)

###############################################################################
# Now we can run our Euler solver on a moving window over the data.
# Each window will produce an estimated point for the source.
# We use a structural index of 3 to indicate that we think the sources are
# spheres.

# Run the Euler deconvolution on moving windows to produce a set of solutions
euler = Classic(x, y, z, data, xderiv, yderiv, zderiv, structural_index=3)
solver = MovingWindow(euler, windows=(10, 10), size=(1000, 1000))
# Use the fit() method to obtain the estimates
solver.fit()

###############################################################################
# Plot the solutions on top of the magnetic data. Remember that the true depths
# of the center of these sources is 1500 m.

plt.figure()
plt.title('Euler deconvolution results')
plt.contourf(y.reshape(shape), x.reshape(shape), data.reshape(shape), 30,
             cmap="RdBu_r")
plt.scatter(solver.estimate_[:,1], solver.estimate_[:,0],
            s=50, c=solver.estimate_[:,2], cmap='cubehelix')
plt.colorbar(pad=0).set_label('Depth (m)')
plt.xlim(area[2:])
plt.ylim(area[:2])
plt.tight_layout()
plt.show()
