# - sqlalchemy — el nucleo: tipos de columnas (String, Integer), create_engine, ForeignKey, etc. 
#   Todo lo relacionado a la DB directamente.
# - sqlalchemy.orm — la capa de objetos: DeclarativeBase, Mapped, mapped_column, relationship, etc. 
#   Todo lo relacionado a mapear clases Python a tablas.
# Se puede ver así: sqlalchemy habla con la DB, sqlalchemy.orm habla con mis clases Python.
from sqlalchemy.orm import DeclarativeBase

# Funciones de Base:
# 1. Registro — cada clase que hereda de Base queda registrada en un catalogo interno que SQLAlchemy 
# mantiene. Ese catalogo se llama metadata y contiene la informacion de todas las tablas.

# 2. Creación de tablas — cuando se haga Base.metadata.create_all(engine), SQLAlchemy 
# recorre ese catalogo y crea todas las tablas en la DB de una vez.

# 3. Se podria decir que Base es el puente entre las clases Python y la DB. Sin ella, SQLAlchemy no 
# sabria que tablas crear ni como mapearlas.

# Analogia:
# Base es como el registro civil de un pais.
# Cada vez que nace una persona (User, Car, Address), se registra ahi. El registro civil no sabe que 
# hace cada persona,pero sabe que existen y tiene su informacion basica.
# Cuando el gobierno necesita hacer un censo (create_all), no va casa por casa buscando personas — 
# simplemente le pregunta al registro civil y este le devuelve la lista completa.
# Si una persona nunca se registro (no hereda de Base), para el gobierno no existe — 
# aunque uno la vea en el codigo.


# DeclarativeBase es la clase de SQLAlchemy que permite definir los modelos de forma declarativa — 
# es decir, usando clases Python con atributos en lugar de construir tablas manualmente.

# Cuando se utiliza class Base(DeclarativeBase), estoy creando mi propio sistema de registro 
# (el "registro civil" de la analogía). DeclarativeBase le da a Base toda la maquinaria interna para:

# -Leer los __tablename__ y columnas de cada clase hija
# -Mantener el metadata con todas las tablas registradas
# -Saber como traducir las clases a SQL


class Base(DeclarativeBase):
    #Con esto le digo a sqlalquemy que Base no es una tabla real, si no una clase padre.
    #Con la version moderna de DeclarativeBase, SQLAlchemy no se confune pero es buena practica agregarlo
    __abstract__ = True

    #Le indico el schema que vamos a usar a sqlalchemy
    __table_args__ = {"schema": "lyfter_ORM_exercise"}

