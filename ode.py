import math
import iolib
import plots
import random
import lagrange


class InterpolatableFunction:
    def __init__(self, action, solution, str_rep_solution, str_rep_action):
        self.action = action
        self.solution = solution
        self.str_rep = str_rep_action
        self.str_rep = str_rep_solution


def solve_ode():
    od_equations = [InterpolatableFunction(lambda _x, _y: _x ** 2 - math.sin(2 * _x),
                                           lambda _x, c1: math.cos(2*_x)/2 + (_x**3)/3 + c1,
                                           "y' = x^2 - sin(2x)", "y = cos(2x)/2 + x^3/3 + C"),
                    InterpolatableFunction(lambda _x, _y: 3*(_x**3) + 2*(_x**2) - _y,
                                           lambda _x, c1: 3*(_x**3) - 7*(_x**2) + 14*_x -14 + c1/math.exp(_x),
                                           "y' = 3x^3 + 2x^2 - y", "y = 3x^3 -7x^2 +14x -14 + C/exp(x)"),
                    InterpolatableFunction(lambda _x, _y: _x ** 2 - 2 * _y,
                                           lambda _x, c1: 0.5*(_x ** 2) - 0.25*(2 * _x - 1) + c1 / math.exp(2 * _x),
                                           "y' = x^2 - 2y", "y = x^2/2 - x/2 + 1/4 + C/exp(2x)")
                    ]
    od_equation_number = get_function_number(od_equations)
    od_equation = od_equations[od_equation_number - 1]

    x0, y0 = get_initial_data()
    c = y0 - od_equation.solution(x0, 0)
    x, y = [x0], [y0]
    b = get_right_boundary(x0)
    h = get_step()

    while len(x) < 4:
        x_next = round((x[-1] + h) * 10**9) / 10**9
        y_next = ode_next_runge_kutta(od_equation.action, x[-1], y[-1], h)
        x.append(x_next)
        y.append(y_next)

    while x[-1] + h <= b:
        x_next = round((x[-1] + h) * 10**9) / 10**9
        y_next = ode_next_adams(od_equation.action, x, y, h)
        x.append(x_next)
        y.append(y_next)

    iolib.print_table_headers(["X Values", "Adams Values", "True Values", ])
    for i in range(min(len(x), len(y))):
        iolib.print_table_row(["Точка №" + str(i + 1),
                               str(round(x[i] * 100) / 100),
                               str(round(y[i] * 1000000) / 1000000),
                               str(round(od_equation.solution(x[i], c) * 1000000) / 1000000)])

    x_many = sorted([random.random()*(b-x0)+x0 for i in range(100)] + [x0, x[-1]])
    plots.draw_result(x, y, x_many,
                      lambda _x: od_equation.solution(_x, c),
                      lagrange.get_polynomial(x, y),
                      "y(x)")
    plots.show_graphs()


def get_function_number(functions):
    iolib.write_message("Выберите ОДУ:\n")
    number = 0
    functions = [f.str_rep for f in functions]
    for i in range(len(functions) - 1):
        iolib.write_message("\t" + str(i + 1) + ") " + str(functions[i]) + "\n")
    iolib.write_message("\t" + str(len(functions)) + ") " + str(functions[-1]))

    is_valid = False
    while not is_valid:
        number = iolib.get_digit("Номер ОДУ", iolib.InputType.INTEGER)
        if number < 1 or number > len(functions):
            iolib.write_error("ОДУ с таким номером не найдена!")
        else:
            is_valid = True
    return number


def get_right_boundary(left):
    right = 0
    is_valid = False
    while not is_valid:
        right = iolib.get_digit("Введите значение правой границы", iolib.InputType.FLOAT)
        if right <= left:
            iolib.write_error("Введенное значение слишком мало!")
        else:
            is_valid = True
    return right


def get_step():
    h = 0
    is_valid = False
    while not is_valid:
        h = iolib.get_digit("Величина шага", iolib.InputType.FLOAT)
        if h <= 0:
            iolib.write_error("Введенное значение слишком мало!")
        else:
            is_valid = True
    return h


def get_initial_data():
    iolib.write_message("\nВведите начальное условие:\n")
    x0 = iolib.get_digit("Введите x0", iolib.InputType.FLOAT)
    y0 = iolib.get_digit("Введите y0", iolib.InputType.FLOAT)
    return x0, y0


def ode_next_runge_kutta(f, x0, y0, h):
    k1 = f(x0, y0)
    k2 = f(x0 + h / 2, y0 + k1 * h / 2)
    k3 = f(x0 + h / 2, y0 + k2 * h / 2)
    k4 = f(x0 + h, y0 + h * k3)
    return y0 + h / 6 * (k1 + 2 * k2 + 2 * k3 + k4)


def ode_next_adams(derivative_f, x, y, h):
    if len(x) < 4:
        return ode_next_runge_kutta (derivative_f, x[-1], y[-1], h)

    f = [derivative_f(x[-i], y[-i]) for i in range(4, 0, -1)]

    y_next = y[-1] + h/24 * (55*f[-1] - 59*f[-2] + 37*f[-3] - 9*f[-4])

    return y_next

