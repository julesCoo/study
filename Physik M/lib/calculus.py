# Numeric integration of a function f(x) from lower to upper
def integrate(f, lower, upper, n=10000):
    step_size = (upper - lower) / n
    sum = 0
    for i in range(n):
        x = lower + i * step_size
        sum += f(x) * step_size
    return sum


# Numeric derivation of a function f(x) at x
def derive(x, f):
    dx = 0.0001
    return (f(x + dx) - f(x - dx)) / (2 * dx)
