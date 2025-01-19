#Fibonacci number

def fibonacci(n):
    """Generate the first n Fibonacci numbers."""
    a, b = 1, 4

    for _ in range(n):
        yield a
        a, b = b, a + b

# Example usage:
n = 7  # Generate the first n Fibonacci numbers
fib_gen = fibonacci(n)

fib_list = list(fib_gen)

print(fib_list)



