from functions.funciones_parcial import *
from functions.funciones import *
from utils.models import *
import functools
import re
import os


def count_by(lista: list, key):
    # extraemos las principales marcas
    marcas = list(set(map(lambda item: item[key], lista)))

    diccionario = {}
    for marca in marcas:

        acc = 0
        # si la marca del elemento coincide con algunz de las marcas aumentamos su cantidad en 1
        for item in lista:
            if item[key] == marca:
                acc += 1

        diccionario[marca] = acc

    print(header_branches)
    for key in diccionario:
        print(f"|{key:^52}|{diccionario[key]:^50}|\n")


def buscar_insumos(lista: list) -> list:

    description = pedir_texto("Ingrese la descripcion del insumo: ")

    # creamos una nueva lista con los elemtos que en su camnpo caracteriticas contengan lo que el usuario quiere buscar
    elementos_encontrados = list(filter(
        lambda item:  description in item["CARACTERISTICAS"], lista))

    return elementos_encontrados


def actualizar_total(carrito: dict, key: str) -> int:
    # toma una key sobre la cual va a operar y el carrito. Itera sobre todos los productos del carrito y retorna un valor final
    total = functools.reduce(
        lambda acc, product: acc + product[key], carrito["ITEMS"], 0)
    return total


def comprar_producto(lista):

    # esta funcion crea un diccionario que representa nuestro carrito, le permiter al usuario filtrar los productos en base a su marca y elegir uno para agregar al carrito. Si el producto no esta en el carrito lo agrega, si ya esta en el carrito aumenta su cantidad

    carrito = {
        "ITEMS": [],
        "TOTAL": 0,
        "TOTAL_QUANTITY": 0
    }

    respuesta = "s"

    while respuesta == "s":

        while True:
            ingresar_marca = pedir_texto(
                "Ingrese la marca del producto que quiere comprar: ").capitalize()

            elementos_agrupados = list(
                filter(lambda item: item["MARCA"] == ingresar_marca, lista))

            if len(elementos_agrupados) > 0:
                break
            else:
                print("No se encontro esa marca, ingrese otra")

        for elemento in elementos_agrupados:
            print(elemento)

        while True:
            name = input(
                "Ingrese el nombre del producto que quiere comprar: ")

            find_product = list(
                filter(lambda item: item["NOMBRE"] == name, lista))
            print(find_product)

            if len(find_product) > 0:
                break
            else:
                print("No se encontro el elemento, ingrtese otro")

        product_in_cart = list(
            filter(lambda product: product["ID"] == find_product[0]["ID"], carrito["ITEMS"]))

        if len(product_in_cart) > 0:

            amount = pedir_num("Ingrese la cantidad del producto: ")

            find_product[0]["QUANTITY"] += amount
            sub_total = find_product[0]["PRECIO"] * amount
            find_product[0]["SUB_TOTAL"] += sub_total
            carrito["TOTAL"] = actualizar_total(carrito, "SUB_TOTAL")
            carrito["TOTAL_QUANTITY"] = actualizar_total(carrito, "QUANTITY")

        else:

            amount = pedir_num("Ingrese la cantidad del producto: ")

            find_product[0]["QUANTITY"] = amount
            find_product[0]["SUB_TOTAL"] = find_product[0]["PRECIO"] * amount
            carrito["ITEMS"].append(find_product[0])
            carrito["TOTAL"] = actualizar_total(carrito, "SUB_TOTAL")
            carrito["TOTAL_QUANTITY"] = actualizar_total(carrito, "QUANTITY")

        respuesta = input("Desea agregar otro producto al carrito? (s/n)")

    return carrito


def buscar_producto(lista, product_name):
    # creamos una nueva lista filtrando los elementos que en su nombre contengan la variable product_name
    # solo va a retornar si el len de la lista es mayor a 0, es decir si encontro alguna concidencia
    productos_filtrados = list(filter(lambda product: len(
        re.findall(product_name, product["NOMBRE"])) > 0, lista))
    return productos_filtrados


def aplicar_aumento(lista: list):

    # crea una copia de cada item de nuestra lista, pero en su campo PRECIO aplica un aumento del % 8.4

    lista_aumenta = list(
        map(lambda product: {**product, "PRECIO": round(product["PRECIO"] * 8.4, 2)}, lista))

    return lista_aumenta


def generar_menu(options: list):

    os.system("cls")

    print(header)
    print("-----------------------------------------\n")
    for option in options:
        print(option)

    choise = pedir_num('Ingrese lo que quiere hacer: ')

    return choise


def guardar_archivo(lista: list, extension: str = ""):

    if len(lista) == 0:
        return

    if extension == "":
        while True:
            extension = pedir_texto(
                "Ingrese la extension a guardar (json, csv): ")
            if extension == "json" or extension == "csv":
                break

    file_name = pedir_texto("Ingrese el nombre del archivo: ")

    with open(f"data/{file_name}.{extension}", "w") as file:
        match extension:
            case "csv":
                headers = lista[0].keys()
                writer = csv.DictWriter(file, fieldnames=headers)
                # Escribir las claves en la primera fila
                writer.writeheader()
                writer.writerows(lista)
            case "txt":
                file.write(f"ORDEN DE COMPRA\n")
                file.write("-------------------------\n")
                for product in lista["ITEMS"]:

                    file.write(
                        f"{product['NOMBRE']}: ${product['PRECIO']:.2f} x {product['QUANTITY']}\n")
                file.write("-------------------------\n")
                total = actualizar_total(lista, "SUB_TOTAL")
                file.write(f"Total: ${total:.2f}\n")

            case "json":
                json.dump(lista, file, indent=4)


def crear_nuevo_producto(lista_marcas, lista):
    lista_productos = []
    while True:

        new_product = {}

        ultimo_id = int(lista[len(lista) - 1]["ID"])

        new_product["ID"] = ultimo_id + 1

        name = pedir_texto("Ingrese el nombre del producto: ")

        new_product["NOMBRE"] = name

        for marca in lista_marcas:
            print(marca)

        while True:

            branch = pedir_texto("Ingrese la marca de su producto: ")

            find_branch = list(
                filter(lambda item: item == branch, lista_marcas))

            if len(find_branch) > 0:
                break

            else:
                print("No se encotnro la marca, intente otra vez")

        new_product["MARCA"] = branch

        price = pedir_num("Ingrese el valor del producto: ")

        new_product["PRICE"] = price

        new_product["CARACTERISTICAS"] = []

        while len(new_product["CARACTERISTICAS"]) < 3:
            if len(new_product["CARACTERISTICAS"]) >= 1:
                choose = pedir_texto("Desea continuar? (s/n): ")
                if choose == "s":
                    caracteristica = pedir_texto(
                        "Ingrese la caract de su producto: ")
                    new_product["CARACTERISTICAS"].append(caracteristica)
                else:
                    break
            else:

                caracteristica = pedir_texto(
                    "Ingrese la caract de su producto: ")

                new_product["CARACTERISTICAS"].append(caracteristica)

        caracterisiticas = "|!*|".join(new_product["CARACTERISTICAS"])
        new_product["CARACTERISTICAS"] = caracterisiticas

        choose = pedir_texto("Deseea continuar? (s/n):")
        if choose == "n":
            lista_productos.append(new_product)
            break
        else:
            lista_productos.append(new_product)

    return lista_productos
