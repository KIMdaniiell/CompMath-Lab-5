import math
import random
import plots
import iolib


class InterpolatableFunction:
    def __init__(self, str_rep, action):
        self.str_rep = str_rep
        self.action = action


def interpolate():
    actions = [(lambda arg: math.sin(arg), "sin(x)"),
               (lambda arg: 2 * arg ** 3 - arg ** 2 + 9, "2x^3 - x^2 + 9"),
               (lambda arg: 7 * math.log(arg) if arg > 0 else None, "7*ln(x)")]
    functions = [InterpolatableFunction(i[1], i[0]) for i in actions]

    function = functions[get_function_number(functions)-1]
    boundaries = {iolib.get_digit("Введите границу a", iolib.InputType.FLOAT),
                  iolib.get_digit("Введите границу b", iolib.InputType.FLOAT)}
    a, b = min(boundaries), max(boundaries)
    (x_values, y_values) = generate_dots(get_dots_number(), a, b, function)
    x_values, y_values = filer_invalid_dots(x_values, y_values)

    for i in range(len(x_values)):
        iolib.write_debug(str(x_values[i])+"\t;\t"+str(y_values[i])+"\n")

    plots.draw_result(x_values, y_values,
                      sorted([random.random()*(b*1.1-a*0.9)+a*0.9 for i in range(100)]+[a, b, a-0.1*abs(a), b+0.1*abs(b)]),
                      function.action, get_polynomial(x_values, y_values),
                      function.str_rep)
    plots.show_graphs()


def get_function_number(functions):
    iolib.write_message("Выберите интегрируемую интерполируемую функцию:\n")
    number = 0
    functions = [f.str_rep for f in functions]
    for i in range(len(functions) - 1):
        iolib.write_message("\t" + str(i + 1) + ") " + str(functions[i]) + "\n")
    iolib.write_message("\t" + str(len(functions)) + ") " + str(functions[-1]))

    is_valid = False
    while not is_valid:
        number = iolib.get_digit("Номер уравнения", iolib.InputType.INTEGER)
        if number < 1 or number > len(functions):
            iolib.write_error("Функция с таким номером не найдена!")
        else:
            is_valid = True
    return number


def get_dots_number():
    number = 0
    is_valid = False
    while not is_valid:
        number = iolib.get_digit("Количество генерируемых точек", iolib.InputType.INTEGER)
        if number < 1:
            iolib.write_error("Введенное значение слишком мало!")
        else:
            is_valid = True
    return number


def generate_dots(n, a, b, function):
    arguments = [random.random()*(b-a)+a for i in range(n)]
    arguments.sort()
    values = [function.action(arg) for arg in arguments]
    return [arguments, values]


def filer_invalid_dots( x_values, y_values):
    iolib.write_message("\n")
    if y_values.count(None) >= 1:
        iolib.write_error("Выбранный интервал вышел за область допустимых значений функции. ")
        iolib.write_message("Часть сгенерированных точек будет потеряна!\n")
        while y_values.count(None) >= 1:
            x_values.pop(y_values.index(None))
            y_values.pop(y_values.index(None))
    return x_values, y_values


def get_polynomial(x_values, y_values):
    basic_polynomials = [get_basic_polynomial(x_values, i)
                         for i in range(len(x_values))]

    def polynomial(x):
        sum = 0
        for i in range(len(x_values)):
            sum += y_values[i] * basic_polynomials[i](x)
        return sum
    return polynomial


def get_basic_polynomial(x_values, i):
    def basic_polynomial(x):
        numerator, denominator = 1, 1
        for j in range(len(x_values)):
            if j != i:
                numerator *= (x - x_values[j])
                denominator *= (x_values[i] - x_values[j])
        return numerator/denominator
    return basic_polynomial


