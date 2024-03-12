from app import app, db
from constants import PORT

if __name__ == "__main__":
    db.create_all()
    app.debug = True
    app.run(debug=True, port=PORT)