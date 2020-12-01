import csv
import sys


def read_database():
    fi = open("bank.csv")
    for line in fi:
        if not len(line.split(',')) == 4:
            continue
        username, account_number, password, amount = line.split(',')
        database[account_number] = {
            'username': username,
            'password': password,
            'amount': int(amount)
        }
    fi.close()


def format_database():
    with open("bank.csv", "r") as f:
        lines = f.readlines()
    with open("bank.csv", "w") as fo:
        for line in lines:
            if len(line) != 1:
                fo.write(line)
        f.close()


def check_user_pass_input(acount_number, password):
    if database.get(acount_number) is None:
        return False
    elif database.get(acount_number).get('password') == password:
        return True
    else:
        return False


def display_check_monney(acount_number):
    so_du = database.get(acount_number).get('amount')
    print("Số dư là : " + str(so_du))


def convert_database_to_array():
    fi = open('bank.csv')
    lines = fi.readlines()
    array_database = []
    for line in lines:
        array_database.append(line)
    return array_database


def update_pass_to_database(acount_number, password):
    # update password mới
    database[acount_number]['password'] = password
    with open("bank.csv", "w") as file:
        writer = csv.writer(file)
        for key in database:
            writer.writerow([database[key]['username'], key, database[key]['password'], int(database[key]['amount'])])


def update_money_to_database(acount_number, amount):
    database[acount_number]['amount'] = amount
    with open("bank.csv", "w") as file:
        writer = csv.writer(file)
        for line in database:
            writer.writerow(
                [database[line]['username'], line, database[line]['password'], int(database[line]['amount'])])


def cash_out(acount_number):
    cash_current = database.get(acount_number).get('amount')
    print("Số dư : " + str(cash_current))
    print("-------------------")
    count = 0
    while count != 3:
        input_cashout = int(input("Nhập số tiền :"))
        if input_cashout > cash_current:
            print("Tài khoản không đủ để thực hiện giao dịch")
            print("Xin mời nhập lại")
            count += 1
        else:
            print("Rút tiền thành công, vui lòng nhận tiền")
            remaining_money = int(cash_current) - input_cashout
            update_money_to_database(acount_number, remaining_money)
            return True
    return False


def transfer_money(acount_number_sending):
    print("======Chuyển khoản======")
    account_number_recieved = input("Nhập số tài khoản người nhận :")
    if database.get(account_number_recieved) is None:
        print("Tài khoản người nhận không có trong hệ thống, vui lòng nhập lại")
        transfer_money(acount_number_sending)
    count = 0
    current_money = database.get(acount_number_sending).get('amount')
    while count != 3:
        sending_money = input("Nhập số tiền cần chuyển :")
        if int(sending_money) > int(current_money):
            print("Tài khoản không đủ để thực hiện giao dịch")
            print("Xin mời nhập lại")
            count += 1
        else:
            print("-----xác nhận thông tin-------")
            print("Tên người nhận :", database.get(account_number_recieved).get('username'))
            print("Số tiền gửi là :", sending_money)
            change_money_people_received = int(database.get(account_number_recieved).get('amount')) + int(sending_money)
            update_money_to_database(account_number_recieved, change_money_people_received)
            _change_money_people_sending = int(current_money) - int(sending_money)
            update_money_to_database(acount_number_sending, _change_money_people_sending)
            return True
    return False


def change_password(acount_number):
    password_current = database.get(acount_number).get('password')
    count = 0
    while count < 3:
        print("==================================================")
        pass_current_input = input("Nhập mật khẩu hiện tại của bạn :")
        if pass_current_input == password_current:
            check_pass = 0
            if check_pass > 3:
                return False
            new_password = input("Nhập mật khẩu mới :")
            new_password_check = input("Xác nhận mật khẩu mới :")
            if new_password == new_password_check:
                # update_password_to_database(acount_number, new_password)
                update_pass_to_database(acount_number, new_password)
                print("Đổi mật khẩu thành công")
                print("Đăng nhập lại để sử dụng dịch vụ")
                return True
            else:
                print("Mật khẩu mới không trùng nhau")
                check_pass += 1
        else:
            print("Mật khẩu không đúng, vui lòng nhập lại!")
            count += 1
    return False


def menu_back():
    print("-------------------")
    print("1. Giao dịch khác")
    print("0. Thoát")
    input_return_main_menu = int(input("nhập lựa chọn cửa bạn :"))
    return input_return_main_menu


def main_menu(acountnumber_input):
    while True:
        print("=====MENU=====")
        print("1.Kiểm tra số dư")
        print("2.Rút tiền")
        print("3.Chuyển khoản")
        print("4.Đổi mật khẩu")
        print("0.Thoát")
        input_choose_main_menu = int(input("nhập lựa chọn của bạn:"))
        if input_choose_main_menu == 1:
            display_check_monney(acountnumber_input)
            input_return_main_menu = menu_back()
            if input_return_main_menu == 0:
                break
        elif input_choose_main_menu == 2:
            if not cash_out(acountnumber_input):
                sys.exit()
            input_return_main_menu = menu_back()
            if input_return_main_menu == 0:
                break
        elif input_choose_main_menu == 3:
            if not transfer_money(acountnumber_input):
                sys.exit()
            input_return_main_menu = menu_back()
            if input_return_main_menu == 0:
                break
        elif input_choose_main_menu == 4:
            if not change_password(acountnumber_input):
                sys.exit()
            break
        elif input_choose_main_menu == 0:
            sys.exit()


def routing():
    print("1. Login")
    print("0. Exit")
    input_choose_login = int(input("Nhập lựa chọn của bạn:"))
    if input_choose_login == 1:
        check_login = 0
        while check_login != 3:
            print("==========Xin mời đăng nhập=============")
            acountnumber_input = input("Nhap so tai khoan :")
            password_input = input("Nhap mat khau :")
            if check_user_pass_input(acountnumber_input, password_input):
                main_menu(acountnumber_input)
            else:
                print("----sai thông tin đăng nhập, xin mời nhập lại----")
                check_login += 1

        print("=========================================================")
        print(
            "Ngân hàng tạm thời giữ thẻ do bạn nhập sai mật khẩu 3 lần."
            "Vui lòng liên hệ nhân viên ngân hàng để được hỗ trợ")
    elif input_choose_login == 0:
        exit()


database = {}
read_database()
routing()
