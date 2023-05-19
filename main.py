from functions.funciones_parcial import *
from functions.funciones import *
from utils.models import *

options = [
    "1 - Traer datos desde csv",
    "2 - Listar cantidad por marca",
    "3 - Listar insumos por marca",
    "4 - Buscar insumo por caracteristica",
    "5 - Listar insumos ordenados",
    "6 - Realizar compras",
    "7 - Guardar json",
    "8 - Leer json",
    "9 - Actualizar precios",
    "10 - Abrir txt"
]

lista = []

while True:
    match(generar_menu(options)):
        case 1:
            lista = abrir_csv("data/insumos.csv")
            lista = normalize_data(lista)

        case 2:
            if len(lista) == 0:
                print(error)
            else:
                count_by(lista, "MARCA")
        case 3:
            if len(lista) == 0:
                print(error)
            else:
                lista_agrupada = sort(lista, "MARCA")

                print(headers_ordenamiento)
                for item in lista_agrupada:
                    print(
                        f"|{item['ID']:^8}|{item['NOMBRE']:^60}|{item['MARCA']:^18}|{item['PRECIO']:^16}|{str(item['CARACTERISTICAS'].split('|!*|')[0]):^76}|\n")

        case 4:
            if len(lista) == 0:
                print(error)

            else:
                print(buscar_insumos(lista))
        case 5:
            if len(lista) == 0:
                print(error)
            else:
                lista_ordenada = double_sort(
                    lista, "MARCA", "PRECIO", asc=False)

                for item in lista_ordenada:
                    print(
                        f"|{item['ID']:^8}|{item['NOMBRE']:^60}|{item['MARCA']:^18}|{item['PRECIO']:^16}|{item['CARACTERISTICAS'][0]:^82}|\n")

        case 6:
            if len(lista) == 0:
                print(error)
            else:
                carrito = comprar_producto(lista)

                option = pedir_texto(
                    "Desea guardar el archivo en docuemnto de texto ? (s/n): ")
                if (option == "s"):
                    guardar_archivo(carrito, "txt")

        case 7:
            if len(lista) == 0:
                print(error)
            else:

                lista_filtrada = buscar_producto(lista, "Disco Duro")
                guardar_archivo(lista_filtrada, "json")
        case 8:

            file = abrir_json("data/data_productos.json")
            print(file)
        case 9:

            lista_precios_actualizados = aplicar_aumento(lista)

            guardar_archivo(lista_precios_actualizados, "csv")
        case 10:
            lista_marcas = abrir_txt("data/marcas.txt")
            lista_productos = crear_nuevo_producto(lista_marcas, lista)
            for product in lista_productos:
                lista.append(product)

            guardar_archivo(lista)

    respuesta = pedir_texto("Desea agregar otro producto ? (s/n): ")

    if (respuesta == "n"):
        break
