from app import create_app, db

app = create_app()

# Add these two lines right here!
with app.app_context():
    db.create_all()

if __name__ == "__main__":
    app.run(debug=True)