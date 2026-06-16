import psycopg2


class PgManager:
    def __init__(self, db_name, user, password, host, port=5432):
        self.db_name= db_name
        self.user= user
        self.password = password
        self.host = host
        self.port = port
        
        self.connection = self.create_connection()
        if self.connection:
            print("Connected to database!")
            self.cursor = self.connection.cursor()

        
    def create_connection(self):
        try:
            connection = psycopg2.connect(
	            dbname=self.db_name,
	            user=self.user,
	            password=self.password,
	            host=self.host,
	            port=self.port,
            )
            return connection
        except Exception as error:
            print("Error connecting to the database:", error)
            return None
        

    def close_connection(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()
        print("Connection closed")


    def execute_query(self, query, *args):
        self.cursor.execute(query, args)
        self.connection.commit()


        #Confirmamos si el query devuelve algo o no 
        #En caso de devolver algo lo recuperamos y lo retornamos. Ex: SELECT
        #Y si no, solo se ejecuta el query pero sin devolver nada. Ex: INSERT
        if self.cursor.description:
            result = self.cursor.fetchall()
            return result
        
