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
        day_spent = 0
        for i in self.records:
            if i.date == date.today():
                day_spent += i.amount
        return day_spent

    def get_week_stats(self):
        week_spent = 0
        for i in self.records:
            days = date.today() - i.date
            if 0 <= days.days <= 7:
                week_spent += i.amount
        return (week_spent)


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
        currencies = {'usd': [CashCalculator.USD_RATE, 'USD'],
                      'eur': [CashCalculator.EURO_RATE, 'Euro'],
                      'rub': [CashCalculator.RUB_RATE, 'руб']}
        spent = self.limit - CashCalculator.get_today_stats(self)
        self.remain = round(currencies[currency][0] * spent, 2)
        if self.remain > 0:
            return ('На сегодня осталось '
                    f'{self.remain} {currencies[currency][1]}')
        elif self.remain == 0:
            return ('Денег нет, держись')
        else:
            return ('Денег нет, держись: твой долг - '
                    f'{-self.remain} {currencies[currency][1]}')


class Record:
    """Создает запись для калькулятора."""
    def __init__(self, amount: float,
                 date: Optional[str] = None,
                 comment: str = None) -> None:
        self.amount = abs(amount)
        if date is None:
            self.date = dt.datetime.today().date()
        else:
            self.date = dt.datetime.strptime(date, '%d.%m.%Y').date()
        self.comment = comment


cash_calculator = CashCalculator(5000)
cal_calculator = CaloriesCalculator(1000)

cash_calculator.add_record(Record(amount=30,
                                  comment='бар в Танин др',
                                  date='08.11.2019'))
cash_calculator.add_record(Record(amount=300,
                                  comment='бар в Машин др',
                                  date='18.10.2021'))
cash_calculator.add_record(Record(amount=300,
                                  comment='бар в Машин др',
                                  date='18.10.2021'))
cal_calculator.add_record(Record(amount=500,
                                 comment='бар в Танин др',
                                 date='18.10.2021'))
cal_calculator.add_record(Record(amount=500,
                                 comment='бар в Танин др',
                                 date='18.10.2021'))
cal_calculator.add_record(Record(amount=500))


print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())
print(cal_calculator.get_today_stats())
print(cal_calculator.get_week_stats())
print(cal_calculator.get_calories_remained())
print(cash_calculator.get_today_cash_remained('usd'))
print(cash_calculator.get_today_cash_remained('eur'))
print(cash_calculator.get_today_cash_remained('rub'))
