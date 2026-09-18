/*
 * UNIVERSIDAD NACIONAL DE INGENIERIA
 * Laboratorio #2: Teoría de Conjuntos - Producto Cartesiano
 */

#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define MAX_ELEMENTOS 50
#define TAM_CADENA 50

void mostrarConjunto(const char* nombre, char conjunto[MAX_ELEMENTOS][TAM_CADENA], int n) {
    int i;
    printf("%s = { ", nombre);
    for (i = 0; i < n; i++) {
        printf("%s", conjunto[i]);
        if (i < n - 1) {
            printf(", ");
        }
    }
    printf(" }\n");
}

void calcularProductoCartesiano(char A[MAX_ELEMENTOS][TAM_CADENA], int nA, 
                                char B[MAX_ELEMENTOS][TAM_CADENA], int nB) {
    int i, j;
    int contador = 0;

    printf("\n===================================================\n");
    printf("          RESULTADO DEL PRODUCTO CARTESIANO        \n");
    printf("===================================================\n\n");

    mostrarConjunto("A", A, nA);
    mostrarConjunto("B", B, nB);

    printf("\nAxB = {\n");

    for (i = 0; i < nA; i++) {
        printf("  ");
        for (j = 0; j < nB; j++) {
            printf("(%s, %s)", A[i], B[j]);
            contador++;

            if (i < nA - 1 || j < nB - 1) {
                printf(", ");
            }
        }
        printf("\n");
    }

    printf("}\n");
    printf("\nTotal de pares ordenados |AxB| = n(A) * n(B) = %d * %d = %d\n", nA, nB, contador);
    printf("===================================================\n\n");
}

void cargarEjemploGuia(char A[MAX_ELEMENTOS][TAM_CADENA], int *nA, 
                       char B[MAX_ELEMENTOS][TAM_CADENA], int *nB) {
    *nA = 3;
    strcpy(A[0], "A");
    strcpy(A[1], "B");
    strcpy(A[2], "C");

    *nB = 4;
    strcpy(B[0], "1");
    strcpy(B[1], "5");
    strcpy(B[2], "7");
    strcpy(B[3], "9");
}

void ingresarConjuntosUsuario(char A[MAX_ELEMENTOS][TAM_CADENA], int *nA, 
                              char B[MAX_ELEMENTOS][TAM_CADENA], int *nB) {
    int i;

    printf("\n--- INGRESO DEL CONJUNTO A ---\n");
    printf("¿Cuántos elementos tiene el conjunto A? ");
    scanf("%d", nA);

    for (i = 0; i < *nA; i++) {
        printf("Elemento A[%d]: ", i + 1);
        scanf("%s", A[i]);
    }

    printf("\n--- INGRESO DEL CONJUNTO B ---\n");
    printf("¿Cuántos elementos tiene el conjunto B? ");
    scanf("%d", nB);

    for (i = 0; i < *nB; i++) {
        printf("Elemento B[%d]: ", i + 1);
        scanf("%s", B[i]);
    }
}

int main() {
    char A[MAX_ELEMENTOS][TAM_CADENA];
    char B[MAX_ELEMENTOS][TAM_CADENA];
    int nA = 0, nB = 0;
    int opcion;

    do {
        printf("===================================================\n");
        printf("      UNIVERSIDAD NACIONAL DE INGENIERIA           \n");
        printf("    LABORATORIO #2: PRODUCTO CARTESIANO DE CONJUNTOS\n");
        printf("===================================================\n");
        printf("1. Probar con el ejemplo de la guía A={A,B,C}, B={1,5,7,9}\n");
        printf("2. Ingresar conjuntos personalizados\n");
        printf("0. Salir\n");
        printf("Seleccione una opción: ");
        scanf("%d", &opcion);

        switch (opcion) {
            case 1:
                cargarEjemploGuia(A, &nA, B, &nB);
                calcularProductoCartesiano(A, nA, B, nB);
                break;

            case 2:
                ingresarConjuntosUsuario(A, &nA, B, &nB);
                calcularProductoCartesiano(A, nA, B, nB);
                break;

            case 0:
                printf("\n¡Gracias por utilizar el programa!\n");
                break;

            default:
                printf("\nOpción no válida. Intente nuevamente.\n\n");
                break;
        }

    } while (opcion != 0);

    return 0;
}