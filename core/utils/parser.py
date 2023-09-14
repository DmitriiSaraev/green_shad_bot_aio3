def date_parser(date):
    # 15,09,23
    #'2023-09-15'
    date_pars = date.split('.')
    day = date_pars[0]
    month = date_pars[1]
    year = '20' + date_pars[2]

    return f'{year}-{month}-{day}'

