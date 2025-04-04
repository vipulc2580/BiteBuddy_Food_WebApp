# BiteBuddy Food WebApp

![BiteBuddy Banner](https://github.com/vipulc2580/BiteBuddy_Food_WebApp/blob/main/static/assets/extra-images/main-logo1.png)  
*An innovative food ordering platform that connects hungry customers with their favorite local vendors.*

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation & Setup](#installation--setup)
- [Usage](#usage)
- [Acknowledgements](#acknowledgements)

## Introduction

BiteBuddy Food WebApp is a comprehensive food ordering platform designed to offer a seamless experience for customers looking for a quick meal and vendors who wish to reach a broader audience. The project leverages modern web technologies to provide a responsive, user-friendly interface along with robust backend functionality.

## Features

- **User Authentication & Authorization**  
  Secure user registration, login, password reset, and profile management.
  
- **Dynamic Food Menu**  
  Display an extensive list of food items with detailed descriptions, images, and prices.
  
- **Cart Management**  
  Easily add, remove, and update items in the shopping cart with real-time feedback.
  
- **Vendor Management**  
  Vendors have dedicated pages showcasing their specialties, ratings, and detailed information.
  
- **Order Summary & Checkout**  
  A streamlined checkout process with order summaries, tax calculations, and total pricing.

- **Admin Dashboard**  
  Manage orders, users, vendors, and food items from a centralized dashboard.
  
- **Real-time Notifications**  
  Stay updated with order status and promotions through real-time alerts and notifications.

## Technologies Used

- **Backend:** Python, Django  
- **Frontend:** HTML5, CSS3, JavaScript, Bootstrap  
- **Database:** SQLite / MySQL (configurable)  
- **Others:** jQuery, AJAX, RESTful APIs

## Installation & Setup

1. **Clone the repository:**

   ```bash
       git clone https://github.com/vipulc2580/BiteBuddy_Food_WebApp.git
       cd BiteBuddy_Food_WebApp
   ```

2. **Create and activate a virtual environment:**

  ```bash
        python -m venv env
        source env/bin/activate    # On Windows use: env\Scripts\activate
  ```

3. **Install the dependencies:**
   ```bash
       pip install -r requirements.txt
   ```
   
4. **Apply migrations:**
   ```bash
       python manage.py makemigrations
       python manage.py migrate
   ```
   
5. **Create a superuser (optional, for admin access):**
    ```bash
      python manage.py createsuperuser
    ```
    
6. **Run the development server:**
    ```bash
        python manage.py runserver
    ```

7. **Access the application:**
    Open your browser and navigate to http://127.0.0.1:8000


## 🚀 Usage

### 👨‍🍳 User Journey:
- Users can sign up, browse through a curated list of food items.
- Add items to cart, review them, and proceed to checkout.

### 🛍️ Vendor Interaction:
- Each vendor has their own page with menu listings.
- Vendors can update menus and track incoming orders.

### 🛡️ Admin Panel:
- A secure admin dashboard for managing users, vendors, and orders.

---
## 🙏 Acknowledgements

Inspired by real-world food delivery apps.

Thanks to Django, Bootstrap, and all supporting open-source libraries.

Gratitude to contributors and the amazing open-source community! 💚
