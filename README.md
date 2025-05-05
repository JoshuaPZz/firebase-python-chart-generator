# Nombre_De_Tu_Repositorio

Una función de Firebase Cloud escrita en Python que acepta datos de salud (calorías quemadas) a través de una solicitud HTTP POST y genera dinámicamente un gráfico JPG visualizando la quema de calorías a lo largo del tiempo utilizando las bibliotecas Matplotlib y Pandas.

## Características

* **Trigger HTTP:** Se activa mediante una solicitud POST a un endpoint HTTP.
* **Validación de Datos:** Valida el formato y la estructura de los datos JSON de entrada.
* **Generación de Gráficos:** Crea un gráfico de líneas/puntos de las calorías quemadas a lo largo del tiempo.
* **Salida de Imagen:** Devuelve el gráfico generado como una imagen JPG.
* **CORS Habilitado:** Configurado para permitir solicitudes desde cualquier origen.
* **Manejo Básico de Errores:** Proporciona respuestas de error informativas en formato JSON.

## Tecnologías Utilizadas

* [Firebase Cloud Functions](https://firebase.google.com/docs/functions)
* [Python 3.x](https://www.python.org/)
* [Matplotlib](https://matplotlib.org/)
* [Pandas](https://pandas.pydata.org/)

## Prerrequisitos

Antes de comenzar, asegúrate de tener instalado lo siguiente:

* [Node.js y npm](https://nodejs.org/) (necesario para la CLI de Firebase)
* [Firebase CLI](https://firebase.google.com/docs/cli) (`npm install -g firebase-tools`)
* [Python 3.x](https://www.python.org/downloads/)
* [pip](https://pip.pypa.io/en/stable/installation/) (generalmente viene con Python)
* Una cuenta de Google Cloud y un [Proyecto de Firebase](https://console.firebase.google.com/)

## Configuración

Sigue estos pasos para configurar y desplegar la función en tu proyecto de Firebase:

1.  **Clona el repositorio:**
    ```bash
    git clone [https://github.com/TuUsuario/Nombre_De_Tu_Repositorio.git](https://github.com/TuUsuario/Nombre_De_Tu_Repositorio.git)
    cd Nombre_De_Tu_Repositorio
    ```
2.  **Navega al directorio de las funciones:**
    ```bash
    cd functions
    ```
3.  **Crea y activa un entorno virtual de Python:**
    ```bash
    python -m venv venv
    # En Linux/macOS
    source venv/bin/activate
    # En Windows
    .\venv\Scripts\activate
    ```
4.  **Instala las dependencias de Python:**
    ```bash
    pip install -r requirements.txt
    ```
5.  **Regresa al directorio raíz del proyecto:**
    ```bash
    cd ..
    ```
6.  **Inicia sesión en Firebase (si no lo has hecho):**
    ```bash
    firebase login
    ```
7.  **Asocia tu proyecto local con tu proyecto de Firebase:**
    ```bash
    firebase use --add
    ```
    Selecciona el proyecto de Firebase al que deseas desplegar la función.
8.  **Despliega la función:**
    ```bash
    firebase deploy --only functions
    ```

Una vez completado el despliegue, la función estará disponible en un endpoint HTTP proporcionado por Firebase.

## Uso

La función `generate_chart` espera una solicitud HTTP **POST** con un cuerpo en formato **JSON**.

**Endpoint:**

Encontrarás la URL exacta en la Consola de Firebase, bajo la sección "Functions" > "Dashboard". La URL tendrá un formato similar a:
`https://REGION-PROJECT_ID.cloudfunctions.net/generateChart`

Reemplaza `REGION` con la región donde desplegaste la función (ej. `us-central1`) y `PROJECT_ID` con el ID de tu proyecto de Firebase.

**Método de Solicitud:**

`POST`

**Cabeceras:**

`Content-Type: application/json`

**Cuerpo de la Solicitud (JSON):**

El JSON debe contener los siguientes campos:

* `start_date` (string): La fecha de inicio para el rango del gráfico en formato `YYYY-MM-DD`.
* `end_date` (string): La fecha de fin para el rango del gráfico en formato `YYYY-MM-DD`.
* `data` (array de objetos): Una lista de puntos de datos. Cada objeto en la lista debe tener:
    * `date` (string): La fecha del punto de dato en formato `YYYY-MM-DD`.
    * `calories` (número): El valor de calorías quemadas para esa fecha.

**Ejemplo de cuerpo JSON:**

```json
{
  "start_date": "2023-10-01",
  "end_date": "2023-10-07",
  "data": [
    { "date": "2023-10-01", "calories": 450 },
    { "date": "2023-10-02", "calories": 520 },
    { "date": "2023-10-03", "calories": 480 },
    { "date": "2023-10-04", "calories": 600 },
    { "date": "2023-10-05", "calories": 550 },
    { "date": "2023-10-06", "calories": 580 },
    { "date": "2023-10-07", "calories": 620 }
  ]
}
