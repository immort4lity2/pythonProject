import locale

locale.setlocale(locale.LC_ALL, '')
# Параметрээр авах шаардлагтай бол үүнийг uncomment болго
# import argparse
from beautifultable import BeautifulTable
from datetime import datetime


def interest_per_payment(amount, rate, days):
    """
    Тухайн төлөлт дээрх хүүгийн хэмжээг олох
    :param amount: Зээлийн үлдэгдэл
    :param rate: Өдрийн хүү
    :param days: Хүү тооцох хоног
    :return: Тухайн төлөлт дээрх хүүгийн хэмжээ
    """
    return amount * rate * days


def days_per_month(month, year):
    """
    Тухайн сар хэдэн хоногтойг олох
    :param month: Сар
    :param year: Жил
    :return: Тухайн сар дахь хоногийн тоо
    """
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        if (year % 4) == 0:
            return 29
        else:
            return 28
    else:
        raise ValueError('month expected', month)


def next_month(month, year):
    """
    Дараагийн сар, жилийг олох
    :param month: Одоогийн сар
    :param year: Одоогийн жил
    :return: Дараагийн сар болон жил
    """
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    return next_month, next_year


def monthly_principal(monthly_payment, current_interest_payment):
    """
    Тухайн төлөлтийн үндсэн зээлийн төлбөрийн мэдээлэл авах
    :param monthly_payment: Сарын тэнцүү төлөлт
    :param current_interest_payment: Тухайн төлөлт дээрх хүүгийн төлбөр
    :return: Тухайн төлөлтийн үндсэн зээлийн төлбөр
    """
    return monthly_payment - current_interest_payment


def amortize(annual_rate, duration_years, start_year, start_month, P):
    """
    Зээлийн хуваарь үүсгэх
    :param annual_rate: Жилийн хүү
    :param duration_years: Зээлийн хугацаа жилээр
    :param start_year: Зээл эхлэх огнооны жил
    :param start_month: Зээл эхлэх огнооны сар
    :param P: Зээлийн дүн
    :return: Зээлийн хуваарь
    """
    n = 0

    # Сарын хүү
    rate_per_payment = annual_rate / 12

    # Нийт төлөлтийн хэмжээ
    totalpmts = duration_years * 12

    # Тэнцүү төлөлтийг олох
    ratio = pow(1 + rate_per_payment, totalpmts)
    payment = (P * rate_per_payment * ratio) / (ratio - 1)

    table = BeautifulTable(maxwidth=120)
    table.columns.header = ["ТӨЛӨЛТ",
                            "Жил",
                            "Сар",
                            "Хүү тооцох хоног",
                            "ЭХНИЙ ҮЛДЭГДЭЛ",
                            "ТӨЛӨХ ДҮН",
                            "ХҮҮ",
                            "ҮНДСЭН ТӨЛБӨР",
                            "ЭЦСИЙН ҮЛДЭГДЭЛ"]

    # Эхний төлөлтийн огноог тохируулах
    year = start_year
    month = start_month
    while P > 0:
        n = n + 1
        amount = P

        days = days_per_month(month, year)
        interest_amount = interest_per_payment(amount, days, rate)

        interest = P * rate_per_payment
        principle = payment - interest

        if P - payment < 0:
            principle = P
        table.rows.append([n,
                           year,
                           month,
                           days,
                           locale.format_string('%.2f', P, True),
                           locale.format_string('%.2f', payment, True),
                           locale.format_string('%.2f', interest, True),
                           locale.format_string('%.2f', principle, True),
                           locale.format_string('%.2f', P - principle, True)])
        P = P - principle
        month, year = next_month(month, year)

    print(table)


if __name__ == '__main__':
    # Параметрээр авах шаардлагтай бол үүнийг uncomment болго
    # parser = argparse.ArgumentParser()
    # parser.add_argument("amount",help="Зээлийн дүн")
    # parser.add_argument("annual_rate",help="Жилийн хүү (5% = .05)")
    # parser.add_argument("duration_by_years",help="Зээлийн хугацаа /жил/")
    # parser.add_argument("start_date", help="Зээл олгох огноо")
    # parser.add_argument("payment_start_date", help="Эхний төлөлтийн огноо")
    # args = parser.parse_args()

    # value = float(args.amount)
    # rate= float(args.annual_rate)
    # years = float(args.duration_by_years)
    # start_date = args.start_date
    # payment_start_date = args.payment_start_date

    # Параметрээр авах шаардлагтай бол үүнийг comment болго
    value = float(input('Зээлийн дүн: '))
    years = float(input('Зээлийн хугацаа жилээр: '))
    rate = float(input('Жилийн хүү (12% = .12): '))
    start_date = input('Зээл эхлэх огноо (Жишээ 2022,3,15): ')
    year_start_date, month_start_date, day_start_date = map(int, start_date.split(','))
    s_date = datetime(year_start_date, month_start_date, day_start_date)

    payment_date = input('Эхний төлөлтийн огноо (Жишээ 2022,3,15): ')
    year_payment_date, month_payment_date, day_payment_date = map(int, payment_date.split(','))
    p_date = datetime(year_payment_date, month_payment_date, day_payment_date)

    # Calculate and printing schedule
    amortize(rate, years, year_start_date, month_start_date, value)
