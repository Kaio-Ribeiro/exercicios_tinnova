def sum_multiples(n: int) -> int:
    """
    Retorna a soma dos múltiplos de 3 ou 5 abaixo de n.
    """
    sum = 0
    for i in range(1, n):
        if i % 3 == 0 or i % 5 == 0:
            sum += i
    return sum