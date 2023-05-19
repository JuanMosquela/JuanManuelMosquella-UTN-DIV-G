import re
import json
import csv
from utils.models import *


def pedir_texto(placeholder: str) -> str:
    while True:
        try:
            texto = input(placeholder).lower()

            if re.match("^[a-zA-ZáéíóúÁÉÍÓÚüÜñÑ\s_-]+$", texto):
                return texto

            raise ValueError

        except ValueError:
            print('Valor ingresado no valido, ingrese otro porfavor: ')


def pedir_num(texto: str) -> int:
    while True:
        try:
            numero = int(input(texto))
            return numero

        except:
            print('Valor ingresado no valido, ingrese un numero valido porfavor: ')


def group_by(lista: list, key: str, value: any) -> list:

    new_list = list(filter(lambda item: item[key] == value, lista))
    return new_list


def normalize_data(lista: list) -> int | list:

    if len(lista) == 0:
        print("Error: lista vacia")
        return - 1
    is_normalized = False

    for item in lista:

        for field in item:

            if field == "PRECIO":
                item[field] = item[field].replace("$", "")

                if item[field].replace(".", "").isdigit():
                    if item[field].isdigit():
                        item[field] = int(item[field])
                    else:
                        item[field] = float(item[field])
            elif field == "MARCA":
                item[field] = item[field].strip()

        is_normalized = True

    if is_normalized:
        print("Datos normalizados")

    return lista


def sort(lista: list, key: str, asc: bool = True) -> list:
    for i in range(len(lista) - 1):
        for j in range(i + 1, len(lista)):

            if ((asc and lista[i][key].lower() > lista[j][key].lower())
                    or (not asc and lista[j][key].lower() > lista[i][key].lower())):
                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux

    return lista


def double_sort(lista: list, key: str, secondary_key: str, asc: bool = True) -> list:

    size = len(lista)
    for i in range(size - 1):
        for j in range(i + 1, size):
            if lista[i][key] > lista[j][key] or (lista[i][key] == lista[j][key] and lista[i][secondary_key] < lista[j][secondary_key]):
                aux = lista[i]
                lista[i] = lista[j]
                lista[j] = aux

    return lista


def abrir_json(path):
    try:
        with open(path) as file:
            file = file.read()
            data_json = json.loads(file)
            data_json = json.dumps(data_json, indent=4)
            return data_json
    except:
        print(barra)
        print("No se encontro el archivo")
        print(barra)


def crear_lista(lista: list, headers: list) -> list:
    aux = []

    for item in lista:
        diccionario = {}
        for i in range(len(headers)):

            diccionario[headers[i]] = item[i]

        aux.append(diccionario)

    return aux


def abrir_csv(path):
    with open(path, newline="", encoding="utf-8") as file:
        data = csv.reader(file, delimiter="\n")
        lista = []

        headers = next(data)[0].split(",")

        for row in data:
            items = row[0].split(",")
            lista.append(items)

        return crear_lista(lista, headers)
