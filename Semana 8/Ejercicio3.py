

# 1. Cree un programa que me permita ingresar información de n cantidad de videojuegos y los guarde en un archivo csv.
# Debe incluir:
# - Nombre
# - Género
# - Desarrollador
# - Clasificación ESRB

# Ejemplo de archivo final:

# nombre,genero,desarrollador,clasificacion
# Grand Theft Auto IV,Accion,Rockstar Games,M
# The Elder Scrolls IV: Oblivion,RPG,Bethesda,M
# Tony Hawk's Pro Skater 2,Deportes,Activision,T

import csv

def request_videogames():
    videogames_list = []
    while True:
        try:
            name = input("Enter the name of the videogame (or type 'exit' to finish): ")
            if name.lower() == 'exit':
                break
            genre = input("Enter the genre of the videogame: ")
            developer = input("Enter the videogame studio: ")
            esrb = input("Enter the ESRB of the videogame: ")
            videogame = {
                "Name": name,
                "Genre": genre,
                "Developer": developer,
                "ESRB": esrb
            }
            videogames_list.append(videogame)
        except Exception as e:
            print(f"Error: {e}")
    return videogames_list


def create_videogames_csv(file_path, data, headers):
    try:
        with open(file_path,"x") as file:
            writer = csv.DictWriter(file, headers)
            writer.writeheader()
            writer.writerows(data)
            print("File created successfully")
    except FileExistsError:
        print("Error: The file already exists")
    except Exception as e:
        print(f"Error: {e}")

while True:
  try:
    videogames_list = request_videogames()
    if len(videogames_list) == 0:
        raise ValueError("No videogames were entered. Please enter at least one videogame")
    break
  except Exception as e:
    print(f"Error: {e}")  
create_videogames_csv('videogames.csv', videogames_list, videogames_list[0].keys())