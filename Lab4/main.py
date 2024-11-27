from typing import List, Dict, Callable, Tuple


def pick_variable(assignments, vars_to_assign, restrictions, value_ranges):
    """
    Обирає змінну для присвоєння, яка бере участь у найбільшій кількості обмежень.
    """
    # Визначаємо змінні, які ще не були призначені.
    remaining = [v for v in vars_to_assign if v not in {k for entry in assignments for k in entry}]

    # Підраховуємо кількість обмежень для кожної змінної.
    def count_restrictions(variable):
        return sum(variable in constraint["vars"] for constraint in restrictions)

    # Повертаємо змінну з найбільшою кількістю обмежень.
    return max(remaining, key=count_restrictions)


def prioritize_values(variable, value_ranges, assignments, restrictions):
    """
    Сортує значення для змінної за принципом найменшої кількості конфліктів.
    """

    def conflict_count(value):
        # Створюємо тестове присвоєння для перевірки конфліктів.
        test_case = {variable: value}
        return sum(
            not constraint["predicate"](assignments + [test_case], *[
                test_case.get(v) for v in constraint["vars"]
            ])
            for constraint in restrictions if variable in constraint["vars"]
        )

    # Сортуємо значення за кількістю конфліктів (від найменшої до найбільшої).
    return sorted(value_ranges[variable], key=conflict_count)


class ConstraintSatisfactionProblem:
    def __init__(self, variables, value_ranges, restrictions):
        """
        Ініціалізує проблему із заданими змінними, доменами значень та обмеженнями.
        """
        self.vars = variables
        self.value_ranges = value_ranges  # Діапазони допустимих значень для змінних.
        self.restrictions = restrictions  # Список обмежень.
        self.current_state = []  # Список поточних призначень.

    def check_validity(self, new_entry):
        """
        Перевіряє, чи нове присвоєння узгоджується з усіма обмеженнями.
        """
        for restriction in self.restrictions:
            involved_vars = restriction["vars"]
            # Знаходимо записи, які стосуються поточного обмеження.
            related_entries = [
                e for e in self.current_state + [new_entry] if all(v in e for v in involved_vars)
            ]
            for entry in related_entries:
                # Отримуємо значення змінних для перевірки обмеження.
                values = [entry[var] for var in involved_vars]
                # Перевіряємо, чи виконується обмеження.
                if not restriction["predicate"](self.current_state + [new_entry], *values):
                    return False
        return True

    def search_solution(self):
        """
        Реалізує пошук рішення за допомогою методу з поверненням.
        """
        # Перевіряємо, чи досягнуто кінцевий стан.
        if len(self.current_state) == NUM_LECTURES * len(self.value_ranges["group"]):
            return self.current_state

        # Перебір усіх можливих значень для кожної змінної.
        for grp in self.value_ranges["group"]:
            for tm in self.value_ranges["time"]:
                for lect in self.value_ranges["lecturer"]:
                    for clsrm in self.value_ranges["classroom"]:
                        candidate = {
                            "group": grp,
                            "time": tm,
                            "lecturer": lect,
                            "classroom": clsrm,
                        }
                        # Перевіряємо, чи нове присвоєння узгоджується з обмеженнями.
                        if self.check_validity(candidate):
                            # Додаємо нове присвоєння до поточного стану.
                            self.current_state.append(candidate)
                            # Рекурсивно викликаємо функцію для подальшого пошуку.
                            result = self.search_solution()
                            if result is not None:
                                return result
                            # Відкат, якщо рішення не знайдено.
                            self.current_state.pop()

        # Якщо рішення не знайдено, повертаємо None.
        return None


# Змінні (параметри розкладу).
variables = ["lecturer", "classroom", "group", "time"]

# Діапазони значень для змінних.
value_ranges = {
    "lecturer": ["Taranukha V. Y.", "Tkachenko O. M.", "Pashko A. O.", "Bobyl B. V."],
    "time": ["Monday 8:40", "Monday 10:35", "Tuesday 8:40", "Tuesday 10:35"],
    "classroom": ["101", "302", "405"],
    "group": ["MI-41", "MI-42", "TK-4"],
}

# Максимальна кількість лекцій для кожної групи.
NUM_LECTURES = 3

# Список обмежень.
restrictions = [
    # Один викладач не може бути зайнятий у два різні часи.
    {"vars": ("lecturer", "time"),
     "predicate": lambda entries, l, t: sum(e["lecturer"] == l and e["time"] == t for e in entries) <= 1},
    # Група не може бути присутньою на двох лекціях одночасно.
    {"vars": ("group", "time"),
     "predicate": lambda entries, g, t: sum(e["group"] == g and e["time"] == t for e in entries) <= 1},
    # Аудиторія не може використовуватись одночасно для різних лекцій.
    {"vars": ("classroom", "time"),
     "predicate": lambda entries, r, t: sum(e["classroom"] == r and e["time"] == t for e in entries) <= 1},
    # Обмеження на доступний час викладачів.
    {"vars": ("lecturer", "time"), "predicate": lambda entries, l, t: (l, t) in [
        ("Taranukha V. Y.", "Monday 8:40"),
        ("Taranukha V. Y.", "Monday 10:35"),
        ("Taranukha V. Y", "Tuesday 8:40"),
        ("Tkachenko O. M.", "Monday 8:40"),
        ("Tkachenko O. M.", "Monday 10:35"),
        ("Tkachenko O. M.", "Tuesday 10:35"),
        ("Tkachenko O. M.", "Tuesday 8:40"),
        ("Pashko A. O.", "Monday 8:40"),
        ("Pashko A. O.", "Monday 10:35"),
        ("Pashko A. O.", "Tuesday 8:40"),
        ("Pashko A. O.", "Tuesday 10:35"),
        ("Bobyl B. V.", "Tuesday 10:35"),
    ]},
    # Обмеження на кількість пар для кожної групи.
    {"vars": ("group",), "predicate": lambda entries, g: sum(e["group"] == g for e in entries) <= NUM_LECTURES},
]

# Ініціалізація CSP.
scheduler = ConstraintSatisfactionProblem(variables, value_ranges, restrictions)

# Генерація розкладу.
schedule = scheduler.search_solution()

# Виведення результату.
if schedule:
    print("Розклад успішно знайдено:")
    for entry in schedule:
        print(entry)
else:
    print("Не вдалося знайти розклад.")
