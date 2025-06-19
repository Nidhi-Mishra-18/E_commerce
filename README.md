# 🛒 E-Commerce Backend API using FastAPI

A robust, secure, and maintainable **backend RESTful API** for an e-commerce platform, built using **FastAPI**. This system enables **admin** product management and **customer** operations like authentication, product browsing, shopping cart, and order history — all accessible via **Postman**.

---

## 📌 1. Introduction

### 1.1 Objective
Develop a RESTful API backend with the following core features:

- 🔐 User Authentication (Sign-up, Sign-in, Forgot/Reset Password)
- ⚙️ Admin Product Management (CRUD)
- 🔍 Product Browsing (Filters, Search, Detail View)
- 🛒 Shopping Cart
- 💳 Dummy Checkout
- 📦 Order History and Order Details

### 1.2 Scope
- Backend-only (No frontend)
- API can be tested using **Postman** or any REST client.
- JWT-based authentication with **role-based access**.

### 1.3 Prerequisites
- Python 3.9+
- FastAPI + SQLAlchemy
- Postman for API testing
- Basic knowledge of REST APIs

---

## ✅ 2. Functional Requirements

### 2.1 Authentication and User Management

- **User Signup**
  - `POST /auth/signup`
  - Fields: `name`, `email`, `password`, `role`
  - Email must be unique, password should be hashed

- **User Signin**
  - `POST /auth/signin`
  - Returns **JWT access** and **refresh tokens**

- **Forgot Password**
  - `POST /auth/forgot-password`
  - Sends reset link/token via email

- **Reset Password**
  - `POST /auth/reset-password`
  - Validates token and sets new password

- **Roles**
  - `admin`, `user`
  - Enforced using **RBAC (Role-Based Access Control)**

---

### 2.2 Admin Product Management (CRUD)

- `POST /admin/products` – Create product *(Admin only)*
- `GET /admin/products` – List products (pagination supported)
- `GET /admin/products/{id}` – Get product by ID
- `PUT /admin/products/{id}` – Update product
- `DELETE /admin/products/{id}` – Delete product

---

### 2.3 Public Product APIs

- `GET /products` – List with filters:  
  `category`, `min_price`, `max_price`, `sort_by`, `page`, `page_size`
- `GET /products/search` – Search by keyword
- `GET /products/{id}` – Product detail

---

### 2.4 Cart Management (User only)

- `POST /cart` – Add item (Fields: `product_id`, `quantity`)
- `GET /cart` – View cart
- `PUT /cart/{product_id}` – Update quantity
- `DELETE /cart/{product_id}` – Remove from cart

---

### 2.5 Checkout (User only)

- `POST /checkout`  
  - Mocks payment
  - Creates order
  - Clears cart after success

---

### 2.6 Orders and Order History (User only)

- `GET /orders` – View all past orders
- `GET /orders/{order_id}` – View details of a specific order  
  Includes product name, quantity, subtotal


## ⚙️ Technologies Used

- [FastAPI](https://fastapi.tiangolo.com/) 🚀
- [SQLAlchemy](https://www.sqlalchemy.org/) – ORM
- [Pydantic](https://pydantic-docs.helpmanual.io/) – Schema validation
- JWT (JSON Web Tokens) – Secure auth
- SQLite / PostgreSQL – Database (configurable)
- Postman – API testing

---

## 🚀 Getting Started

```bash
# Install dependencies
pip install -r requirements.txt

# Run the FastAPI app
uvicorn app.main:app --reload
