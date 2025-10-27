def money_for_db(money: float) -> int:
    return int(money * 100)


def money_for_front(money: int) -> str:
    # return float(money / 100)
    return f"{money / 100:.2f}"