import re


def check_name(name):

    words = re.split(r'\s+', name.strip())
    if len(name) > 30:
        print("نام وارد شده بیش از ۳۰ کاراکتر است. لطفاً نامی کوتاه‌تر وارد کنید.")
        return False

    if len(words) > 6:
        print("نام وارد شده شامل بیش از ۶ کلمه است. لطفاً نامی با تعداد کلمات کمتر وارد کنید.")
        return False

    if not re.fullmatch(r'[a-zA-Z\s]+', name):
        print("نام باید فقط شامل حروف انگلیسی باشد و نمی‌تواند شامل اعداد یا کاراکترهای خاص باشد.")
        return False

    return True


def check_birth_date(birth_date):

    pattern_sep = r'^(?!.*-.*\/|.*\/.*-).*'
    if not re.search(pattern_sep, birth_date):
        print(
            "تاریخ وارد شده شامل ترکیب غیرمجاز جداکننده‌ها ('-' و '/') است. لطفاً فقط از یک نوع جداکننده استفاده کنید.")
        return False


    pattern = r'^\d{1,4}[-/]\d{1,2}[-/]\d{1,4}$'
    match = re.search(pattern, birth_date)

    if not match:
        print("تاریخ تولد باید به فرمت d-m-yyyy، yyyy-m-d یا yyyy/m/d وارد شود. لطفاً فرمت صحیح را رعایت کنید.")
        return False


    parts = list(map(int, re.findall(r'\d+', birth_date)))


    if parts[0] > 31:
        year, month, day = parts
    elif parts[2] > 31:
        day, month, year = parts
    else:
        print("ترتیب نامعتبر برای تاریخ تولد. لطفاً فرمت صحیح را رعایت کنید.")
        return False


    if not (1 <= day <= 31):
        print("روز وارد شده نامعتبر است. لطفاً عددی بین ۱ تا ۳۱ وارد کنید.")
        return False


    if not (1 <= month <= 12):
        print("ماه وارد شده نامعتبر است. لطفاً عددی بین ۱ تا ۱۲ وارد کنید.")
        return False



    if not (1200 <= year <= 1403 or 1900 <= year <= 2024):
        print("سال وارد شده نامعتبر است. لطفاً عددی بین ۱۹۰۰ تا ۲۰۲۴ یا ۱۲۰۰ تا ۱۴۰۳ وارد کنید.")
        return False

    return True
def check_email(email):

    pattern = r'^[a-zA-Z0-9_-]{5,}@[a-zA-Z]+(\.[a-zA-Z]+)+$'
    if not re.search(pattern, email):
        print("ایمیل وارد شده نامعتبر است.")
        print("آیدی ایمیل باید حداقل ۵ کاراکتر شامل حروف، ارقام یا خط تیره باشد.")
        print("دامین ایمیل باید شامل حروف الفبایی باشد و حداقل یک نقطه داشته باشد (مثل example@example.com).")
        return False
    return True



def check_phone(phone):

    pattern = (
        r'^('
        r'0\d{2,3}[-\s]?\d{3,4}[-\s]?\d{4}'  
        r'|'
        r'\+\d{1,3}[-\s]?\d{1,4}[-\s]?\d{3,4}[-\s]?\d{4}'  
        r')$'
    )


    digits_only = re.sub(r'\D', '', phone)

    if not re.search(pattern, phone) or len(digits_only) < 11:
        print("شماره تلفن وارد شده نامعتبر است.")
        print("لطفاً شماره‌ای معتبر با یکی از فرمت‌های زیر وارد کنید:")
        print("- شماره‌های داخلی: مانند 0912-345-6789 یا 077-3428-4981")
        print("- شماره‌های بین‌المللی: مانند +98-77-3428-4981 یا +1-555-243-2354")
        return False

    return True


def check_username(username):

    if not re.search(r'^[a-zA-Z][a-zA-Z0-9_-]*$', username) or ' ' in username:
        print("نام کاربری باید با حرف شروع شود، فقط شامل حروف، اعداد، خط زیر (_) یا خط تیره (-) باشد و نباید شامل فاصله خالی باشد.")
        return False
    return True


def check_password(password, username):
    if len(password) < 8:
        print("کلمه عبور باید حداقل ۸ کاراکتر باشد. لطفاً کلمه عبور طولانی‌تری وارد کنید.")
        return False
    if username in password:
        print("کلمه عبور نباید شامل نام کاربری باشد. لطفاً کلمه عبوری متفاوت وارد کنید.")
        return False
    if not re.search(r'[A-Z]', password):
        print("کلمه عبور باید حداقل یک حرف بزرگ (مثل A) داشته باشد.")
        return False
    if not re.search(r'[a-z]', password):
        print("کلمه عبور باید حداقل یک حرف کوچک (مثل a) داشته باشد.")
        return False

    if not re.search(r'[0-9]', password):
        print("کلمه عبور باید حداقل یک عدد داشته باشد.")
        return False
    if not re.search(r'[&?*_%!\\$@]', password):
        print("کلمه عبور باید حداقل یک کاراکتر خاص (مثل @ یا !) داشته باشد.")
        return False
    return True


def validate_user_info(name=None, birth_date=None, email=None, phone=None, username=None, password=None):
    if not name:
        name = input("نام خود را وارد کنید: ")
    if not check_name(name):
        return None

    if not birth_date:
        birth_date = input("تاریخ تولد خود را وارد کنید (yyyy-mm-dd یا yyyy/mm/dd): ")
    if not check_birth_date(birth_date):
        return None

    if not email:
        email = input("ایمیل خود را وارد کنید: ")
    if not check_email(email):
        return None

    if not phone:
        phone = input("شماره تلفن خود را وارد کنید: ")
    if not check_phone(phone):
        return None

    if not username:
        username = input("نام کاربری خود را وارد کنید: ")
    if not check_username(username):
        return None

    if not password:
        password = input("کلمه عبور خود را وارد کنید: ")
    if not check_password(password, username):
        return None

    user_info = {
        "name": name,
        "birth_date": birth_date,
        "email": email,
        "phone": phone,
        "username": username,
        "password": password,
    }
    return user_info


if __name__ == "__main__":
    user_info = validate_user_info()
    if user_info:
        print("اطلاعات کاربر با موفقیت ثبت شد:")
        print(user_info)
    else:
        print("برخی از اطلاعات وارد شده نامعتبر بودند.")
