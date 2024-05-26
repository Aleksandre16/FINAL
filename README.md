# Library Management System using Django

This is a library management system developed using Django, aimed at facilitating the control of a library's book database and the process of issuing and returning books to users. The application allows library employees to manage the book inventory, while also enabling users to register on the website and utilize library services.

## Functionality

1. **User Registration**: Library employees can register on the site with mandatory fields including email, password, full name, personal number, and birth date. Employees can also be added to the site via the admin panel.

2. **Authorization**: Users, including employees and regular users, can authorize on the site to access its functionalities.

3. **Book Management**:
   - Librarians can add, delete, and modify books in the system.
   - The system supports fully managing content through both the Django admin interface and an API for conditional systems.
   - At least 1000 books are generated randomly and added to the system.
   - Each book includes the following data:
     - Title
     - Author
     - Genre
     - Publication Date
     - Stock Quantity
   - Additional functionalities include:
     - Connecting author data to the book model.
     - Establishing a genre-related connection.
     - Allowing users to reserve a book for 1 day if it's in stock, with automatic removal from the list upon checkout (implemented via ManagementCommand and API).

## Usage

To run the project locally, follow these steps:

1. Clone the repository:
   ```bash
   git clone https://github.com/Aleksandre16/FINAL
   ```

2. Navigate to the project directory:
   ```bash
   cd FINAL
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

4. Run migrations:
   ```bash
   python manage.py migrate
   ```

5. Create a superuser (to access the Django admin panel):
   ```bash
   python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   python manage.py runserver
   ```

7. Access the application at [http://localhost:8000/](http://localhost:8000/) in your web browser.

