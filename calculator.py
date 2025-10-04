import math
import re


class Calculator:
    def evaluate(self, expression: str) -> float:
        """Публичный метод для вычисления выражения."""
        if not expression or expression.strip() == "":
            raise ValueError("Пустое выражение")

        try:
            expr = expression.replace(" ", "")
            return self._evaluate_expression(expr)
        except ZeroDivisionError:
            raise
        except ValueError:
            raise
        except Exception as e:
            raise ValueError(f"Ошибка вычисления: {str(e) or 'неверное выражение'}")

   
    def _evaluate_expression(self, expr: str) -> float:
        expr = re.sub(r'\bpi\b', str(math.pi), expr)
        expr = re.sub(r'\be\b', str(math.e), expr)

        
        expr = self._handle_functions(expr)

        numbers = []
        operators = []
        i = 0

        while i < len(expr):
            c = expr[i]

            if c == ' ':
                i += 1
                continue

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
                while operators and (
                    (self._get_precedence(operators[-1]) > self._get_precedence(c)) or
                    (self._get_precedence(operators[-1]) == self._get_precedence(c) and c != '^')
                ):
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
        """Рекурсивная обработка функций sin, cos, tan, sqrt, log, exp + проверка неизвестных."""

        allowed = {"sin", "cos", "tan", "sqrt", "log", "exp"}

        i = 0
        while i < len(expr):
          
            if expr[i].isalpha():
                match = re.match(r"[a-zA-Z_]+", expr[i:])
                if match:
                    func = match.group(0)
                    func_start = i
                    i += len(func)

                    if i < len(expr) and expr[i] == '(':
                        
                        if func not in allowed:
                            raise ValueError(f"Неизвестная функция: {func}")

                        
                        depth = 0
                        j = i
                        while j < len(expr):
                            if expr[j] == '(':
                                depth += 1
                            elif expr[j] == ')':
                                depth -= 1
                                if depth == 0:
                                    break
                            j += 1
                        if depth != 0:
                            raise ValueError("Несбалансированные скобки в функции")

                        arg_expr = expr[i + 1:j]
                        inner_value = self._evaluate_expression(arg_expr)

                      
                        if str(arg_expr).endswith("deg"):
                            arg_expr = arg_expr[:-3]
                            inner_value = math.radians(inner_value)

                        
                        result = self._apply_function(func, inner_value)

                       
                        expr = expr[:func_start] + str(result) + expr[j + 1:]
                        i = func_start + len(str(result)) - 1
            i += 1

        return expr

    def _apply_function(self, func: str, value: float) -> float:
        if func == "sin":
            return math.sin(value)
        elif func == "cos":
            return math.cos(value)
        elif func == "tan":
            return math.tan(value)
        elif func == "sqrt":
            if value < 0:
                raise ValueError("Квадратный корень из отрицательного числа")
            return math.sqrt(value)
        elif func == "log":
            if value <= 0:
                raise ValueError("Логарифм от неположительного числа")
            return math.log(value)
        elif func == "exp":
            return math.exp(value)
        else:
            raise ValueError(f"Неизвестная функция: {func}")

    # ============================
    # === Арифметика ===
    # ============================
    def _apply_operation(self, numbers, operator):
        if len(numbers) < 2:
            raise ValueError(f"Недостаточно операндов для '{operator}'")

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

    def _get_precedence(self, op):
        return {'+': 1, '-': 1, '*': 2, '/': 2, '^': 3, '(': 0}.get(op, -1)

    def _is_operator(self, c):
        return c in '+-*/^'
