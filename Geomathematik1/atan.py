import math

x = 2
y = 3


# Q1: x > 0 and y > 0
w1a = math.atan(y / x)
w1b = math.atan2(y, x)

# Q2: x < 0 and y > 0
w2a = math.pi + math.atan(y / -x)
w2b = math.atan2(y, -x)

# Q3: x < 0 and y < 0
w3a = math.pi + math.atan(-y / -x)
w3b = math.atan2(-y, -x)

# Q4: x > 0 and y < 0
w4a = math.atan(-y / x)
w4b = math.atan2(-y, x)


def clean(w):
    deg = math.degrees(w)
    if deg < 0:
        deg += 360
    return f"{deg:.1f}°"


print(clean(w1a), clean(w1b))
print(clean(w2a), clean(w2b))
print(clean(w3a), clean(w3b))
print(clean(w4a), clean(w4b))
