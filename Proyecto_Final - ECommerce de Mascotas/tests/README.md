# Tests

## Requisitos previos

- PostgreSQL corriendo y accesible según `DATABASE_URL` en tu `.env`.
- Redis corriendo y accesible según `REDIS_URL` en tu `.env`.
- Dependencias instaladas: `pip install -r requirements.txt`.

## Cómo correr los tests

Desde la raíz del proyecto:

```
pytest tests/ -v
```
