def calculate_daily_calories(weight, height, age, gender):

    if not all([weight, height, age, gender]):
        raise ValueError("Усі параметри повинні бути заповнені")

    if gender == 'Чоловік':
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    return round(bmr, 2)

