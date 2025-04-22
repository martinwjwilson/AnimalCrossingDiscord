from search import Search

search = Search()

if __name__ == '__main__':
    while True:
        user_input = input("Hi there, what would you like to know?\n")
        match user_input:
            case "month":
                search.month()
            case "arriving":
                search.arriving()
            case "leaving":
                search.leaving()
            case _:
                print("Sorry that doesn't match any of my commands\n")
