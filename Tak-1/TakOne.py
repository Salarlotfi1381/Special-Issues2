# متغیرهای سراسری
username = 'Admin'  # نام کاربری پیش‌فرض
pin = 1234  # پین پیش‌فرض
account_type = None  # نوع حساب
balance = None  # موجودی حساب

# تابع ورود به سیستم
def login():
    entered_username = input("Enter Username: ")
    
    # مدیریت ورودی نامعتبر برای PIN
    while True:
        try:
            entered_pin = int(input("Enter PIN: "))
            break
        except ValueError:
            print("Invalid input! Please enter a numeric PIN.")

    # بررسی نام کاربری و پین
    if entered_username == username and entered_pin == pin:
        print(f"Welcome Dear {entered_username}")
        show_main_menu()
    else:
        print("Invalid username or PIN!")
        show_login_menu()

# تابع نمایش منوی ورود
def show_login_menu():
    print("1. Login")
    print("2. Exit")
    choice = input("Enter Your Choice (1/2): ")
    if choice == '1':
        login()
    elif choice == '2':
        exit()
    else:
        print("Invalid choice!")
        show_login_menu()

# تابع نمایش منوی اصلی
def show_main_menu():
    global account_type, balance
    print("1. Open Account")
    print("2. Check Balance")
    print("3. Make Deposit")
    print("4. Withdraw Funds")
    print("5. Logout")
    choice = input("Enter Your Choice (1/2/3/4/5): ")
    
    if choice == '1':
        account_type, balance = open_account()
        show_main_menu()
    elif choice == '2':
        check_balance(account_type, balance)
        show_main_menu()
    elif choice == '3':
        balance = make_deposit(balance)
        show_main_menu()
    elif choice == '4':
        balance = withdraw_funds(balance)
        show_main_menu()
    elif choice == '5':
        print("Back to login .... ")
        show_login_menu()
    else:
        print("Invalid choice!")
        show_main_menu()

# تابع افتتاح حساب
def open_account():
    print("Choose account type:")
    print("1. Current Account")
    print("2. Savings Account")
    choice = input("Enter Your Choice (1/2): ")
    
    if choice == '1':
        account_type = 'Current'
        balance = 2000
        print("Current account opened successfully with balance of 2000!")
        return account_type, balance
    elif choice == '2':
        account_type = 'Savings'
        balance = 5000
        print("Savings account opened successfully with balance of 5000!")
        return account_type, balance
    else:
        print("Invalid account type! Please choose again.")
        return open_account()

# تابع بررسی موجودی حساب
def check_balance(account_type=None, balance=None):
    if account_type and balance is not None:
        print(f"Account Type: {account_type}, Balance: {balance}")
    else:
        print("No account found! Please open an account first.")

# تابع واریز وجه
def make_deposit(balance):
    if balance is not None:
        while True:
            try:
                amount = int(input("Enter amount to deposit: "))
                break
            except ValueError:
                print("Invalid input! Please enter a numeric value for the amount.")
        
        balance += amount
        print(f"{amount} deposited successfully. New Balance: {balance}")
    else:
        print("No account found! Please open an account first.")
    
    return balance

# تابع برداشت وجه
def withdraw_funds(balance):
    if balance is not None:
        while True:
            try:
                amount = int(input("Enter amount to withdraw: "))
                break
            except ValueError:
                print("Invalid input! Please enter a numeric value for the amount.")
        
        if amount <= balance:
            balance -= amount
            print(f"{amount} withdrawn successfully. New Balance: {balance}")
        else:
            print("Insufficient funds! Your balance is less than the requested amount.")
    else:
        print("No account found! Please open an account first.")
    
    return balance

# شروع برنامه از منوی ورود
show_login_menu()
