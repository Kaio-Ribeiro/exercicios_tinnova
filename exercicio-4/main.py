from sum_multiples import sum_multiples

def main():
    user_input = input("Insira um número inteiro positivo para somar os múltiplos de 3 e 5 abaixo dele: ")

    if not user_input.isdigit() or int(user_input) <= 0:
        print("Por favor, insira um número inteiro positivo válido.")
        return

    number = int(user_input)
    print(f"A soma dos múltiplos de 3 e 5 abaixo de {number} é {sum_multiples(number)}")


if __name__ == "__main__":
    main()