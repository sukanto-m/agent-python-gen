def ask_name_and_greet():
    """
    Ask the user for their name and print a greeting message.
    """
    name = input("Please enter your name: ")
    print(f"Hello! {name}")

if __name__ == "__main__":
    ask_name_and_greet()
This script will ask the user to enter their name and then print a greeting message. The greeting message is 'Hello!' followed by the user's name. The script includes a `main()` block to ensure that the function is only executed when the script is run directly, not when it is imported as a module.