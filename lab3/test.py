import numpy as np

test = np.zeros(1)
print(test)
test[0] = 123
x = 456
test = np.append(test, x)

print(test)
