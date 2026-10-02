"""
UNIVERSIDAD NACIONAL DE INGENIERIA
Laboratorio #2: Teoría de Conjuntos - Producto Cartesiano, Operaciones de hasta 3 conjuntos,
Leyes de De Morgan y Diagrama de Venn con Validaciones Lógicas y Servidor Web Local.
Lenguaje: Python
"""
import sys
import os
import http.server
import socketserver
import threading
import webbrowser
import time
# Compatibilidad de consolas Windows
if sys.platform == "win32":
    sys.stdout.reconfigure(encoding='utf-8')
def mostrar_conjunto(nombre: str, conjunto: set) -> None:
    elementos = sorted(list(conjunto))
    if not elementos:
        print(f"  {nombre} = {{ }} (Conjunto Vacío ∅)")
    else:
        print(f"  {nombre} = {{ {', '.join(elementos)} }}")
# =====================================================================
# 1. PRODUCTO CARTESIANO (A x B)
# =====================================================================
def calcular_producto_cartesiano(A: set, B: set) -> None:
    print("\n" + "=" * 55)
    print("          RESULTADO DEL PRODUCTO CARTESIANO (AxB)   ")
    print("=" * 55 + "\n")
    mostrar_conjunto("Conjunto A", A)
    mostrar_conjunto("Conjunto B", B)
    elem_A = sorted(list(A))
    elem_B = sorted(list(B))
    producto = [(a, b) for a in elem_A for b in elem_B]
    print("\nAxB = {")
    for i, a in enumerate(elem_A):
        linea_pares = [f"({a}, {b})" for b in elem_B]
        separador = "," if i < len(elem_A) - 1 else ""
        print("  " + ", ".join(linea_pares) + separador)
    print("}")
    print(f"\nTotal de pares ordenados |AxB| = {len(elem_A)} * {len(elem_B)} = {len(producto)}")
    print("=" * 55 + "\n")
# =====================================================================
# 2. GENERADOR DE SERVIDOR WEB LOCAL Y DIAGRAMA DE VENN HTML/CSS
# =====================================================================
PUERTO_SERVIDOR = 8050
servidor_iniciado = False
def generar_html_venn(U: set, conjuntos: dict) -> str:
    n_conjuntos = len(conjuntos)
    set_U = list(sorted(U))
    set_A = list(sorted(conjuntos.get('A', set())))
    set_B = list(sorted(conjuntos.get('B', set())))
    set_C = list(sorted(conjuntos.get('C', set()))) if n_conjuntos == 3 else []
    A = set(set_A)
    B = set(set_B)
    C = set(set_C) if n_conjuntos == 3 else set()
    Universo = set(set_U)
    if n_conjuntos == 2:
        solo_A = sorted(list(A - B))
        inter_AB = sorted(list(A & B))
        solo_B = sorted(list(B - A))
        fuera = sorted(list(Universo - (A | B)))
        svg_content = f'''
        <svg viewBox="0 0 450 260" class="w-full h-64">
            <!-- Universo -->
            <rect x="10" y="10" width="430" height="240" rx="12" fill="none" stroke="currentColor" stroke-dasharray="4" class="text-[var(--border)]" stroke-width="2"/>
            <text x="25" y="32" class="fill-slate-400 text-xs font-bold">Universo (U)</text>
            
            <!-- Círculo A -->
            <circle cx="160" cy="130" r="80" fill="rgba(59, 130, 246, 0.25)" stroke="#3b82f6" stroke-width="2.5"/>
            <text x="110" y="70" class="fill-blue-500 font-bold text-sm">Conjunto A</text>
            <!-- Círculo B -->
            <circle cx="270" cy="130" r="80" fill="rgba(236, 72, 153, 0.25)" stroke="#ec4899" stroke-width="2.5"/>
            <text x="280" y="70" class="fill-pink-500 font-bold text-sm">Conjunto B</text>
            <!-- Textos Regiones -->
            <text x="130" y="135" text-anchor="middle" class="fill-slate-100 text-xs font-semibold">{", ".join(solo_A) if solo_A else "∅"}</text>
            <text x="215" y="135" text-anchor="middle" class="fill-amber-400 text-xs font-bold">{", ".join(inter_AB) if inter_AB else "∅"}</text>
            <text x="300" y="135" text-anchor="middle" class="fill-slate-100 text-xs font-semibold">{", ".join(solo_B) if solo_B else "∅"}</text>
            <text x="215" y="230" text-anchor="middle" class="fill-slate-400 text-xs font-mono">Fuera (A u B)': {{ {", ".join(fuera)} }}</text>
        </svg>
        '''
    else: # 3 conjuntos A, B, C
        solo_A = sorted(list(A - B - C))
        solo_B = sorted(list(B - A - C))
        solo_C = sorted(list(C - A - B))
        inter_AB = sorted(list((A & B) - C))
        inter_AC = sorted(list((A & C) - B))
        inter_BC = sorted(list((B & C) - A))
        inter_ABC = sorted(list(A & B & C))
        fuera = sorted(list(Universo - (A | B | C)))
        svg_content = f'''
        <svg viewBox="0 0 500 320" class="w-full h-80">
            <!-- Universo -->
            <rect x="10" y="10" width="480" height="300" rx="12" fill="none" stroke="currentColor" stroke-dasharray="4" class="text-[var(--border)]" stroke-width="2"/>
            <text x="25" y="32" class="fill-slate-400 text-xs font-bold">Universo (U)</text>
            
            <!-- Círculo A -->
            <circle cx="190" cy="120" r="75" fill="rgba(59, 130, 246, 0.2)" stroke="#3b82f6" stroke-width="2"/>
            <text x="140" y="60" class="fill-blue-500 font-bold text-xs">Conjunto A</text>
            <!-- Círculo B -->
            <circle cx="310" cy="120" r="75" fill="rgba(236, 72, 153, 0.2)" stroke="#ec4899" stroke-width="2"/>
            <text x="320" y="60" class="fill-pink-500 font-bold text-xs">Conjunto B</text>
            <!-- Círculo C -->
            <circle cx="250" cy="200" r="75" fill="rgba(34, 197, 94, 0.2)" stroke="#22c55e" stroke-width="2"/>
            <text x="235" y="290" class="fill-emerald-500 font-bold text-xs">Conjunto C</text>
            <!-- Textos Regiones -->
            <text x="160" y="115" text-anchor="middle" class="fill-slate-100 text-xs font-medium">{", ".join(solo_A) if solo_A else "∅"}</text>
            <text x="340" y="115" text-anchor="middle" class="fill-slate-100 text-xs font-medium">{", ".join(solo_B) if solo_B else "∅"}</text>
            <text x="250" y="245" text-anchor="middle" class="fill-slate-100 text-xs font-medium">{", ".join(solo_C) if solo_C else "∅"}</text>
            
            <text x="250" y="100" text-anchor="middle" class="fill-amber-300 text-xs font-bold">{", ".join(inter_AB)}</text>
            <text x="195" y="170" text-anchor="middle" class="fill-purple-300 text-xs font-bold">{", ".join(inter_AC)}</text>
            <text x="305" y="170" text-anchor="middle" class="fill-teal-300 text-xs font-bold">{", ".join(inter_BC)}</text>
            <text x="250" y="145" text-anchor="middle" class="fill-yellow-400 text-xs font-black">{", ".join(inter_ABC)}</text>
            
            <text x="250" y="300" text-anchor="middle" class="fill-slate-400 text-xs font-mono">Fuera (A u B u C)': {{ {", ".join(fuera)} }}</text>
        </svg>
        '''
    html_code = f'''<!DOCTYPE html>
<html lang="es" class="dark">
<head>
    <meta charset="UTF-8">
    <title>Visualizador de Diagrama de Venn - UNI</title>
    <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
</head>
<body class="bg-slate-900 text-slate-100 p-6 min-h-screen flex flex-col items-center justify-center">
    <div class="max-w-4xl w-full bg-slate-800 border border-slate-700 rounded-2xl p-6 shadow-2xl space-y-6">
        <div class="border-b border-slate-700 pb-4 flex justify-between items-center">
            <div>
                <h1 class="text-2xl font-black text-blue-400">UNIVERSIDAD NACIONAL DE INGENIERIA</h1>
                <p class="text-slate-400 text-sm">Visualizador del Diagrama de Venn ({n_conjuntos} Conjuntos - Validados en U)</p>
            </div>
            <span class="bg-blue-500/10 text-blue-400 border border-blue-500/20 px-3 py-1 rounded-full text-xs font-semibold">Laboratorio #2</span>
        </div>
        <div class="bg-slate-900 border border-slate-700 rounded-xl p-4 flex flex-col items-center">
            <h2 class="text-sm font-bold uppercase tracking-wider text-slate-400 mb-4">Diagrama de Venn Validado</h2>
            {svg_content}
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs font-mono">
            <div class="bg-slate-900/50 p-4 rounded-xl border border-slate-700 space-y-1">
                <p class="text-slate-400 font-bold uppercase mb-2">Resumen de Conjuntos</p>
                <p><span class="text-blue-400 font-bold">Universo (U):</span> {{ {", ".join(set_U)} }}</p>
                <p><span class="text-blue-400 font-bold">Conjunto A:</span> {{ {", ".join(set_A)} }}</p>
                <p><span class="text-pink-400 font-bold">Conjunto B:</span> {{ {", ".join(set_B)} }}</p>
                {"<p><span class='text-emerald-400 font-bold'>Conjunto C:</span> { " + ", ".join(set_C) + " }</p>" if n_conjuntos == 3 else ""}
            </div>
            <div class="bg-slate-900/50 p-4 rounded-xl border border-slate-700 space-y-1">
                <p class="text-slate-400 font-bold uppercase mb-2">Operaciones Principales</p>
                <p><span class="text-amber-400 font-bold">Unión:</span> {{ {", ".join(sorted(list(A | B | C if n_conjuntos==3 else A | B)))} }}</p>
                <p><span class="text-purple-400 font-bold">Intersección General:</span> {{ {", ".join(sorted(list(A & B & C if n_conjuntos==3 else A & B)))} }}</p>
                <p><span class="text-cyan-400 font-bold">Complemento A' (U - A):</span> {{ {", ".join(sorted(list(Universo - A)))} }}</p>
            </div>
        </div>
    </div>
</body>
</html>'''
    return html_code
def abrir_servidor_web(U: set, conjuntos: dict):
    global servidor_iniciado
    directorio = os.path.dirname(os.path.abspath(__file__))
    archivo_html = os.path.join(directorio, "diagrama_venn_local.html")
    
    with open(archivo_html, "w", encoding="utf-8") as f:
        f.write(generar_html_venn(U, conjuntos))
    url = f"http://localhost:{PUERTO_SERVIDOR}/diagrama_venn_local.html"
    if not servidor_iniciado:
        class QuietHTTPRequestHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, format, *args):
                pass
        def run_server():
            os.chdir(directorio)
            with socketserver.TCPServer(("", PUERTO_SERVIDOR), QuietHTTPRequestHandler) as httpd:
                httpd.serve_forever()
        t = threading.Thread(target=run_server, daemon=True)
        t.start()
        servidor_iniciado = True
        time.sleep(0.5)
    print(f"\n[+] ¡Servidor Web iniciado con éxito!")
    print(f"[+] Abriendo Diagrama de Venn en tu navegador: {url}\n")
    webbrowser.open(url)
# =====================================================================
# 3. MENU Y VALIDACIONES LÓGICAS DE TEORIA DE CONJUNTOS
# =====================================================================
def pedir_conjunto_valido(nombre_conjunto: str, U: set) -> set:
    """Solicita un conjunto al usuario y valida estrictamente que todos sus elementos pertenezcan a U."""
    while True:
        inp = input(f"   • Ingrese elementos del Conjunto {nombre_conjunto} (separados por coma): ").strip()
        elem = set([x.strip() for x in inp.split(",") if x.strip()])
        
        # Validación lógica: Elementos fuera del Universo U
        fuera_de_universo = elem - U
        if fuera_de_universo:
            print(f"\n   ❌ ERROR LÓGICO: Los siguientes elementos NO pertenecen al Universo (U): {sorted(list(fuera_de_universo))}")
            print(f"      El Universo (U) contiene únicamente: {sorted(list(U))}")
            print("      Por favor, reingrese sólo elementos pertenecientes a U.\n")
        else:
            return elem
def ingresar_teoria_conjuntos():
    print("\n" + "=" * 55)
    print("      CONFIGURACIÓN DE TEORÍA DE CONJUNTOS           ")
    print("=" * 55)
    # 1. Pedir el Conjunto Universo U (Validación: no puede estar vacío)
    while True:
        input_U = input("\n[1] Ingrese los elementos del UNIVERSO (U) separados por coma: ").strip()
        U = set([x.strip() for x in input_U.split(",") if x.strip()])
        if not U:
            print("   ❌ ERROR: El Universo (U) no puede estar vacío. Intente nuevamente.")
        else:
            break
    print(f"   ✅ Universo registrado: U = {{ {', '.join(sorted(list(U)))} }}")
    # 2. Cantidad de conjuntos (hasta 3)
    n_conjuntos = 0
    while n_conjuntos not in [2, 3]:
        try:
            n_conjuntos = int(input("\n[2] ¿Cuántos conjuntos desea trabajar? (2 o 3): "))
            if n_conjuntos not in [2, 3]:
                print("   ❌ ERROR: Debe ingresar 2 o 3 conjuntos.")
        except ValueError:
            print("   ❌ ERROR: Ingrese un número válido (2 o 3).")
    # 3. Ingresar conjuntos con validación contra el Universo U
    conjuntos = {}
    nombres = ['A', 'B', 'C']
    for i in range(n_conjuntos):
        nombre = nombres[i]
        conjuntos[nombre] = pedir_conjunto_valido(nombre, U)
    return U, conjuntos
def menu_operaciones_interactivas(U: set, conjuntos: dict):
    n_conjuntos = len(conjuntos)
    A = conjuntos['A']
    B = conjuntos['B']
    C = conjuntos.get('C', set())
    while True:
        print("\n" + "=" * 55)
        print("          MENÚ DE OPERACIONES DE TEORÍA DE CONJUNTOS    ")
        print("=" * 55)
        print(f"  Universo (U) = {{ {', '.join(sorted(list(U)))} }}")
        print(f"  Conjunto A   = {{ {', '.join(sorted(list(A)))} }}")
        print(f"  Conjunto B   = {{ {', '.join(sorted(list(B)))} }}")
        if n_conjuntos == 3:
            print(f"  Conjunto C   = {{ {', '.join(sorted(list(C)))} }}")
        print("-" * 55)
        print("1. Unión (∪)")
        print("2. Intersección (∩)")
        print("3. Diferencia (-)")
        print("4. Diferencia Simétrica (Δ)")
        print("5. Complementos (A', B', C')")
        print("6. Demostrar Leyes de De Morgan")
        print("7. Ver Diagrama de Venn (Servidor HTML/CSS)")
        print("0. Volver al menú principal")
        op = input("\nSeleccione una opción: ").strip()
        if op == "1":
            print("\n--- UNIÓN ---")
            mostrar_conjunto("A ∪ B", A | B)
            if n_conjuntos == 3:
                mostrar_conjunto("A ∪ C", A | C)
                mostrar_conjunto("B ∪ C", B | C)
                mostrar_conjunto("A ∪ B ∪ C", A | B | C)
        elif op == "2":
            print("\n--- INTERSECCIÓN ---")
            mostrar_conjunto("A ∩ B", A & B)
            if n_conjuntos == 3:
                mostrar_conjunto("A ∩ C", A & C)
                mostrar_conjunto("B ∩ C", B & C)
                mostrar_conjunto("A ∩ B ∩ C", A & B & C)
        elif op == "3":
            print("\n--- DIFERENCIA ---")
            mostrar_conjunto("A - B", A - B)
            mostrar_conjunto("B - A", B - A)
            if n_conjuntos == 3:
                mostrar_conjunto("A - C", A - C)
                mostrar_conjunto("B - C", B - C)
        elif op == "4":
            print("\n--- DIFERENCIA SIMÉTRICA ---")
            mostrar_conjunto("A Δ B", A ^ B)
            if n_conjuntos == 3:
                mostrar_conjunto("A Δ C", A ^ C)
                mostrar_conjunto("B Δ C", B ^ C)
        elif op == "5":
            print("\n--- COMPLEMENTOS ---")
            mostrar_conjunto("A' (U - A)", U - A)
            mostrar_conjunto("B' (U - B)", U - B)
            if n_conjuntos == 3:
                mostrar_conjunto("C' (U - C)", U - C)
        elif op == "6":
            print("\n--- DEMOSTRACIÓN LEYES DE DE MORGAN ---")
            comp_A, comp_B = U - A, U - B
            izq1, der1 = U - (A | B), comp_A & comp_B
            izq2, der2 = U - (A & B), comp_A | comp_B
            print(f"1. (A ∪ B)' = A' ∩ B' -> Izq: {sorted(list(izq1))} | Der: {sorted(list(der1))} | {'✅ CUMPLE' if izq1==der1 else '❌'}")
            print(f"2. (A ∩ B)' = A' ∪ B' -> Izq: {sorted(list(izq2))} | Der: {sorted(list(der2))} | {'✅ CUMPLE' if izq2==der2 else '❌'}")
        elif op == "7":
            abrir_servidor_web(U, conjuntos)
        elif op == "0":
            break
# =====================================================================
# 4. PROGRAMA PRINCIPAL
# =====================================================================
def main():
    U = {"1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "A", "B", "C"}
    conjuntos = {
        'A': {"A", "B", "C", "1", "2"},
        'B': {"1", "2", "5", "7", "9"}
    }
    while True:
        print("\n" + "=" * 55)
        print("      UNIVERSIDAD NACIONAL DE INGENIERIA           ")
        print("    LABORATORIO #2: TEORÍA DE CONJUNTOS CON VALIDACIÓN LÓGICA")
        print("=" * 55)
        print("1. Producto Cartesiano (A x B)")
        print("2. Configurar Universo U e Ingresar Conjuntos (hasta 3 con validación)")
        print("3. Calcular Operaciones de Conjuntos y Leyes de De Morgan")
        print("4. Ver Diagrama de Venn (Servidor HTML/CSS en Navegador)")
        print("0. Salir")
        opcion = input("\nSeleccione una opción: ").strip()
        if opcion == "1":
            calcular_producto_cartesiano(conjuntos['A'], conjuntos['B'])
        elif opcion == "2":
            U, conjuntos = ingresar_teoria_conjuntos()
        elif opcion == "3":
            menu_operaciones_interactivas(U, conjuntos)
        elif opcion == "4":
            abrir_servidor_web(U, conjuntos)
        elif opcion == "0":
            print("\n¡Gracias por utilizar el programa del Laboratorio #2!")
            break
        else:
            print("\nOpción no válida. Intente nuevamente.")
if __name__ == "__main__":
    main()