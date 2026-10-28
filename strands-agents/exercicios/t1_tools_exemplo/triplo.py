from strands import tool


@tool
def triplo(x: int) -> int:
    """Devolve o triplo de um número inteiro.

    Args:
        x: Número inteiro
    """
    return x * 3
