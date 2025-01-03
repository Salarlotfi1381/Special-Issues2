
# سیستم مدیریت حساب بانکی با پایتون

## توضیحات کلی
این پروژه یک سیستم مدیریت حساب بانکی مبتنی بر کنسول است که با زبان پایتون پیاده‌سازی شده است. این برنامه عملیات بانکی ساده‌ای مانند ایجاد حساب، بررسی موجودی، واریز وجه و برداشت وجه را شبیه‌سازی می‌کند. این پروژه به‌عنوان تمرین دانشگاهی توسط دانشجو انجام شده است.

## قابلیت‌ها
1. **ورود و احراز هویت**: کاربران می‌توانند با نام کاربری و رمز عبور از پیش تعیین‌شده وارد سیستم شوند.
2. **عملیات حساب**:
   - **ایجاد حساب**: ایجاد یک حساب بانکی جدید با موجودی اولیه.
   - **بررسی موجودی**: مشاهده موجودی فعلی حساب.
   - **واریز وجه**: افزودن وجه به حساب.
   - **برداشت وجه**: برداشت وجه از حساب (با کنترل موجودی).
3. **مدیریت خطاها**: برنامه شامل مدیریت خطا برای ورودی‌های نامعتبر و عدم موجودی کافی است.

## نحوه استفاده
### منوی اصلی
بعد از ورود، منوی اصلی برای کاربر نمایش داده می‌شود:
1. **ایجاد حساب**
2. **بررسی موجودی**
3. **واریز وجه**
4. **برداشت وجه**
5. **خروج**

### جریان برنامه
1. کاربر با نام کاربری و رمز عبور وارد سیستم می‌شود.
2. منوی اصلی نمایش داده شده و کاربر می‌تواند یکی از عملیات‌ها را انتخاب کند.
3. هر گزینه در منو به یک عملیات بانکی مرتبط است:
   - ایجاد حساب
   - بررسی موجودی حساب
   - واریز وجه
   - برداشت وجه
4. برنامه زمانی به پایان می‌رسد که کاربر گزینه‌ی خروج را انتخاب کند.

### نمونه اجرای برنامه
پس از اجرا، برنامه رابط ورود را نمایش می‌دهد. بعد از ورود به سیستم، گزینه‌های منوی اصلی نمایش داده می‌شود و کاربر می‌تواند یک عملیات را انتخاب کند.

```plaintext
1. Open Account 
1. Check Balance 
1. Make Deposit 
1. Withdraw Funds 
1. Logout 

Enter Your Choice (1/2/3/4/5): _
```

## نیازمندی‌ها
- پایتون نسخه 3.x

## اجرای برنامه
1. مخزن را کلون کنید:
   ```bash
   https://github.com/Salarlotfi1381/Special-Issues2.git
   ```
2. به دایرکتوری پروژه بروید:
   ```bash
   cd Tak-1
   ```
3. برنامه را اجرا کنید:
   ```bash
   python TakOne.py
   ```

## نویسنده
این پروژه توسط سالار لطفی  به‌عنوان بخشی از یک تمرین درسی در دانشگاه انجام شده است.
