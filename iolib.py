from enum import Enum


class InputType(Enum):
    FLOAT = 0,
    INTEGER = 1,
    BOOLEAN = 2,


def write_debug(message):
    f = open("debug.txt", "a")
    f.write(message)
    f.close()


def write_error(message):
    print("[Ошибка] " + message)


def write_message(message):
    print(message, end="")


def get_digit(message, required_type):
    is_valid = False
    value = None
    while not is_valid:
        print("\n[Ввод] " + message + ": ", end="")
        try:
            match required_type:
                case InputType.FLOAT:
                    value = float(input())
                case InputType.INTEGER:
                    value = int(input())
                case InputType.FLOAT:
                    raw_value = input().lower()
                    value = True if (raw_value == "" or raw_value == "y") else False
            is_valid = True
        except ValueError:
            error_message = ""
            match required_type:
                case InputType.FLOAT:
                    error_message = "Неудалось распознать число"
                case InputType.INTEGER:
                    error_message = "Неудалось распознать число"
            write_error(error_message)
    return value


def print_table_row(data):
    out = ""
    for i in range(len(data)):
        out += data[i] + " "*(25*(i+1)-len(out)-len(data[i]))
    out += "\n"
    write_message(out)


def print_table_headers(headers):
    headers.insert(0, "\n")
    print_table_row(headers)



