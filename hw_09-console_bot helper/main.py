user_dict_db = {}


def input_error(func):
    def inner(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except KeyError as ex:
            result = f'{ex}\nPlease try again!\n'
        except ValueError as ex:
            result = f'{ex}\nPlease try again!\n'
        except IndexError as ex:
            result = f'{ex}\nPlease try again!\n'
        return result

    return inner


def available_commands():
    command_list = ['.', 'hello', 'add', 'change',
                    'phone', 'show all', 'good bye', 'close', 'exit']
    command_explain = ['app closing if found in input',
                       'greeting to the user',
                       "adding new user and phone, with spaces enter 'user name' and 'phone number'",
                       "rewrite phone number of the existent user name, with spaces enter 'user name' and 'phone number'",
                       "to show phone number, with space enter 'user name'",
                       "to show all availaple users in the database",
                       'close the application',
                       'close the application',
                       'close the application']
    return ''.join('|{:<10} - {:<20}|\n'.format(command_list[item], command_explain[item]) for item in range(len(command_list)))


@input_error
def adding_new_user(prompt: str) -> str:
    info = ''
    temp_list = prompt.split()
    temp_list[1] = temp_list[1].lower().capitalize()
    if not temp_list[1][:1].isdigit() and (temp_list[2].startswith('+') or temp_list[2][1:].isdigit()) and not temp_list[1] in user_dict_db:
        user_dict_db[temp_list[1]] = temp_list[2]
        info = f"1. '{temp_list[0]}' - user '{temp_list[1]}' and contact info'{temp_list[2]}' successfully added to the database!\n"
    elif temp_list[1] in user_dict_db:
        info = f"1. Sorry but such user name '{temp_list[1]}' is exist in database!\n"
    else:
        info = "1. Error in provided info. User name must start with the letter or contact info must consist only numbers or start with special symbol '+'!\n"
    return info


@input_error
def changing_exist_user(prompt: str) -> str:
    info = ''
    temp_list = prompt.split()
    temp_list[1] = temp_list[1].lower().capitalize()
    if not temp_list[1][:1].isdigit() and (temp_list[2].startswith('+') or temp_list[2][1:].isdigit()) and temp_list[1] in user_dict_db:
        user_dict_db[temp_list[1]] = temp_list[2]
        info = f"2. '{temp_list[0]}' - user '{temp_list[1]}' and contact info'{temp_list[2]}' successfully rewrited in the database!\n"
    elif not temp_list[1] in user_dict_db:
        info = f"2. Sorry but such user name '{temp_list[1]}' isn`t exist in database!\n"
    else:
        info = "2. Error in provided info. User name must start with the letter or contact info must start with number or special symbol '+'!\n"
    return info


@input_error
def looking_exist_user(prompt: str) -> str:
    temp_list = prompt.split()
    temp_list[1] = temp_list[1].lower().capitalize()
    return user_dict_db.get(temp_list[1], f"Such user name '{temp_list[1]}' isn`t exist in database!")


def show_all_users(prompt: str) -> str:
    return user_dict_db


def main():
    while 1:
        from_user = input(
            "To see available list of commands enter 'cli'.\nPlease enter command to proceed: ")

        if from_user.lower() == 'cli':
            print(available_commands())

        elif from_user.lower() == 'hello':
            print('How can I help you?\n')

        elif from_user.lower().find('add ') != -1:
            handler = adding_new_user(from_user)
            print(handler)

        elif from_user.lower().find('change ') != -1:
            handler = changing_exist_user(from_user)
            print(handler)

        elif from_user.lower().find('phone ') != -1:
            handler = looking_exist_user(from_user)
            print(handler, '\n')

        elif from_user.lower() == 'show all':
            handler = show_all_users(from_user)
            print(handler, '\n')

        elif from_user.lower().find('.') != -1 or from_user.lower() in ('good bye', 'close', 'exit'):
            print('Good bye!\n')
            break


if __name__ == '__main__':
    main()
