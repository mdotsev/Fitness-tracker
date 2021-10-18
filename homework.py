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
            if i.dates == date.today():
                day_cost += i.amount
        return day_cost

    def get_week_stats(self):
        week_cost = 0
        for i in self.records:
            days = date.today() - i.dates
            if days.days <= 7:
                week_cost += i.amount
        return (week_cost)

class CaloriesCalculator (Calculator):
    def get_calories_remained(self):
        self.remain = self.limit - CaloriesCalculator.get_today_stats(self)
        if self.remain > 0:
            return (f'Сегодня можно съесть что-нибудь ещё, но с общей калорийностью не более {self.remain} кКал')
        else:
            return ('Хватит есть!')

class CashCalculator (Calculator):
    def get_today_cash_remained(self, currency):
        USD_RATE = 0.014
        EURO_RATE = 0.0121
        if currency == 'usd':
            self.remain = USD_RATE
        elif currency == 'eur':
            self.remain = EURO_RATE
        else:
            self.remain = 1
        self.remain *= self.limit -  CashCalculator.get_today_stats(self)
        if self.remain > 0:
            return (f'На сегодня осталось {self.remain} {currency}')
        elif self.remain == 0:
            return ('Денег нет, держись')
        else:
            return (f'Денег нет, держись: твой долг - {-self.remain} {currency}')

class Record:
    """Создает запись для калькулятора."""
    def __init__(self, amount: float, dates: Optional[str] = None, comment: str = None) -> None:
        self.amount = amount
        if dates is None:
            self.dates = dt.datetime.today()
        else: 
            self.dates = dt.datetime.strptime(dates, '%d.%m.%Y').date()
        self.comment = comment

# создадим калькулятор денег с дневным лимитом 1000
cash_calculator = CashCalculator(5000)
cal_calculator = CaloriesCalculator(1000)

cash_calculator.add_record(Record(amount=3000,
                                  comment='бар в Танин др',
                                  dates='08.11.2019'))
cash_calculator.add_record(Record(amount=30000,
                                  comment='бар в Машин др',
                                  dates='18.10.2021'))
cal_calculator.add_record(Record(amount=500,
                                  comment='бар в Танин др',
                                  dates='18.10.2021'))

print(cash_calculator.get_today_stats())
print(cash_calculator.get_week_stats())
print(cal_calculator.get_today_stats())
print(cal_calculator.get_week_stats())
print(cal_calculator.get_calories_remained())
print(cash_calculator.get_today_cash_remained('usd'))
