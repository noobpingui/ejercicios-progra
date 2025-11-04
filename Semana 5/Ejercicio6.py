

# 1. Cree un diccionario que guarde la siguiente información sobre un hotel:
#     - `nombre`
#     - `numero_de_estrellas`
#     - `habitaciones`
#     - El value del key de `habitaciones` debe ser una lista, y cada habitación debe tener la siguiente información:
#         - `numero`
#         - `piso`
#         - `precio_por_noche`

the_hotel_dictionary = {

    "name" : "Monte Verde",
    "stars" : 5,
    "rooms" : [
				{"Room number": 101, "Floor": 3, "Price per night": 100},
				{"Room number": 51, "Floor": 2, "Price per night": 85},
				{"Room number": 23, "Floor": 1, "Price per night": 75}       
		]
}

print(f"La informacion del hotel: {the_hotel_dictionary}")