import locale
locale.setlocale(locale.LC_ALL, '')
# Параметрээр авах шаардлагтай бол үүнийг uncomment болго
#import argparse
from beautifultable import BeautifulTable
from datetime import datetime


def amortize(P, r, t):
    n = 0
    #Сарын хүү
    intrate = r / 12
    #Нийт төлөлтийн хэмжээ
    totalpmts = t * 12
    ratio = pow(1 + intrate, totalpmts)
    #Тэнцүү төлөлтийг олох
    payment = (P * intrate * ratio) / (ratio - 1)

    table = BeautifulTable(maxwidth=120)
    table.columns.header = ["ТӨЛӨЛТ", "ЭХНИЙ ҮЛДЭГДЭЛ", "ТӨЛӨХ ДҮН", "ХҮҮ", "ҮНДСЭН ТӨЛБӨР", "ЭЦСИЙН ҮЛДЭГДЭЛ"]
    while P > 0:
        n = n + 1

        interest = P * intrate
        principle = payment - interest

        if P - payment < 0:
            principle = P
        table.rows.append([n, locale.format_string('%.2f', P, True),
                           locale.format_string('%.2f', payment, True),
                           locale.format_string('%.2f', interest, True),
                           locale.format_string('%.2f', principle, True),
                           locale.format_string('%.2f', P - principle, True)])
        P = P - principle

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
    amortize(value, rate, years)