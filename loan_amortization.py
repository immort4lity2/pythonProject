def perdiem(amount, rate):
    return (amount * rate) / 365


def days_per_month(month, year):
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
    if month == 12:
        next_month = 1
        next_year = year + 1
    else:
        next_month = month + 1
        next_year = year
    return next_month, next_year


def monthly_interest(principal, days, rate):
    return perdiem(principal, rate) * days


def monthly_principal(monthly_payment, current_interest_payment):
    return monthly_payment - current_interest_payment


def yield_expected_payment_schedule(start_year,
                                    start_month,
                                    initial_amount,
                                    rate,
                                    duration_in_years,
                                    monthly_payment):
    year = start_year
    month = start_month
    amount = initial_amount
    for t in range(duration_in_years * 12 + 1):
        days = days_per_month(month, year)
        interest_due = monthly_interest(amount, days, rate)
        if amount > 0:
            yield {'balance at month start': amount,
                   'interest due': interest_due,
                   'year': year,
                   'month': month,
                   'days': days
                   }
        amount = amount - (monthly_payment - interest_due)
        month, year = next_month(month, year)


if __name__ == '__main__':
    arg_dict1 = dict(start_year=2022,
                     start_month=3,
                     initial_amount=1000000,
                     rate=0.05,
                     duration_in_years=1,
                     monthly_payment=88848)
    schedule = list(yield_expected_payment_schedule(**arg_dict1))
    print(schedule)
