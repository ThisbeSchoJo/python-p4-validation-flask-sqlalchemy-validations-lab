from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import validates
db = SQLAlchemy()

class Author(db.Model):
    __tablename__ = 'authors'
    
    id = db.Column(db.Integer, primary_key=True)
    name= db.Column(db.String, unique=True, nullable=False)
    phone_number = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators 
    # All authors have a name
    # No two authors have the same name
    # Author phone numbers are exactly 10 digits
    @validates('name')
    def validates_name(self, key, name):
        existing_author = db.session.query(Author).filter(Author.name == name).first()
        if not name or (existing_author):
            raise ValueError("Each record must have a name and no two authors can have the same name!")
        return name



    @validates('phone_number')
    def validate_phone_number(self, key, phone_number):
        if not phone_number.isdigit() or len(phone_number) != 10:
            raise ValueError("Phone number must be exactly 10 digits.")
        return phone_number


    def __repr__(self):
        return f'Author(id={self.id}, name={self.name})'

class Post(db.Model):
    __tablename__ = 'posts'
    
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    content = db.Column(db.String)
    category = db.Column(db.String)
    summary = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    # Add validators  
    # Post content is at least 250 characters long
    # Post summary is a max of 250 characters
    # Post category is either Fiction or Non-Fiction
    # Post title is sufficiently clickbait-y and must contain one of the following:
    # "Won't Believe", "Secret", "Top", "Guess"
    @validates('content')
    def validate_content(self, key, content):
        if len(content) < 250:
            raise ValueError("Post content must be at least 250 characters long.")
        return content

    @validates('summary')
    def validate_summary(self, key, summary):
        if len(summary) > 250:
            raise ValueError("Post summary cannot exceed 250 characters.")
        return summary
    
    @validates('category')
    def validate_category(self, key, category):
        if category != "Fiction" and category !="Non-Fiction":
            raise ValueError("Category must be either Fiction or Non-Fiction.")
        return category
    
    @validates('title')
    def validate_title(self, key, title):
        clickbait_phrases = ["Won't Believe", "Secret", "Top", "Guess"]
        if not any(phrase in title for phrase in clickbait_phrases):
            raise ValueError("Title must be clickbait-y")
        return title

    def __repr__(self):
        return f'Post(id={self.id}, title={self.title} content={self.content}, summary={self.summary})'
