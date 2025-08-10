def factorial(n: int) -> int:
    """
    Calcula o fatorial de um número inteiro não negativo n.
    """
    result = 1
    for i in range(1, n + 1):
        result *= i
    return result