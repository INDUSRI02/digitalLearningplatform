# Digital Learning Platform for Rural School Students in Nabha

## Project Overview

The **Digital Learning Platform for Rural School Students in Nabha** is a full-stack web application developed to improve access to structured digital education for rural students.

Many rural schools face issues such as fragmented learning resources, language barriers, lack of structured assessments, and minimal digital monitoring by teachers. This platform provides a centralized system where administrators, instructors, and students interact through dedicated portals to manage learning resources, tasks, and academic performance.

The system is built using the **Django framework** and follows a **role-based architecture** to ensure proper access control and workflow management.

---

## Problem Statement

Rural school students often lack organized digital learning systems. Existing platforms are usually complex, urban-focused, or lack features such as bilingual support and performance tracking suitable for rural environments.

This project addresses these challenges by providing:

* Structured learning modules
* Teacher-driven curriculum design
* Student performance tracking
* Administrative monitoring and analytics
* Lightweight user interface suitable for low-end devices

---

## Solution Provided

The platform provides a **complete digital learning ecosystem** including:

* Admin, Instructor, and Student portals
* Curriculum and course management
* Assessment bank for question management
* Time management system for task assignments
* Student performance tracking
* Feedback system with sentiment analysis
* Analytics dashboard for administrators

The system is fully functional and designed as a **production-style academic system rather than a prototype**. 

---

# System Architecture

The system follows the **Django MVT (Model-View-Template) architecture**.

Frontend (HTML + CSS + JavaScript)
↓
Django Templates & Views
↓
Business Logic Layer
↓
Database (Users, Courses, Assessments, Tasks)
↓
Analytics & Reporting Views

This architecture ensures modular design, scalability, and maintainability.

---

# Modules of the System

## 1. Admin Module

The administrator manages the entire platform.

Features:

* Manage students and instructors
* Monitor system activities
* View analytics and reports
* Manage feedback and system performance

---

## 2. Instructor Module

Instructors are responsible for designing course content and evaluating students.

Features:

* Curriculum creation and topic management
* Upload learning materials
* Create assessments
* Assign tasks and deadlines
* Track student performance

---

## 3. Student Module

Students interact with the learning platform through the student portal.

Features:

* Student dashboard
* View assigned tasks
* Access learning materials
* Submit feedback
* Update profile information

---

## 4. Assessment Bank

The platform includes a centralized question management system.

Features:

* Add and manage questions
* Create assessments
* Maintain question database
* Faculty-only access

---

## 5. Enrollment Lab

This module tracks student enrollment across courses.

Features:

* Scholar directory
* Course-wise student distribution
* Enrollment monitoring

---

## 6. Time Management System

This module helps students maintain discipline and track academic tasks.

Features:

* Create performance milestones
* Assign tasks with deadlines
* Task completion tracking
* Completion analytics

---

## 7. Feedback and Sentiment Monitoring

Students can submit feedback about courses and the platform.

Features:

* Feedback submission
* Sentiment classification
* Visualization of satisfaction trends

---

# Machine Learning Component

The project integrates **Machine Learning for feedback sentiment analysis**.

The ML component processes student feedback and automatically classifies it into:

* Positive
* Neutral
* Negative

This helps administrators understand student satisfaction and detect issues early. 

### ML Workflow

Student submits feedback
↓
Feedback stored in database
↓
Text preprocessing
↓
Feature extraction (Bag-of-Words / term frequency)
↓
Sentiment classification
↓
Results displayed in admin analytics dashboard

This automation reduces the need for manual analysis of feedback.

---

# Technology Stack

## Frontend

* HTML5
* CSS
* JavaScript
* Django Templates

## Backend

* Python
* Django Framework

## Database

* SQLite (Django ORM managed)

## Development Tools

* Visual Studio Code
* Git & GitHub

---

# Installation and Setup

### Step 1: Clone the Repository

```bash
git clone https://github.com/yourusername/Digital-Learning-Platform-for-Rural-School.git
```

### Step 2: Navigate to Project Folder

```bash
cd Digital-Learning-Platform-for-Rural-School
```

### Step 3: Install Dependencies

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

### Step 6: Open the Application

```
http://127.0.0.1:8000
```

---

# Project Workflow

1. Admin initializes the platform
2. Instructors create curriculum and assessments
3. Students enroll in courses
4. Tasks and assignments are assigned
5. Students complete tasks and submit feedback
6. System records performance and analytics
7. Admin reviews results and platform insights

---

# Future Enhancements

* Mobile application integration
* Video lecture streaming
* AI-based learning recommendations
* Advanced student performance prediction
* Adaptive learning modules

---

# Conclusion

The **Digital Learning Platform for Rural School Students in Nabha** provides a structured and scalable solution for digital education in rural areas. By integrating course management, assessments, analytics, and machine learning-based feedback analysis, the platform enables better learning experiences and improved academic monitoring.

---

# Author

Developed as part of an academic project submission
