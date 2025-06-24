# 🧾 Smart Ration Distribution Ticketing System

A Django-based web application that streamlines the process of ration distribution by allowing registered suppliers to create daily distribution sessions and users to book tokens online using their ration card numbers. The system also features real-time QR code generation, token status tracking, and efficient session management.

---

## 📌 Features

- 👤 **Supplier Registration & Login**
- 🗓️ **Create and Manage Daily Distribution Sessions**
- 🧾 **User Token Booking via Ration Card**
- 🎫 **QR Code Based Booking Access**
- 📊 **Track Token Status in Real-time**
- ✅ **Update Ticket Status & Auto-Move to Next Token**
- 🧑‍💼 **Supplier Profile Management**

---

## 🏗️ Project Structure

```bash
srdts/
├── smart_ration_ticket/
│   ├── migrations/
│   ├── admin.py/
│   ├── apps.py/
│   ├── models.py
│   ├── views.py
│   ├── urls.py
│   ├── tests.py
├── core/        
│   ├── settings.py
│   ├── urls.py
|   ├── wsgi.py
|   ├── asgi.py
├──templates/core/ .. all templates
├── db.sqlite3
├── manage.py
├── README.md
````

---

## ⚙️ Installation & Setup

### 1. Clone the Repository

```bash
git clone https://github.com/LE0-MAhendra/Smart-Ration-Distibution-Ticketing-System
cd srdts
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Start Development Server

```bash
python manage.py runserver
```

Now visit: `http://127.0.0.1:8000`

---

## 🧪 Running Tests

```bash
python manage.py test
```

* Uses Django's built-in `TestCase` framework.
* Tests models, authentication, views, and booking workflows.
* Runs on a **temporary SQLite test database** (doesn't affect production data).

---

## ✅ Modules Overview

### 👨‍💼 Supplier Dashboard

* Login-based access
* Daily session creation
* Live QR code for users to scan and book
* Track current token
* Manually update ticket status

### 👨‍👩‍👦 User Booking System

* Book token using ration card number
* View token number and estimated wait time
* Prevent duplicate bookings per day
* Error messages for full sessions

---

## 🧠 Technologies Used

* **Backend**: Django (Python)
* **Frontend**: HTML5, CSS3, Django Templating
* **Database**: SQLite (default)
* **QR Code Generation**: Python `qrcode` + `Pillow`
* **Session Handling**: Django Authentication & ORM
* **Testing**: Django `TestCase`

---

## 🔐 Security & Access Control

* `@login_required` used for supplier views
* CSRF protection for form submissions
* Limited access based on user type (supplier vs. public user)
* QR code access is session-specific and date-restricted

---

## 📸 Screenshots

![Screenshot 2025-06-21 214451](https://github.com/user-attachments/assets/4cd92964-06f1-4b1c-9680-f025c23ed81d)
![Screenshot 2025-06-21 213954](https://github.com/user-attachments/assets/b7b5daf9-2397-4a56-8b5a-d34d590e1e44)
![Screenshot 2025-06-21 213937](https://github.com/user-attachments/assets/3a876812-7783-40b7-9937-085b671b6856)
![Screenshot 2025-06-21 213911](https://github.com/user-attachments/assets/6658fb33-ce7c-41cc-890b-5509224a5039)
![Screenshot 2025-06-21 213858](https://github.com/user-attachments/assets/06da2c50-6d13-417c-bbf5-f11d9be85923)
![Screenshot 2025-06-21 213843](https://github.com/user-attachments/assets/0dd99a16-b671-4c92-8a47-c580ad0a47eb)
![Screenshot 2025-06-21 213741](https://github.com/user-attachments/assets/611f375c-edb6-4771-8e34-c65c5a2a8e0b)
![Screenshot 2025-06-21 213721](https://github.com/user-attachments/assets/de9dc103-c84a-421b-aa4f-84732b705880)

---

## 📝 Future Enhancements

* Add OTP verification for booking
* Admin panel for supplier approval
* Session analytics and reporting
* Support for multi-language and SMS alerts


---

## 🙋‍♂️ Author

**Mahender Kurikyala**
Full Stack Developer
📧 [mahender.kurikyala11@gmail.com](mailto:mahender.kurikyala11@gmail.com)
🔗 [LinkedIn](https://www.linkedin.com/in/leo-mahendra)

```

