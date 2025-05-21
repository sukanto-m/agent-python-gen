def greet_user():
    """
    This function asks a user for their name and prints "Hello!" followed by the user name.
    """
    name = input("Please enter your name: ")
    print(f"Hello! {name}")

if __name__ == "__main__":
    greet_user()