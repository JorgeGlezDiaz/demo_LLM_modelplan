 


def sumar(a: int, b: int) -> int:
    resultado = a + b
    # print(f"La suma de {a} y {b} es igual a {resultado}")
    # imprimir(a)
    return resultado

def imprimir(t):
    print(t)

def leer_datos() -> list[int]:
    with open("/home/jorgeglezdiaz/Escritorio/practises/ATRINEO/demo_LLM_modelplan/datos.csv", "r") as f:
        lineas = f.readlines()
    lista_sin_encabezado = lineas[1:]
    datos = []
    for num in lista_sin_encabezado:
        n = num.split(",")
        for each in n:
            datos.append(int(each))
    return datos


#
# Codigo Principal
#
costo = 100
impuesto = 16

print(sumar(costo, impuesto))

datos = leer_datos()
print(datos)
print(sumar(datos[0], datos[1]))
