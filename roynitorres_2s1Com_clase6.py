"""
UNIVERSIDAD NACIONAL DE INGENIERIA
Laboratorio #2: Teoría de Conjuntos - Producto Cartesiano
Lenguaje: Python
"""

def mostrar_conjunto(nombre: str, conjunto: list[str]) -> None:
    print(f"{nombre} = {{ {', '.join(conjunto)} }}")

def calcular_producto_cartesiano(A: list[str], B: list[str]) -> None:
    print("\n" + "=" * 51)
    print("          RESULTADO DEL PRODUCTO CARTESIANO        ")
    print("=" * 51 + "\n")

    mostrar_conjunto("A", A)
    mostrar_conjunto("B", B)

    # Cálculo del producto cartesiano mediante comprensión de listas
    producto = [(a, b) for a in A for b in B]

    print("\nAxB = {")
    
    # Formatear la salida en filas por cada elemento de A
    for i, a in enumerate(A):
        linea_pares = [f"({a}, {b})" for b in B]
        separador = "," if i < len(A) - 1 else "" #Esto se llama operador ternario. Es un if-else comprimido que sirve para decidir si la fila debe llevar una coma al final o no.
        print("  " + ", ".join(linea_pares) + separador)

    print("}")
    print(f"\nTotal de pares ordenados |AxB| = n(A) * n(B) = {len(A)} * {len(B)} = {len(producto)}")
    print("=" * 51 + "\n")





def cargar_ejemplo_guia():
    A = ["A", "B", "C"]
    B = ["1", "5", "7", "9"]
    return A, B

def ingresar_conjuntos_usuario():
    print("\n--- INGRESO DEL CONJUNTO A ---")
    nA = int(input("¿Cuántos elementos tiene el conjunto A? "))
    A = [input(f"Elemento A[{i+1}]: ").strip() for i in range(nA)]

    print("\n--- INGRESO DEL CONJUNTO B ---")
    nB = int(input("¿Cuántos elementos tiene el conjunto B? "))
    B = [input(f"Elemento B[{i+1}]: ").strip() for i in range(nB)]

    return A, B

def main():
    while True:
        print("=" * 51)
        print("      UNIVERSIDAD NACIONAL DE INGENIERIA           ")
        print("    LABORATORIO #2: PRODUCTO CARTESIANO DE CONJUNTOS")
        print("=" * 51)
        print("1. Probar con el ejemplo de la guía A={A,B,C}, B={1,5,7,9}")
        print("2. Ingresar conjuntos personalizados")
        print("0. Salir")
        
        opcion = input("Seleccione una opción: ").strip()

        if opcion == "1":
            A, B = cargar_ejemplo_guia()
            calcular_producto_cartesiano(A, B)
        elif opcion == "2":
            A, B = ingresar_conjuntos_usuario()
            calcular_producto_cartesiano(A, B)
        elif opcion == "0":
            print("\n¡Gracias por utilizar el programa!")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.\n")

if __name__ == "__main__":
    main()