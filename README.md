
# **Jaiva – Complete E-commerce Shop**  

Jaiva is a **fully functional e-commerce platform** built with **Django and JavaScript**, providing a seamless shopping experience for both customers and administrators. It includes features like product management, order processing, user authentication, and sales reporting.  

## **Features**  
- **User Authentication** – Secure login and registration system.  
- **Product Management** – Add, edit, and manage product inventory.  
- **Shopping Cart & Checkout** – Smooth order placement with a shopping cart.  
- **Order Tracking** – Users can track their order status.  
- **Admin Panel** – Manage orders, sales reports, and customer data.  
- **Blog Integration** – Includes a blog section for updates and promotions.  
- **Sales Reporting** – Year-wise and order-wise reports for admins.  

## **Tech Stack**  
- **Backend:** Django (Python)  
- **Frontend:** HTML, CSS, JavaScript  
- **Database:** PostgreSQL / SQLite  
- **Deployment:** Nginx, Gunicorn  
- **Version Control:** Git & GitHub  

## **Installation**  

1. Clone the repository:  
   ```bash
   git clone https://github.com/bannawandoor27/Jaiva-complete-Ecommerce-shop.git
   cd Jaiva-complete-Ecommerce-shop
   ```  

2. Create a virtual environment and install dependencies:  
   ```bash
   python -m venv env
   source env/bin/activate  # On Windows use `env\Scripts\activate`
   pip install -r requirements.txt
   ```  

3. Apply migrations:  
   ```bash
   python manage.py migrate
   ```  

4. Create a superuser (for admin access):  
   ```bash
   python manage.py createsuperuser
   ```  

5. Run the development server:  
   ```bash
   python manage.py runserver
   ```  

6. Access the site at `http://127.0.0.1:8000/`  

## **Usage**  
- Admin Panel: `http://127.0.0.1:8000/admin/`  
- Storefront: Browse and purchase products.  

## **Contributing**  
Pull requests are welcome! Feel free to **fork the repository** and submit improvements.  

## **License**  
This project is **MIT licensed**.  

