
--Session:-- 
Es el espacio de trabajo entre el codigo Python y la base de datos. Todo lo que se hace con objetos —
agregar, modificar, borrar — primero ocurre dentro de la session, y solo llega a la DB cuando se realiza un commit().

--Tiene tres responsabilidad:--
1. Rastrea cambios — si se modifica user.name, la sesión sabe que ese objeto cambió y que hay que actualizar en la DB.
2. Maneja transacciones — agrupa operaciones y las confirma juntas con commit(), o las deshace con rollback().
3. Actúa como caché local — si se pide el mismo user_id dos veces, la segunda vez no va a la DB, devuelve el objeto que ya tiene en memoria.

--Session en los repositories:--
Cuando en User/Car/AddressRepository se recibe db: Session, se esta recibiendo ese espacio de trabajo activo. El repositorio no crea ni cierra la session — solo la usa. Quien la crea y cierra es responsabilidad de afuera.

--Analogia:--
Es como el staging area de git:

  - git add → session.add()
  - git commit → session.commit()
  - git reset → session.rollback()

Los cambios estan registrados pero no son permanentes hasta que se hace commit().