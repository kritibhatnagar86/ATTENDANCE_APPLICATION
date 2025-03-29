from app import app, db, Admin
from werkzeug.security import generate_password_hash

# Create an admin user
admin_id = "admin123"  # Change this as needed
password = "securepassword"  # Set your password
hashed_password = generate_password_hash(password)

with app.app_context():  # Ensure database access works correctly
    new_admin = Admin(admin_id=admin_id, password=hashed_password)
    db.session.add(new_admin)
    db.session.commit()
    print("✅ Admin added successfully!")
