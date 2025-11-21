from datetime import datetime


def money_for_db(money: any) -> int:
    if money:
        if type(money) == str:
            money = money.replace("R$", "").strip().replace(".", "")
            money = money.replace(",", ".")
        money = float(money)
        return int(money * 100)
    elif type(money) == int:
        money = float(money)
        return int(money * 100)
    else:
        return money


def money_for_front(money: int | str | None) -> str | float:
    if money:
        money = int(float(money))
        return f"{money / 100:.2f}"
    else:
        return "0.00"


def format_phone(value):
    # Converte para string e remove caracteres não numéricos, se houver
    num = str(value).replace('(', '').replace(')', '').replace('-', '').replace(' ', '')

    if len(num) == 11:  # (99) 99999-9999 (com 9º dígito)
        return f"({num[:2]}) {num[2:7]}-{num[7:]}"
    elif len(num) == 10:  # (99) 9999-9999
        return f"({num[:2]}) {num[2:6]}-{num[6:]}"
    return num  # Retorna sem formatar se for inválido

# app.jinja_env.filters['phone_format'] = format_phone


def date_for_front(date: any) -> any:
    date = str(date)
    date = datetime.strptime(date, '%Y-%m-%d')
    date = date.strftime("%d/%m/%Y")
    return date
