def greet_user():
    """
    Ask a user for their name and print a greeting message.
    """
    user_name = input("Please enter your name: ")
    print(f"Hello! {user_name}")

if __name__ == "__main__":
    greet_user()