from db_connection import PgManager

def format_user(user_record):
    return{
        "id": user_record[0],
        "full_name": user_record[1],
        "email": user_record[2],
        "password": user_record[3],
    }

db_manager = PgManager(
    db_name="postgres",
    user="postgres",
    password="Estudiar1234",
    host="localhost"
)

results = db_manager.execute_query("SELECT * FROM lyfter_duad.users;")
formatted_results = [format_user(result) for result in results]
print(formatted_results)

db_manager.close_connection()