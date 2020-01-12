import numpy as np

coins = "$$ $$ $$ $$$$ $$ $$ $$$$ $$ $$ $$"
horizontalBeam = "           zzzzzzzzzzz           "
verticalBeam = "zzzzzz"
angledBeam = "z      z      z      z      z      z"

coins = np.array(list(coins))
horizontalBeam = np.array(list(horizontalBeam))
verticalBeam = np.array(list(verticalBeam))
angledBeam = np.array(list(angledBeam))

coins = coins.reshape(3,11)
horizontalBeam = horizontalBeam.reshape(3,11)
verticalBeam = verticalBeam.reshape(6,1)
angledBeam = angledBeam.reshape(6,6)

print(horizontalBeam)
print(verticalBeam)
print(angledBeam)
print(coins)
