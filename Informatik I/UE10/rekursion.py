def factorial(n: int) -> int:
    if n > 0:
        # Usually the factorial is 1*2*3*...*n
        # Here we write it as n*(n-1)*(n-2)*...*1, by calling
        # the factorial function recursively with decreasing
        # values of n.
        return n * factorial(n - 1)
    else:
        # Eventually, n will be 0 and we have to stop the recursion,
        # because the argument can not be a negative number.
        # By definition, the factorial of 0 is 1.
        return 1


def ggT(a: int, b: int) -> int:
    # The euclidean algorithm for the greatest common divisor:
    # If a and b are both positive integers, then the greatest
    # common divisor of a and b is the same as the greatest
    # common divisor of b and the remainder of a divided by b.
    if a < 0 or b < 0:
        raise ValueError("The arguments must be positive integers.")
    if b == 0:
        return a
    else:
        return ggT(b, a % b)


print(">>>")
print("Aufgabe 1:")
print("Geben Sie die Zahl ein, für die die Fakultät berechnet werden soll:")
n = int(input("Eingabe: "))
print(f"Output: {factorial(n)}")

print("")
print("Aufgabe 2:")
print("Geben Sie die Zahlen ein, für die der ggT berechnet werden soll:")
a = int(input("Zahl 1: "))
b = int(input("Zahl 2: "))
print(f"Output: der ggT von {a} und {b} ist {ggT(a, b)}!")
