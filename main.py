from search import Search


if __name__ == '__main__':
    while True:
        user_input = input("Hi there, what would you like to know?")
        match user_input:
            case "search":
                search = Search()
                search.month()
            case _:
                print("Sorry that doesn't match any of my commands\n")
