# Digital Learning Platform for Rural School

## Project Overview

The **Digital Learning Platform for Rural School** is a web-based learning management system designed to improve access to education in rural areas. The platform allows students to access study materials, instructors to upload courses and documents, and administrators to manage users and monitor system activities.

The system provides a centralized platform where learning resources can be easily shared and accessed, helping students continue their education through digital technology.

---

## Objectives

* Provide easy access to educational resources for rural students.
* Enable instructors to upload learning materials and manage courses.
* Allow administrators to manage students, instructors, and system activities.
* Improve digital learning accessibility through a simple web interface.

---

## System Modules

### 1. Admin Module

The administrator manages the entire system.

Functions:

* Manage students and instructors
* Approve instructor registrations
* View system dashboard
* Monitor courses and uploaded materials
* Remove users if required

### 2. Instructor Module

Instructors are responsible for teaching and uploading course content.

Functions:

* Upload study materials
* Manage courses
* View enrolled students
* Track student progress

### 3. Student Module

Students can access the learning platform and view course materials.

Functions:

* Register and login
* View available courses
* Access study materials
* Update profile information

---

## Technologies Used

### Frontend

* HTML
* CSS
* Bootstrap
* JavaScript

### Backend

* Python
* Django Framework

### Database

* SQLite3

### Other Tools

* Visual Studio Code
* GitHub for version control

---

## System Architecture

The project follows the **Model-View-Template (MVT)** architecture used by Django.

* **Model** – Handles database structure and data management.
* **View** – Contains the business logic.
* **Template** – Handles the user interface and presentation layer.

---

## Features

* User authentication (Login & Registration)
* Role-based access (Admin, Instructor, Student)
* Course and document management
* Multilingual support (English, Hindi, Telugu)
* Email notification system
* Profile management

---

## Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Digital-Learning-Platform-for-Rural-School.git
```

### Step 2: Navigate to Project Folder

```bash
cd Digital-Learning-Platform-for-Rural-School
```

### Step 3: Install Required Packages

```bash
pip install -r requirements.txt
```

### Step 4: Apply Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 5: Run the Server

```bash
python manage.py runserver
```

### Step 6: Open in Browser

```
http://127.0.0.1:8000/
```

---

## Folder Structure

```
Digital-Learning-Platform-for-Rural-School
│
├── adminapp
├── userapp
├── instructorapp
├── media
├── static
├── templates
├── db.sqlite3
├── manage.py
└── gameProject
```

---

## Future Enhancements

* Mobile application integration
* Video lecture streaming
* AI-based personalized learning recommendations
* Online examinations and automatic grading
* Advanced analytics dashboard

---

## Conclusion

The Digital Learning Platform for Rural School helps bridge the educational gap by providing a digital platform for learning. It enables students to access educational content easily while allowing instructors and administrators to efficiently manage courses and users.

---

## Author

Project developed as part of an academic project submission.

