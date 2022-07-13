import openpyxl
import numpy as np


class CompetitorsPriceMarkup:

    def __init__(self, cost_price, competitor_price):
        self.cost_price = cost_price
        self.comp_price = competitor_price

    def get_cost(self):
        return self.cost_price

    def get_competitor_price(self):
        return self.comp_price

    def get_competitor_price_markup(self):
        rec_markup = (self.comp_price - self.cost_price) / self.cost_price * 100
        return rec_markup


class ExpenseMarkup:
    def __init__(self, cost_price, total_expense, implementation_num):
        self.cost_price = cost_price
        self.total_expense = total_expense
        self.implementation_num = implementation_num

    def get_cost(self):
        return self.cost_price

    def get_expenses(self):
        return self.total_expense

    def get_implementation_period(self):
        return self.implementation_num

    def get_expense_markup(self):
        rec_markup = self.total_expense / (self.implementation_num * self.cost_price) * 100
        return rec_markup


class SeasonalMarkup:

    def __init__(self, name, date):
        self.name = name
        self.date = date

    def get_name(self):
        return self.name

    def get_date(self):
        return self.date

    def get_seasonal_markup(self):
        wb = openpyxl.load_workbook('./Seasonal.xlsx')
        sheet = wb.active

        number_date = int(self.date[0:2].strip())
        month_date = self.date[2:len(self.date)].strip()
        rec_markup = 0

        if month_date == "ноября" or month_date == "декабря" or month_date == "января":
            for row in sheet.rows:
                if row[0].value == self.name:
                    rec_markup = 100

        if number_date > 6 or number_date < 16 and month_date == "февраля":
            for row in sheet.rows:
                if row[1].value == self.name:
                    rec_markup = 100

        if number_date > 19 or number_date < 26 and month_date == "февраля":
            for row in sheet.rows:
                if row[2].value == self.name:
                    rec_markup = 100

        if number_date >= 1 or number_date < 11 and month_date == "марта":
            for row in sheet.rows:
                if row[3].value == self.name:
                    rec_markup = 100

        if month_date == "апреля":
            for row in sheet.rows:
                if row[4].value == self.name:
                    rec_markup = 100

        if number_date >= 28 and month_date == "апреля" or number_date < 8 and month_date == "мая":
            for row in sheet.rows:
                if row[5].value == self.name:
                    rec_markup = 100

        if number_date > 6 or number_date < 10 and month_date == "мая":
            for row in sheet.rows:
                if row[6].value == self.name:
                    rec_markup = 100

        if month_date == "мая" or month_date == "июня" or month_date == "июля" or month_date == "августа":
            for row in sheet.rows:
                if row[7].value == self.name:
                    rec_markup = 100

        if number_date >= 15 and month_date == "августа" or number_date <= 15 and month_date == "сентября":
            for row in sheet.rows:
                if row[6].value == self.name:
                    rec_markup = 100

        return rec_markup


class ResultMarkup:

    def __init__(self, last_markup, pre_last_markup, last_num, pre_last_num, seasonal_markup, exp_markup, comp_markup):
        self.last_markup = last_markup
        self.pre_last_markup = pre_last_markup
        self.last_num = last_num
        self.pre_last_num = pre_last_num
        self.seasonal_markup = seasonal_markup
        self.exp_markup = exp_markup
        self.comp_markup = comp_markup

    def get_rec_markup(self, gamma):
        rec_markup = self.last_markup + gamma * (self.last_markup * self.last_num - self.pre_last_markup * self.pre_last_num)

        if rec_markup < self.exp_markup:
            rec_markup = self.exp_markup
        if self.seasonal_markup > rec_markup and self.last_num >= self.pre_last_num:
            rec_markup = self.seasonal_markup

        return rec_markup

    def get_first_markup(self):
        recom_markup = self.comp_markup
        if self.exp_markup > recom_markup:
            recom_markup = self.exp_markup
        elif self.seasonal_markup > recom_markup:
            recom_markup = self.seasonal_markup

        return recom_markup


print("Сколько штук товара предположительно будет продано за месяц?")
quantity = int(input())
print("Введите стоимость товара за штуку")
cost = int(input())
print("Введите ваши расходы по пунктам: ")
print("Хостинг")
hosting = int(input())
print("Доступ в Интернет: ")
internet = int(input())
print("Бухгалтерское сопровождение")
accountant = int(input())
print("Затраты на рекламу")
advertisement = int(input())
print("Администрирование сайта")
site_administration = int(input())
print("Введите доп. расходы, если такие есть или же просто 0 ")
dop_expenses = int(input())
total_expenses = hosting + internet + accountant + advertisement + site_administration + dop_expenses

exp_markup = ExpenseMarkup(cost, total_expenses, quantity).get_expense_markup()

print("Введите цену конкурента, на которую вы ориентируетесь")
co_price = int(input())

comp_mark = CompetitorsPriceMarkup(cost, co_price).get_competitor_price_markup()

print("Введите дату начала продажи (формат ввода - 15 марта) : ")
data = str(input())
print("Введие название товара: ")
product_Name = str(input())

season_mark = SeasonalMarkup(product_Name, data).get_seasonal_markup()

print("Вы уже продавали этот товар?")
answer = str(input())

amount = 40
mark_array = np.zeros(amount)     # массив наценок
num_array = np.zeros(amount)      # массив количества продаж
A = np.zeros(amount)              # коеффициент функции спроса
date_month = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
              "декабря"]

if answer == "нет":
    rec_mark = ResultMarkup(0, 0, 0, 0, season_mark, exp_markup, comp_mark).get_first_markup()
    print("Рекомендуемая наценка на первый период времени ", rec_mark)
    print("Рассчет последующих наценок из имеющихся данных ")

    mark_array[0] = 0
    mark_array[1] = rec_mark
    A[0] = 50
    A[1] = A[0] + 6 * np.random.uniform(0, 1)
    num_array[0] = 0
    num_array[1] = A[1] * mark_array[1] ** (-1.3)
    indicator = 0
    month = data[2:len(data)].strip()
    number_of_month = int(data[0:2].strip())

    for i in range(len(date_month) - 1):
        if date_month[i] == month:
            indicator = i
            month = date_month[i]
            break

    for i in range(2, len(mark_array)):
        c_date = str(number_of_month) + " " + month
        season_mark = SeasonalMarkup(product_Name, c_date).get_seasonal_markup()

        mark_array[i] = ResultMarkup(mark_array[i - 1], mark_array[i - 2], num_array[i - 1], num_array[i - 2],
                                     season_mark, exp_markup, comp_mark).get_rec_markup(0.04)
        A[i] = A[i - 1] + 6 * np.random.uniform(0, 1)
        num_array[i] = A[i] * mark_array[i] ** (-1.3)

        if indicator + 1 == len(date_month):
            indicator = -1

        indicator = indicator + 1
        month = date_month[indicator]

    print(mark_array)

else:
    print("Введите последнюю наценку, которая была на данный товар в % (например 40) ")
    markup = int(input())
    print("Введите предыдущую наценку в % (например 40) ")
    pre_markup = int(input())

    mark_array[0] = pre_markup
    mark_array[1] = markup
    A[0] = 50
    A[1] = A[0] + 6 * np.random.uniform(0, 1)
    num_array[0] = A[0] * mark_array[0]**(-1.3)
    num_array[1] = A[1] * mark_array[1]**(-1.3)

    indicator = 0
    month = data[2:len(data)].strip()
    number_of_month = int(data[0:2].strip())

    for i in range(len(date_month) - 1):
        if date_month[i] == month:
            indicator = i
            month = date_month[i]
            break

    for i in range(2, len(mark_array)):
        c_date = str(number_of_month) + " " + month
        season_mark = SeasonalMarkup(product_Name, c_date).get_seasonal_markup()

        mark_array[i] = ResultMarkup(mark_array[i-1], mark_array[i-2], num_array[i-1], num_array[i-2], season_mark, exp_markup, comp_mark).get_rec_markup(0.04)
        A[i] = A[i-1] + 6 * np.random.uniform(0, 1)
        num_array[i] = A[i] * mark_array[i]**(-1.3)

        if indicator + 1 == len(date_month):
            indicator = -1

        indicator = indicator + 1
        month = date_month[indicator]

    print(mark_array)

