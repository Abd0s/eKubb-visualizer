
x = [ i *0.04 for i in range(200)]
y = [ 2 -( i *0.01) for i in range(200)]
z = [-0.0476 * (i ** 2) + 0.281 * i + 0.8 for i in x]

print(x)
print(y)
print(z)



x = [i * -10 for i in x]
y = [i * 10 for i in y]
z = [i * 10 for i in z]

print(x)
print(y)
print(z)
