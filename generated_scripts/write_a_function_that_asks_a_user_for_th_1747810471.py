def ask_name_and_greet():
    """
    Ask for the user's name and print a greeting message.
    """
    name = input("Please enter your name: ")
    print(f"Hello, {name}!")

def main():
    """
    Main function to execute the script.
    """
    ask_name_and_greet()

if __name__ == "__main__":
    main()
```
Please note that this script will not work in an environment where user input is not possible, such as a Jupyter notebook or an online code editor.