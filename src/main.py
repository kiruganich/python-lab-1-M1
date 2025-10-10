from src.power import evaluate
import sys

def main():
    print("Здравствуйте!")
    print("Консольный калькулятор уровня М1")
    print("Программа поддерживает следующие операторы: +, -, *, /, //, %, **, скобки, унарные +/-")
    print("Для выхода введите 'exit' или нажмите Ctrl+C\n")

    while True:
        try:
            expr = input(">>> ").strip()
            if expr.lower() in ('exit', 'quit'):
                print("Выход. До свидания!")
                break
            if not expr:
                continue
            result = evaluate(expr)
            if isinstance(result, float) and result.is_integer():
                print(int(result))
            else:
                print(result)
        except ValueError as e:
            print("Ошибка:", e)
        except KeyboardInterrupt:
            print("\nВыход.  До свидания!")
            break
        except Exception as e:
            print("Неизвестная ошибка:", e)

if __name__ == "__main__":
    main()