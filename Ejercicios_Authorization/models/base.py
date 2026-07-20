from sqlalchemy.orm import DeclarativeBase



class Base(DeclarativeBase):
    #Con esto le digo a sqlalquemy que Base no es una tabla real, si no una clase padre.
    #Con la version moderna de DeclarativeBase, SQLAlchemy no se confunde pero es buena practica agregarlo
    __abstract__ = True

    #Le indico el schema que vamos a usar a sqlalchemy
    __table_args__ = {"schema": "lyfter_authentication_exercise"}