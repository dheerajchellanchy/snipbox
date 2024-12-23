# SnipBox Documentation

**SnipBox** is a simple note-saving application that allows users to save, organize, and manage short notes.

## **Installation Steps**

Follow the steps below to set up and run the SnipBox application locally:

1. Clone the Repository:
   ```bash
   git https://github.com/dheerajchellanchy/snipbox.git
   ```
2. Set up a Virtual Environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```
3. Install Requirements:
   ```bash
   pip install -r requirements.txt
   ```
4. Migrate The changes into database:
   ```bash
   python manage.py migrate
   ```
5. Create a Superuser:
   ```bash
   python manage.py createsuperuser
   ```

6. Run the Server:
   ```bash
   python manage.py runserver
   ```
