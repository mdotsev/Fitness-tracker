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
        day_stat = [abs(i.amount) for i in self.records
                    if date.today() == i.date]
        return sum(day_stat)

    def get_week_stats(self):  # затраты за неделю
        today = date.today()
        week = today - dt.timedelta(days=7)
        week_stat = [abs(i.amount) for i in self.records
                     if today >= i.date >= week]
        return sum(week_stat)


class CaloriesCalculator (Calculator):
    """Операции над каллориями."""
    def get_calories_remained(self):
        self.remain = self.limit - self.get_today_stats()
        if self.remain > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.remain} кКал')
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

        if spent == 0:
            return ('Денег нет, держись')
        elif currency not in CURRENCIES:
            currs = ', '.join([cur for cur in CURRENCIES])
            return ('Данная валюта не поддерживается. Вы можете '
                    f'выбрать одну из трех валют: {currs}')
        rate, name = CURRENCIES[currency]  # задаем значения через кортеж
        remain = spent / rate  # переводим в заданную валюту
        if remain > 0:
            return ('На сегодня осталось '
                    f'{remain:.2f} {name}')
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{abs(remain):.2f} {name}')


class Record:
    """Создает запись для калькулятора."""
    def __init__(self, amount: float,
                 date: Optional[str] = None,
                 comment: str = None,
                 date_format: str = '%d.%m.%Y') -> None:

        self.amount = amount
        if date is None:  # установка текущей даты при отсутствии 'date'
            self.date = dt.date.today()
        else:  # перевод даты из str() в dt
            self.date = dt.datetime.strptime(date, date_format).date()
        self.comment = comment
