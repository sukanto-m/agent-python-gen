def fibonacci(n):
    """
    Generate the Fibonacci series up to n terms.

    :param n: The number of terms to generate.
    :type n: int
    :returns: A list containing the Fibonacci series up to n terms.
    :rtype: list
    """
    fib_series = [0, 1]
    while len(fib_series) < n:
        fib_series.append(fib_series[-1] + fib_series[-2])
    return fib_series[:n]


def main():
    """
    Main function to execute the script.
    """
    n = 10
    print(f"The first {n} terms of the Fibonacci series are: {fibonacci(n)}")


if __name__ == "__main__":
    main()
```
This script will print the first 10 terms of the Fibonacci series when run. The `fibonacci` function can also be imported and used in other scripts.