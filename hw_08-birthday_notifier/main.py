from datetime import date, datetime


def get_birthdays_per_week(users: dict) -> dict:
    if not users:
        return {}
    weekdays = ['Monday', 'Tuesday', 'Wednesday',
                'Thursday', 'Friday']
    current_date = date.today()

    birthday_dict = {day: [] for day in weekdays}
    for user in users:
        user_birth = user['birthday']
        time_diff = user_birth - current_date
        if time_diff.days < -366:
            year = current_date.year
            if current_date.month > user_birth.month:
                year = current_date.year + 1
            user_birth = datetime(
                year, user_birth.month, user_birth.day).date()
        if time_diff.days >= 0 or time_diff.days < -366:
            if user_birth.weekday() > len(weekdays) - 1:
                index = 0
            else:
                index = user_birth.weekday()
            week_day = weekdays[index]
            birthday_dict[week_day].append(user['name'])

    users.clear()
    empty_dict = birthday_dict.copy()
    for day, names in empty_dict.items():
        if not names:
            birthday_dict.pop(day)

    users = birthday_dict.copy()
    return users


if __name__ == "__main__":
    users = [
        {"name": "Jan Koum", "birthday": datetime(1976, 1, 1).date()},
    ]
    result = get_birthdays_per_week(users)
    print(result)
    # Виводимо результат
    for day_name, names in result.items():
        print(f"{day_name}: {', '.join(names)}")
