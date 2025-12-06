# Shopsphere – E-commerce Product API

**A RESTful E-commerce Product API built with Django and Django REST Framework.**  
Shopsphere provides backend functionality for managing products on an e-commerce platform, including user authentication, product CRUD operations, search, and filtering.

---

## Features

- **User Authentication:** Register, login, and JWT token-based authentication  
- **Product Management:** Create, read, update, and delete products  
- **Product Search:** Search products by name or category (supports partial matches)  
- **Filtering & Pagination:** Filter products by category, price range, and stock availability; pagination for large datasets  
- **Deployment-Ready:** Can be deployed on platforms like Heroku or PythonAnywhere  

---

## Tech Stack

- Python 3.x  
- Django 4.x  
- Django REST Framework  
- SQLite (default; can switch to Postgres for production)  
- Django Rest Framework 

---

## Models

- **User:** Handles authentication and management of users  
- **Category:** Organizes products by category
- **Product:** Stores product details such as name, description, price, stock quantity, image URL, and category  
- **Cart:** Represents a user’s shopping cart.
- **Orders:** Represents a completed purchase made by a user.

---

## API Endpoints

### Authentication
| Method | Endpoint | Description |
|--------|---------|-------------|
| POST | `/api/auth/register/` | Register a new user |
| POST | `/api/auth/login/` | Login and receive token |
| GET | `/api/auth/profile/` | Retrieve logged-in user profile |

### Products
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/products/` | List all products |
| GET | `/api/products/<id>/` | Retrieve product details |
| POST | `/api/products/` | Create a new product (auth required) |
| PUT | `/api/products/<id>/` | Update product (auth required) |
| DELETE | `/api/products/<id>/` | Delete product (auth required) |

### Categories
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/categories/` | List all categories |

### Cart
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/cart/` | Retrieve the logged-in user’s cart and items |
| POST | `/api/cart/add/` | Add a product to the cart (requires product ID and quantity) |
| PUT | `/api/cart/update/<cart_item_id>/` | Update quantity of a cart item |
| DELETE | `/api/cart/remove/<cart_item_id>/` | Remove a product from the cart |
| DELETE | `/api/cart/clear/` | Clear all items from the cart |

### Orders
| Method | Endpoint | Description |
|--------|---------|-------------|
| GET | `/api/orders/` | List all orders of the logged-in user |
| GET | `/api/orders/<id>/` | Retrieve details of a specific order |
| POST | `/api/orders/create/` | Create a new order from the user’s cart |
| PUT | `/api/orders/<id>/cancel/` | Cancel a pending order (optional) |



### Search & Filter
- `GET /api/products/?search=<keyword>` — Search products by name  
- `GET /api/products/?category=<category>&min_price=<min>&max_price=<max>` — Filter products by category, price range, or stock availability  


## Contact
If you want to get in touch, share feedback, or discuss anything about this project, feel free to reach out:

- **Email:** ugotachisomstephen@gmail.com  
- **WhatsApp:** +2348074625742

---
