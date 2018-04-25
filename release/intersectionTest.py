from checker import checker

#10 = x, 20 = y from each camera
poscalc = checker(10, 20, 10, 20, 10, 20, 10, 20)
x, y, z = poscalc.position_calculation()
print " x: " + str(x) + " y: " + str(y) + " z: " + str(z)