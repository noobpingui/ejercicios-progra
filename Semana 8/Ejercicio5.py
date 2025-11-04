

# 1. Investigue cómo leer y escribir archivos `JSON` en Python [aquí](https://www.w3schools.com/python/python_json.asp).
# 2. Cree un programa que permita agregar un Pokémon nuevo al archivo de la lección de JSON ([Archivos JSON](https://www.notion.so/Archivos-JSON-79f9758cb59d4452a9c8668efa25356c?pvs=21)).
#     a. Debe leer el archivo para importar los Pokémones existentes.
#     b. Luego debe pedir la información del Pokémon a agregar.
#     c. Finalmente debe guardar el nuevo Pokémon en el archivo.

import json

pokemons_data = [
  {
    "name": {
      "english": "Pikachu"
    },
    "type": [
      "Electric"
    ],
    "base": {
      "HP": 35,
      "Attack": 55,
      "Defense": 40,
      "Sp. Attack": 50,
      "Sp. Defense": 50,
      "Speed": 90
    }
  },
  {
    "name": {
      "english": "Charmander"
    },
    "type": [
      "Fire"
    ],
    "base": {
      "HP": 39,
      "Attack": 52,
      "Defense": 43,
      "Sp. Attack": 60,
      "Sp. Defense": 50,
      "Speed": 65
    }
  },
  {
    "name": {
      "english": "Squirtle"
    },
    "type": [
      "Water"
    ],
    "base": {
      "HP": 44,
      "Attack": 48,
      "Defense": 65,
      "Sp. Attack": 50,
      "Sp. Defense": 64,
      "Speed": 43
    }
  }
]

def create_pokemons_json(file_path, pokemons_data):
    try:
        with open(file_path, "x") as file:
            json.dump(pokemons_data, file, indent=4)
            print("File created successfully")
    except FileExistsError:
        print("Error: The file already exists")
    except Exception as e:
        print(f"Error: {e}")

def read_pokemons_json(file_path):
    try:
        with open(file_path, "r") as file:
            pokemons_data = json.load(file)
            for pokemon in pokemons_data:
                print(f"Pokemon: {pokemon['name']['english']}, Type: {', '.join(pokemon['type'])}, Base Stats: HP: {pokemon['base']['HP']}, Attack: {pokemon['base']['Attack']}, Defense: {pokemon['base']['Defense']}, Sp. Attack: {pokemon['base']['Sp. Attack']}, Sp. Defense: {pokemon['base']['Sp. Defense']}, Speed: {pokemon['base']['Speed']}")

    except FileNotFoundError:
        print("Error: The file does not exist")
    except Exception as e:
        print(f"Error: {e}")

def add_pokemon(file_path):
    try:
        with open(file_path, "r+") as file:
            pokemons_data = json.load(file)
            new_pokemon = {
                "name": {
                    "english": input("Enter the Pokemon's name: ")
                },
                "type": [
                    input("Enter the Pokemon type: ")
                    ],
                "base": {
                    "HP": int(input("Enter the HP of the Pokemon: ")),
                    "Attack": int(input("Enter the Attack of the Pokemon: ")),
                    "Defense": int(input("Enter the Defense of the Pokemon: ")),
                    "Sp. Attack": int(input("Enter the Special Attack of the Pokemon: ")),
                    "Sp. Defense": int(input("Enter the Special Defense of the Pokemon: ")),
                    "Speed": int(input("Enter the Speed of the Pokemon: "))
                }
            }
            pokemons_data.append(new_pokemon)
            file.seek(0)
            json.dump(pokemons_data, file, indent=4)
            print("The new Pokemon has been added successfully")
            file.truncate()
            
    except FileNotFoundError:
        print("Error: The file does not exist")
    except Exception as e:
        print(f"Error: {e}")


create_pokemons_json('pokemons.json', pokemons_data)
read_pokemons_json('pokemons.json')
add_pokemon('pokemons.json')
read_pokemons_json('pokemons.json')