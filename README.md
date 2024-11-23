### **README - Compilador de High-LOGO a Python con Turtle**

---

## **Descripción del Proyecto**

Este proyecto es un compilador que traduce programas escritos en un lenguaje llamado **High-LOGO** a código Python que utiliza la librería `turtle` para gráficos. **High-LOGO** es un lenguaje de alto nivel diseñado para controlar una "tortuga gráfica", permitiendo crear dibujos a partir de comandos como mover hacia adelante, girar, levantar o bajar el lápiz, y más.

El compilador convierte los programas High-LOGO en scripts Python completamente funcionales, listos para ser ejecutados, y genera gráficos en una ventana de `turtle`.

---

## **Características del Lenguaje High-LOGO**

- **Comandos básicos**:
  - `FD <valor>`: Avanza hacia adelante.
  - `BK <valor>`: Retrocede.
  - `LT <valor>`: Gira hacia la izquierda.
  - `RT <valor>`: Gira hacia la derecha.
  - `PU`: Levanta el lápiz (no deja rastro al moverse).
  - `PD`: Baja el lápiz (deja rastro al moverse).

- **Estructuras de control**:
  - Condicionales (`if-else`):
    ```hlogo
    if (x > 5) {
        FD 100
    } else {
        BK 50
    }
    ```
  - Bucles (`for`):
    ```hlogo
    for i in range(0, 10, 2) {
        FD i
    }
    ```

- **Definición de funciones**:
  ```hlogo
  def draw_square(size) {
      for i in range(0, 4, 1) {
          FD size
          RT 90
      }
  }
  draw_square(100)
  ```

---

## **Estructura del Proyecto**

El proyecto se compone de los siguientes archivos clave:

1. **`hlogoc.py`**:
   - El compilador principal que toma un archivo High-LOGO, lo analiza y genera un archivo Python traducido.
   - Utiliza la librería `Lark` para procesar la gramática de High-LOGO y construir el Árbol de Sintaxis Abstracta (AST).

2. **Archivo de entrada (`*.hlogo`)**:
   - Contiene el programa High-LOGO que deseas compilar.

3. **Archivo de salida (`*.hlogo.py`)**:
   - El archivo Python generado por el compilador, que contiene el código traducido y listo para ejecutarse.

---

## **Requisitos Previos**

- Python 3.8 o superior.
- Librerías necesarias: `Lark`, `turtle`.
  - Puedes instalarlas ejecutando:
    ```bash
    pip install lark
    ```

---

## **Cómo Usar el Compilador**

### **1. Preparar el Archivo High-LOGO**
Escribe tu programa en un archivo con la extensión `.hlogo`. Por ejemplo, crea un archivo llamado `program.hlogo` con tu codigo a compilar, como por ejemplo:

```hlogo
FD 100
LT 90
FD 100
```

### **2. Ejecutar el Compilador**
En la terminal, ejecuta el compilador con el archivo de entrada:

```bash
python hlogoc.py program.hlogo
```

Esto generará un archivo de salida llamado `program.hlogo.py`.

### **3. Ejecutar el Archivo Generado**
Corre el archivo Python generado para ver el dibujo de la tortuga:

```bash
python program.hlogo.py
```

---

## **Estructura del Código**

El compilador tiene tres partes principales:

1. **Gramática del Lenguaje**:
   Define las reglas de High-LOGO, incluyendo comandos, condicionales, bucles y funciones.

2. **Funciones de Traducción**:
   - `translate_program`: Traduce todo el programa recorriendo el AST.
   - `translate_boolean_expression`: Convierte expresiones condicionales a Python.
   - `translate_range_args`: Traduce rangos de bucles al formato de Python.

3. **Salida del Código**:
   Genera un archivo Python estructurado, con el encabezado necesario para usar `turtle` y las instrucciones traducidas.

---

## **Ejemplo Completo**

### Código High-LOGO (`program.hlogo`):
```hlogo
def draw_triangle(size) {
    for i in range(0, 3, 1) {
        FD size
        RT 120
    }
}

draw_triangle(150)
```

### Código Python Generado (`program.hlogo.py`):
```python
import turtle
t = turtle.Turtle()

def draw_triangle(size):
    for i in range(0, 3, 1):
        t.forward(size)
        t.right(120)

draw_triangle(150)
turtle.mainloop()
```

Al ejecutarlo, se dibuja un triángulo equilátero con lados de 150 unidades.

---

## **Notas y Consideraciones**

- Asegúrate de que el archivo de entrada tenga una sintaxis válida en High-LOGO.
- Si encuentras errores de traducción o ejecución, revisa el contenido del archivo `.hlogo` para corregir cualquier instrucción mal escrita.
- Puedes modificar el archivo Python generado para personalizar el comportamiento de tu programa.

---

## **Licencia**

Este proyecto es de código abierto y está bajo la Licencia MIT. Puedes usarlo, modificarlo y distribuirlo libremente.

---

Si necesitas ayuda adicional, ¡no dudes en preguntar! 🎨🐢
