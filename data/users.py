import datetime
import sqlalchemy
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase):
    __tablename__ = 'martians'
    # id (Integer, primary_key, autoincrement)
    id = sqlalchemy.Column(sqlalchemy.Integer,
                           primary_key=True,
                           autoincrement=True)
    # surname (String) (фамилия)
    surname = sqlalchemy.Column(sqlalchemy.String,
                                nullable=True)
    # name (String) (имя)
    name = sqlalchemy.Column(sqlalchemy.String,
                             nullable=True)
    # age (Integer) (возраст)
    age = sqlalchemy.Column(sqlalchemy.Integer,
                            nullable=True)
    # position (String) (должность)
    position = sqlalchemy.Column(sqlalchemy.String,
                                 nullable=True)
    # speciality (String) (профессия)
    specialty = sqlalchemy.Column(sqlalchemy.String,
                                  nullable=True)
    # address (String) (адрес)
    address = sqlalchemy.Column(sqlalchemy.String,
                                nullable=True)
    # email (String, unique) (электронная почта)
    email = sqlalchemy.Column(sqlalchemy.String,
                              unique=True)
    # hashed_password (String) (хэшированный пароль)
    hashed_password = sqlalchemy.Column(sqlalchemy.String,
                                        nullable=True)
    # modified_date (DateTime) (дата изменения)
    modified_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                      default=datetime.datetime.now)

    def __repr__(self):
        return f"<Colonist> {self.id} {self.surname} {self.name}"
