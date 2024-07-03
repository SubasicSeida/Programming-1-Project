from questionBank import questions


class Account:
    """Create user account with user data."""

    def __init__(self, username, password, email, status=True):
        self.username = username
        self.password = password
        self.email = email
        self.status = status

    def __str__(self):
        return "{0}".format(self.password)


users = {
    "johndoe": Account("johndoe", "1234", "johndoe@example.com"),
    "janedoe": Account("janedoe", "pass", "janedoe@example.com"),
    "hazelnut": Account("hazelnut", "abcd", "hazelnut@example.com"),
    "marshmallow": Account("marshmallow", "ab12", "marshmallow@example.com")
}


def login():
    """User can log in into an existing account with username and password."""
    while True:
        username_entry = ""
        while username_entry not in users:
            username_entry = input("Username: ")
        user = users[username_entry]
        if not user.status:
            print("Account locked")
        else:
            password_count = 0
            password_entry = ""
            while True:
                if password_count >= 5:
                    print("Login attempts exceeded.  Contact customer support for assistance.")
                    user.status = False
                    break
                password_entry = input("Password: ")
                password_count += 1
                if password_entry == user.password:
                    print("Login details accepted. Welcome " + user.username)
                    break
        break
    return user.status


def register():
    """Add a new user."""
    while True:
        new_username = input("Choose a Username: ")
        while new_username in users:
            new_username = input("Username already in use; choose a different username: ")
        password = ""
        while len(password) != 4:
            password = input("Choose a 4 character password: ")
        email = input("Enter email: ")
        user = Account(new_username, password, email)
        print("Welcome " + user.username)
        users[new_username] = str(user)
        break
    return user.status


def log_questions(question, filename="questionHistory.txt"):
    """Saves all questions that the logged-in user has asked."""
    with open(filename, "a") as file:
        file.write(question.strip() + "\n")


def talk_to_chatbot(logged_in):
    """User inputs a question from a predefined question bank and gets a predefined response."""
    print("Ask me any question. If you want to exit, type (exit) or (quit).")
    while True:
        question = input().lower()
        if question.lower() in ["exit", "quit"]:
            print("Goodbye!")
            return 0
        else:
            answer = questions.get(question, "I don't know the answer to that question.")
        print(answer)
        if logged_in:
            log_questions(question)


def question_history(filename="questionHistory.txt"):
    """Reads the question log."""
    try:
        with open(filename, "r") as file:
            logged_questions = file.readlines()
    except FileNotFoundError:
        print(f"The file {filename} does not exist.")
        return 0
    if logged_questions:
        print("Logged Questions : ")
        for index, question in enumerate(logged_questions, start=1):
            print(f"{index}. {question.strip()}")
    else:
        print("No questions logged.")
    return 0


def delete_file_content(filename="questionHistory.txt"):
    with open(filename, "w") as file:
        file.truncate()


def chatbot():
    print()
    print("Welcome to ChatBot!")
    status = False
    logged_in = False
    while not status:
        account = int(input("Would you like to (0) Continue as a Guest?, (1) Log in or (2) Register? "))
        if account == 1:
            status = login()
            logged_in = True
        elif account == 2:
            status = register()
            logged_in = True
        else:
            break

    option = 0
    while option != 5:
        print()
        print("1. Talk to ChatBot\n2. See Question History\n3. Exit")
        option = int(input("Enter a number for the wanted activity : "))
        match option:
            case 1:
                print()
                talk_to_chatbot(logged_in)
            case 2:
                if account:
                    question_history()
                    print()
                else:
                    print("You are not logged in!")
                    print()
            case 3:
                print("Thank you for using ChatBot.")
                delete_file_content()
                return 0
            case _:
                print("Please enter a valid number.")


chatbot()