import math
import re

class Calculator:
    def evaluate(self, expression: str) -> float:
        if not expression or expression.strip() == "":
            raise ValueError("Пустое выражение")

        try:
            expr = expression.replace(" ", "")
            return self._evaluate_expression(expr)
        except Exception as e:
            raise ValueError(f"Ошибка вычисления: {str(e) or 'неверное выражение'}")

    def _evaluate_expression(self, expr: str) -> float:
        # Константы
        expr = expr.replace("pi", str(math.pi))
        expr = expr.replace("e", str(math.e))

        # Обработка функций
        expr = self._handle_functions(expr)

        numbers = []
        operators = []
        i = 0

        while i < len(expr):
            c = expr[i]

            if c == ' ':
                i += 1
                continue

            # Обработка чисел (включая отрицательные и дробные)
            if c.isdigit() or c == '.' or (c == '-' and (i == 0 or self._is_operator(expr[i - 1]) or expr[i - 1] == '(')):
                num_builder = []

                if c == '-':
                    num_builder.append(c)
                    i += 1

                while i < len(expr) and expr[i].isdigit():
                    num_builder.append(expr[i])
                    i += 1

                if i < len(expr) and expr[i] == '.':
                    num_builder.append('.')
                    i += 1
                    while i < len(expr) and expr[i].isdigit():
                        num_builder.append(expr[i])
                        i += 1

                numbers.append(float("".join(num_builder)))
                continue

            elif c == '(':
                operators.append(c)

            elif c == ')':
                while operators and operators[-1] != '(':
                    self._apply_operation(numbers, operators.pop())
                if operators and operators[-1] == '(':
                    operators.pop()
                else:
                    raise ValueError("Несбалансированные скобки")

            elif self._is_operator(c):
                while operators and self._get_precedence(operators[-1]) >= self._get_precedence(c):
                    self._apply_operation(numbers, operators.pop())
                operators.append(c)

            i += 1

        while operators:
            if operators[-1] == '(':
                raise ValueError("Несбалансированные скобки")
            self._apply_operation(numbers, operators.pop())

        if len(numbers) != 1:
            raise ValueError("Неверное выражение")

        return numbers.pop()

    def _handle_functions(self, expr: str) -> str:
        """Обработка sin, cos, tan, sqrt, log, exp (+ поддержка 'deg')."""

        def replace_func(match):
            func = match.group(1)
            arg_expr = match.group(2)

            # Проверяем, указан ли аргумент в градусах (например sin(90deg))
            is_deg = arg_expr.endswith("deg")
            if is_deg:
                arg_expr = arg_expr[:-3]  # убираем "deg"

            # Рекурсивно вычисляем аргумент
            value = self._evaluate_expression(arg_expr)

            # Переводим градусы в радианы
            if is_deg:
                value = math.radians(value)

            # Вычисляем значение функции
            if func == "sin":
                return str(math.sin(value))
            elif func == "cos":
                return str(math.cos(value))
            elif func == "tan":
                return str(math.tan(value))
            elif func == "sqrt":
                if value < 0:
                    raise ValueError("Квадратный корень из отрицательного числа")
                return str(math.sqrt(value))
            elif func == "log":
                if value <= 0:
                    raise ValueError("Логарифм от неположительного числа")
                return str(math.log(value))
            elif func == "exp":
                return str(math.exp(value))
            else:
                raise ValueError(f"Неизвестная функция: {func}")

        # Ищем выражения вида sin(...), cos(...), sqrt(...), log(...), exp(...)
        pattern = r'(sin|cos|tan|sqrt|log|exp)\(([^()]+)\)'
        while re.search(pattern, expr):
            expr = re.sub(pattern, replace_func, expr)
        return expr

    def _apply_operation(self, numbers: list, operator: str):
        if len(numbers) < 2:
            raise ValueError(f"Недостаточно операндов для оператора: {operator}")

        b = numbers.pop()
        a = numbers.pop()

        if operator == '+':
            numbers.append(a + b)
        elif operator == '-':
            numbers.append(a - b)
        elif operator == '*':
            numbers.append(a * b)
        elif operator == '/':
            if b == 0:
                raise ZeroDivisionError("Деление на ноль")
            numbers.append(a / b)
        elif operator == '^':
            numbers.append(math.pow(a, b))
        else:
            raise ValueError(f"Неизвестный оператор: {operator}")

    def _get_precedence(self, operator: str) -> int:
        if operator in ('+', '-'):
            return 1
        elif operator in ('*', '/'):
            return 2
        elif operator == '^':
            return 3
        elif operator == '(':
            return 0
        return -1

    def _is_operator(self, c: str) -> bool:
        return c in '+-*/^'
