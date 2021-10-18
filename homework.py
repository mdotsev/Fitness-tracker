import datetime as dt
from datetime import date
from typing import Optional


class Calculator:
    """Родительский класс, задающий основной функционал программы."""

    def __init__(self, limit: float) -> None:
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):  # затраты за день
        day_spent = 0
        for i in self.records:
            if i.date == date.today():
                day_spent += abs(i.amount)
        return day_spent

    def get_week_stats(self):  # затраты за неделю
        week_spent = 0
        for i in self.records:
            days=7
            days = date.today() - i.date
            if 0 <= days.days <= 7:
                week_spent += abs(i.amount)
        return week_spent


class CaloriesCalculator (Calculator):
    """Операции над каллориями."""
    def get_calories_remained(self):
        self.remain = self.limit - self.get_today_stats()
        if self.remain > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.remain} кКал')
        else:
            return ('Хватит есть!')


class CashCalculator (Calculator):
    """Денежные операции."""
    USD_RATE = 60.00
    EURO_RATE = 70.00
    RUB_RATE = 1.00

    def get_today_cash_remained(self, currency):
        """Производит расчет оставшейся суммы в заданной валюте."""

        CURRENCIES = {
            'usd': (self.USD_RATE, 'USD'),
            'eur': (self.EURO_RATE, 'Euro'),
            'rub': (self.RUB_RATE, 'руб')
        }

        spent = self.limit - self.get_today_stats()  # потрачено за сегодня
        rate, name = CURRENCIES[currency]  # задаем значения через кортеж

        if spent == 0:
            return ('Денег нет, держись')
        elif currency not in CURRENCIES:
            return 'Данная валюта не поддерживается'

        remain = round(spent / rate, 2)  # переводим в заданную валюту
        if remain > 0:
            return ('На сегодня осталось '
                    f'{remain} {name}')
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{abs(remain)} {name}')


class Record:
    """Создает запись для калькулятора."""
    def __init__(self, amount: float,
                 date: Optional[str] = None,
                 comment: str = None) -> None:

        self.amount = amount
        if date is None:  # установка текущей даты при отсутствии 'date'
            self.date = dt.datetime.today().date()
        else:  # перевод даты из str() в dt
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment
