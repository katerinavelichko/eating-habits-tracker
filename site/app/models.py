from . import db


class Users(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer)
    name = db.Column(db.String(50))
    email = db.Column(db.String(120))
    password = db.Column(db.String(120))

    @classmethod
    def add_user(cls, name, email, password):
        user = cls(name=name, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        print(f'Добавлен новый пользователь: {name}')

    @classmethod
    def delete_user(cls, name, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            db.session.delete(user)
            db.session.commit()
            print(f'Пользователь {name} был удален')
        else:
            print(f'Пользователя {name} нет в списках')
