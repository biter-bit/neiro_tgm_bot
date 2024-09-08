def format_date(dt):
    formating_date = dt.strftime('%A, %d %B %Y г. в %H:%M')
    formating_date = formating_date.lower().replace(" 0", " ")
    formating_date += ' (мск)'
    return formating_date