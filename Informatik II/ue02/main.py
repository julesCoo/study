def pascals_triangle(n):
    """Returns the first n lines of Pascal's triangle as a list of lists."""

    # Base case - create a 1x1 array
    if n == 1:
        return [[1]]

    # Recursive case
    # Get the previous lines as 2d array
    lines = pascals_triangle(n - 1)
    last_line = lines[-1]
    next_line = []

    # The next line is the sum of the previous line's adjacent numbers, padded with 1s at both ends
    next_line.append(1)
    for i in range(n - 2):
        next_line.append(last_line[i] + last_line[i + 1])
    next_line.append(1)

    # Create a new array with the next line added to the previous lines
    return [*lines, next_line]


def fibonacci_pascals_triangle(n):
    """Calculates the nth Fibonacci number using Pascal's triangle."""

    triangle = pascals_triangle(n)
    fibonacci_numbers = [0]

    for i in range(n - 1):
        # The (n+1)th Fibonacci number is the sum of the numbers on the nth diagonal of Pascal's triangle
        diagonal_sum = 0

        # Start in the nth row (y) at the 0th column (x)
        x = 0
        y = i

        # Move diagonally up/right until we reach the end of the triangle, summing the numbers we pass
        while y >= 0 and x < len(triangle[y]):
            diagonal_sum += triangle[y][x]
            y -= 1
            x += 1

        fibonacci_numbers.append(diagonal_sum)

    return fibonacci_numbers


print("Pascal's triangle (6 lines):")
for line in pascals_triangle(6):
    print(line)


print("----")
print("First 10 Fibonacci numbers, calculated from Pascal's triangle:")
print(fibonacci_pascals_triangle(10))
