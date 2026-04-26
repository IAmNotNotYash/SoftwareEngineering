from app import create_app, db
from sqlalchemy import text
app = create_app()
with app.app_context():
    db.session.execute(text('ALTER TABLE posts ADD COLUMN IF NOT EXISTS views_count INTEGER DEFAULT 0'))
    db.session.commit()
    print("Database updated successfully.")
