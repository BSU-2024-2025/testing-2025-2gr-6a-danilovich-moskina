from calculator import Calculator

class CalculatorEngine:
    def __init__(self):
        self.calculator = Calculator()

    def start(self):
        print("🎯 Добро пожаловать в улучшенный калькулятор!")
        print("Доступные операции: +, -, *, /, ^ (степень)")
        print("Функции: sin(x), cos(x), tan(x), sqrt(x), log(x), exp(x)")
        print("Константы: pi, e")
        print("Можно использовать градусы: sin(90deg), cos(180deg), tan(45deg)")
        print("Примеры: sin(pi/2), exp(1), sqrt(16), log(10), sin(90deg)")
        print("Для выхода введите 'exit'")

        while True:
            try:
                print("\n" + "═" * 60)
                expr = input("Введите выражение: ").strip()

                if expr.lower() == "exit":
                    break

                if not expr:
                    print("❌ Пустой ввод. Попробуйте снова.")
                    continue

                result = self.calculator.evaluate(expr)
                print(f"✅ Результат: {expr} = {result:.6f}")

            except ValueError as e:
                print(f"❌ Ошибка: {e}")
            except Exception as e:
                print(f"❌ Неожиданная ошибка: {e}")

        print("👋 До свидания!")
