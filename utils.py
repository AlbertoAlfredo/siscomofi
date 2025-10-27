def money_for_db(money: float) -> int:
    return int(money * 100)


def money_for_front(money: int) -> str:
    # return float(money / 100)
    return f"{money / 100:.2f}"



def format_phone(value):
    # Converte para string e remove caracteres não numéricos, se houver
    num = str(value).replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

    if len(num) == 11:  # (99) 99999-9999 (com 9º dígito)
        return f"({num[:2]}) {num[2:7]}-{num[7:]}"
    elif len(num) == 10:  # (99) 9999-9999
        return f"({num[:2]}) {num[2:6]}-{num[6:]}"
    return num  # Retorna sem formatar se for inválido

# app.jinja_env.filters['phone_format'] = format_phone