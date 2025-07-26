# database.py
import os
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base

# 1. Define the database engine
# This will create a file named 'claim_forge.db' in the same directory

db_path = os.path.join(os.path.dirname(__file__), 'claim_forge.db')
DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(DATABASE_URL)

# 2. Declare a base for declarative models
Base = declarative_base()

# 3. Define your database model (Table)
class User(Base):
    __tablename__ = 'users' # Name of the table in the database

    id = Column(Integer, primary_key=True)
    username = Column(String, unique=True, nullable=False)
    email = Column(String, unique=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, username='{self.username}', email='{self.email}')>"

# 4. Create all tables defined in Base (if they don't exist)
# This connects to the database and issues CREATE TABLE statements
Base.metadata.create_all(engine)

# 5. Create a session factory
# SessionLocal will be a class that can be instantiated to get a database session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# --- Database Operations ---

def create_user(db_session, username: str, email: str):
    """Adds a new user to the database."""
    new_user = User(username=username, email=email)
    db_session.add(new_user)
    db_session.commit()
    db_session.refresh(new_user) # Refresh to get the generated ID
    print(f"Created user: {new_user}")
    return new_user

def get_user_by_username(db_session, username: str):
    """Retrieves a user by username."""
    user = db_session.query(User).filter(User.username == username).first()
    print(f"Found user by username '{username}': {user}")
    return user

def get_all_users(db_session):
    """Retrieves all users from the database."""
    users = db_session.query(User).all()
    print("All users:")
    for user in users:
        print(user)
    return users

def update_user_email(db_session, username: str, new_email: str):
    """Updates the email of an existing user."""
    user = db_session.query(User).filter(User.username == username).first()
    if user:
        user.email = new_email
        db_session.commit()
        db_session.refresh(user)
        print(f"Updated user: {user}")
        return user
    print(f"User with username '{username}' not found for update.")
    return None

def delete_user(db_session, username: str):
    """Deletes a user from the database."""
    user = db_session.query(User).filter(User.username == username).first()
    if user:
        db_session.delete(user)
        db_session.commit()
        print(f"Deleted user: {username}")
        return True
    print(f"User with username '{username}' not found for deletion.")
    return False

# --- Main execution block ---
if __name__ == "__main__":
    # Get a database session
    db = SessionLocal()
    try:
        print("--- Creating Users ---")
        user1 = create_user(db, "alice", "alice@example.com")
        user2 = create_user(db, "bob", "bob@example.com")
        user3 = create_user(db, "charlie", "charlie@example.com")
        # Try to create a user that already exists (will cause an error for unique constraint)
        try:
            create_user(db, "alice", "new_alice@example.com")
        except Exception as e:
            print(f"Error creating duplicate user: {e}")
            db.rollback() # Rollback the failed transaction


        print("\n--- Getting All Users ---")
        get_all_users(db)

        print("\n--- Getting a Specific User ---")
        get_user_by_username(db, "bob")

        print("\n--- Updating a User ---")
        update_user_email(db, "charlie", "charlie.updated@example.com")

        print("\n--- Getting All Users After Update ---")
        get_all_users(db)

        print("\n--- Deleting a User ---")
        delete_user(db, "alice")

        print("\n--- Getting All Users After Deletion ---")
        get_all_users(db)

    finally:
        # Always close the session to release resources
        db.close()
        print("\nDatabase session closed.")
