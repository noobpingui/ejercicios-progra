#Service decide QUÉ hacer.
#Repository sabe CÓMO obtener o guardar los datos.      
#Pydantic responde una pregunta:
#¿Los datos tienen la forma correcta?
#Service responde otra:
#¿La operación tiene sentido para el negocio?
#Repository responde otra:
#¿Cómo obtengo o guardo los datos?
#Son tres problemas distintos.  

#-------------------------------------------------------

#ROUTE O CONTROLLER
#Aquí vive todo lo relacionado con HTTP.
#Por ejemplo: GET-POST-PUT-DELETE
request.get_json()
request.args.get()
jsonify()
status codes: 200-201-400-404

#-------------------------------------------------------

#SERVICE
#Aqui vive la logica de negocio
#Por ejemplo: 
def create_task(new_task):
def update_task(task_id, new_task):
#Aquí se responden preguntas como:
¿El ID ya existe?
¿La tarea puede actualizarse?
¿El usuario tiene permisos?
¿La operación es válida?

#-------------------------------------------------------

#REPOSITORY
#Aquí vive el acceso a datos.
#Por ejemplo:
repository.get_all()
repository.get_by_id()
repository.create()
repository.update()
repository.delete()
El Repository también tiene métodos CRUD.
Pero no son verbos HTTP.
Son operaciones de persistencia.

---o------o------o------o---
---o------o------o------o---
Una analogía sobre una biblioteca.
---o------o------o---
---o---ROUTE---o---
El recepcionista.

Recibe solicitudes.
Habla con la gente.
Devuelve respuestas.
---o------o------o---
---o---SERVICE---o---
El bibliotecario.

Decide si puedes sacar un libro.
Aplica las reglas.
---o------o------o---
---o---REPOSITORY---o---
El archivista.

Sabe dónde están guardados los libros.
Los busca.
Los guarda.
Los elimina.
---o------o------o------o---
---o------o------o------o---

Capa            -----------   Pregunta
Route           -----------   ¿Cómo llegó la petición?
Schema / DTO	-----------   ¿Los datos tienen la forma correcta?
Service	        -----------   ¿La operación tiene sentido para el negocio?
Repository	    -----------   ¿Cómo obtengo o guardo los datos?

---o------o------o------o---
---o------o------o------o---

Route
    ↓
Schema / DTO (Pydantic)
    ↓
Service
    ↓
    depende de
TaskRepository (contrato)
    ↓
JsonTaskRepository
o
PostgresTaskRepository
o
FakeTaskRepository


FLUJO COMPLETO:

  Request HTTP
      → Route        (recibe el request, extrae datos)
          → Service  (aplica reglas de negocio)
              → Repository (ejecuta SQL)
                  → PostgreSQL
              ← Repository (devuelve dict)
          ← Service  (devuelve resultado)
      ← Route        (construye response HTTP)
  Response HTTP


Lo realizado:
    
    - Arquitectura en capas limpia: Routes → Services → Repositories → DB
    - Dependency injection con blueprint factory pattern
    - Validacion con Pydantic en la capa HTTP
    - Excepciones de dominio por capa
    - SQL dinamico con whitelist para prevenir SQL injection
    - Reglas de negocio coordinadas entre multiples repositorios (RentalService)