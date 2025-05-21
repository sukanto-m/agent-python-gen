def reverse_string(input_string):
    """
    Reverse the given string.

    Parameters:
    input_string (str): The string to be reversed.

    Returns:
    str: The reversed string.
    """
    return input_string[::-1]


def main():
    """
    Main function to execute the script.
    """
    test_string = "Hello, World!"
    print(f"Original String: {test_string}")
    print(f"Reversed String: {reverse_string(test_string)}")


if __name__ == "__main__":
    main()