import datetime as dt
from datetime import date
from typing import Optional


class Calculator:
    """Выполняет всю функциональную часть, задает дневной лимит"""

    def __init__(self, limit):
        self.limit = limit
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_today_stats(self):
        day_cost = 0
        for i in self.records:
            if i.date == date.today():
                day_cost += i.amount
        return day_cost

    def get_week_stats(self):
        week_cost = 0
        for i in self.records:
            days = date.today() - i.date
            if days.days <= 7:
                week_cost += i.amount
        return (week_cost)


class CaloriesCalculator (Calculator):
    def get_calories_remained(self):
        self.remain = self.limit - CaloriesCalculator.get_today_stats(self)
        if self.remain > 0:
            return ('Сегодня можно съесть что-нибудь ещё, но с общей '
                    f'калорийностью не более {self.remain} кКал')
        else:
            return ('Хватит есть!')


class CashCalculator (Calculator):
    USD_RATE = 0.014
    EURO_RATE = 0.0121
    RUB_RATE = 1

    def get_today_cash_remained(self, currency):
        currencies = {'usd': CashCalculator.USD_RATE,
                      'eur': CashCalculator.EURO_RATE,
                      'rub': CashCalculator.RUB_RATE}
        spent = self.limit - CashCalculator.get_today_stats(self)
        self.remain = currencies[currency] * spent
        if self.remain > 0:
            return (f'На сегодня осталось {self.remain} {currency}')
        elif self.remain == 0:
            return ('Денег нет, держись')
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{-self.remain} {currency}')


class Record:
    """Создает запись для калькулятора."""
    def __init__(self, amount: float,
                 date: Optional[str] = None,
                 comment: str = None) -> None:
        self.amount = abs(amount)
        if date is None:
            self.date = dt.datetime.today()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


cash_calculator = CashCalculator(5000)
cal_calculator = CaloriesCalculator(1000)

cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
cash_calculator.add_record(Record(amount=30000,
                                  comment='бар в Машин др',
                                  date='18.10.2021'))
cal_calculator.add_record(Record(amount=500,
                                 comment='бар в Танин др',
                                 date='18.10.2021'))

print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())
print(cal_calculator.get_today_stats())
print(cal_calculator.get_week_stats())
print(cal_calculator.get_calories_remained())
print(cash_calculator.get_today_cash_remained('usd'))
print(cash_calculator.get_today_cash_remained('eur'))
print(cash_calculator.get_today_cash_remained('rub'))
