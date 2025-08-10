
from factorial import factorial

def main():
    user_input = input("Insira um número inteiro positivo para calcular o fatorial dele: ")

    if not user_input.isdigit() or int(user_input) < 0:
        print("Por favor, insira um número inteiro positivo válido.")
        return
    number = int(user_input)
    print(f"O fatorial de {number} é {factorial(number)}")


if __name__ == "__main__":
    main()