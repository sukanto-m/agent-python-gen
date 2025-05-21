```python
def add_numbers(a, b):
    """
    Return the sum of two numbers.

    Parameters:
    a (int or float): The first number.
    b (int or float): The second number.

    Returns:
    int or float: The sum of a and b.
    """
    return a + b

def main():
    # Test cases to verify the correctness of the add_numbers function
    print("Test Case 1: add_numbers(2, 3) =", add_numbers(2, 3))  # Expected output: 5
    print("Test Case 2: add_numbers(-1, 5) =", add_numbers(-1, 5))  # Expected output: 4
    print("Test Case 3: add_numbers(0, 0) =", add_numbers(0, 0))  # Expected output: 0
    print("Test Case 4: add_numbers(3.5, 2.5) =", add_numbers(3.5, 2.5))  # Expected output: 6.0
    print("Test Case 5: add_numbers(-3.5, -2.5) =", add_numbers(-3.5, -2.5))  # Expected output: -6.0

if __name__ == "__main__":
    main()
```