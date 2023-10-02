# Unreal Test - Maya
# Henry Foley, 2023

import unreal as ue

v1 = ue.Vector()
v1.x = 10
v2 = ue.Vector(10, 20, 30)
v3 = (v1 + v2) * 2
print(v3)
