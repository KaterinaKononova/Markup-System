import openpyxl
import numpy as np


def toMarkupExpenses(expenses, total_cost):
    rec_markup = expenses/total_cost*100
    return rec_markup


def toMarkupCompetitorPrice(competitor_price, production_cost):
    rec_markup = (competitor_price - production_cost)/production_cost * 100
    return rec_markup


def seasonalMarkup(date, name):
    wb = openpyxl.load_workbook('./Seasonal.xlsx')
    sheet = wb.active

    number_date = int(date[0:2].strip())
    month_date = date[2:len(date)].strip()
    rec_markup = 0

    if month_date == "ноября" or month_date == "декабря" or month_date == "января":
        for row in sheet.rows:
            if row[0].value == name:
                rec_markup = 100

    if number_date > 6 or number_date < 16 and month_date == "февраля":
        for row in sheet.rows:
            if row[1].value == name:
                rec_markup = 100

    if number_date > 19 or number_date < 26 and month_date == "февраля":
        for row in sheet.rows:
            if row[2].value == name:
                rec_markup = 100

    if number_date >= 1 or number_date < 11 and month_date == "марта":
        for row in sheet.rows:
            if row[3].value == name:
                rec_markup = 100

    if month_date == "апреля":
        for row in sheet.rows:
            if row[4].value == name:
                rec_markup = 100

    if number_date >= 28 and month_date == "апреля" or number_date < 8 and month_date == "мая":
        for row in sheet.rows:
            if row[5].value == name:
                rec_markup = 100

    if number_date > 6 or number_date < 10 and month_date == "мая":
        for row in sheet.rows:
            if row[6].value == name:
                rec_markup = 100

    if month_date == "мая" or month_date == "июня" or month_date == "июля"or month_date == "августа":
        for row in sheet.rows:
            if row[7].value == name:
                rec_markup = 100

    if number_date >= 15 and month_date == "августа" or number_date <= 15 and month_date == "сентября":
        for row in sheet.rows:
            if row[6].value == name:
                rec_markup = 100

    return rec_markup


def toMarkupProfit(last_markup, expenses, total_cost, product_name, data):
    num_of_steps = 40

    markup = np.zeros(num_of_steps)  # наценка
    Num_of_sales = np.zeros(num_of_steps)  # кол-во продаж
    Profit = np.zeros(num_of_steps)  # прибыль
    time = np.zeros(num_of_steps)  # периоды
    A = np.zeros(num_of_steps)  # коеффициент функции продаж
    date_month = ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября", "декабря"]

    A[0] = 50
    markup[0] = last_markup/100  # наценка за прошлый период
    gamma = 0.04

    indicator = 0
    month = data[2:len(data)].strip()
    number_of_month = int(data[0:2].strip())

    for i in range(len(date_month)-1):
        if date_month[i] == data:
            indicator = i
            month = date_month[i]
            break

    for i in range(len(markup)):
        c_date = str(number_of_month) + " " + month
        season_mark = seasonalMarkup(c_date, product_name)
        damage_mark = toMarkupExpenses(expenses, total_cost)

        if i < 39:
            Num_of_sales[i] = A[i] * markup[i] ** (-1.3)
            markup[i + 1] = markup[i] + gamma * (Num_of_sales[i] * markup[i] - Num_of_sales[i - 1] * markup[i - 1])

            if season_mark > markup[i+1] and Num_of_sales[i] >= Num_of_sales[i-1]:
                markup[i+1] = season_mark
                Num_of_sales[i] = A[i] * 2 * markup[i] ** (-1.3)

            time[i] = i

            if markup[i+1] < damage_mark:
                markup[i+1] = damage_mark

            A[i + 1] = A[i] + 6 * np.random.uniform(0, 1)
            Profit[i] = markup[i] * Num_of_sales[i]

            if indicator + 1 == len(date_month):
                indicator = -1

            indicator = indicator + 1
            month = date_month[indicator]

        else:

            time[i] = i

            if season_mark > markup[i] and Num_of_sales[i - 1] >= A[i] / (1 + damage_mark / 100 ** 2):
                Num_of_sales[i] = A[i] * markup[i] ** (-1.3)
            else:
                Num_of_sales[i] = A[i] * markup[i] ** (-1.3)

            Profit[i] = markup[i] * Num_of_sales[i]




print("Сколько штук товара предположительно будет продано за месяц?")
quantity = int(input())
print("Введите стоимость товара за штуку")
cost = int(input())
full_cost = quantity * cost

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

print("Введите цену конкурента, на которую вы ориентируетесь")
co_price = int(input())

print("Введите дату начала продажи (формат ввода - 15 марта) : ")
data = str(input())
print("Введие название товара: ")
product_Name = str(input())


print("Вы уже продавали этот товар?")
answer = str(input())

if answer == "нет":
    markup_1 = toMarkupExpenses(total_expenses, full_cost)
    markup_2 = toMarkupCompetitorPrice(co_price, cost)
    markup_3 = seasonalMarkup(data, product_Name)

    print(markup_1)
    print(markup_2)
    print(markup_3)

    recom_markup = markup_2
    if recom_markup < markup_1:
        recom_markup = markup_1
    elif markup_3 > recom_markup:
        recom_markup = markup_3

    print("Рекомендуемая наценка на первый период времени ", recom_markup)
    print("Рассчет последующих наценок из имеющихся данных ")
    toMarkupProfit(recom_markup, total_expenses, full_cost, product_Name, data)
else:
    print("Введите последнюю наценку, которая была на данный товар в % (например 40) ")
    markup = int(input())
    toMarkupProfit(markup, total_expenses, full_cost, product_Name, data)


