from firebase_functions import https_fn
from firebase_admin import initialize_app
import json
import matplotlib
matplotlib.use('Agg')  # Para entornos sin interfaz gráfica como Cloud Functions
import matplotlib.pyplot as plt
import pandas as pd
from io import BytesIO
from datetime import datetime
import logging

# Inicializar la app de Firebase
initialize_app()

# Configuración de logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def validate_date_format(date_str: str) -> bool:
    """Valida que la fecha tenga el formato YYYY-MM-DD."""
    try:
        datetime.strptime(date_str, '%Y-%m-%d')
        return True
    except ValueError:
        return False

@https_fn.on_request()
def generate_chart(req: https_fn.Request) -> https_fn.Response:
    """
    Función HTTP de Firebase que genera un gráfico JPG de calorías quemadas.
    """
    # CORS preflight
    if req.method == 'OPTIONS':
        return https_fn.Response(
            '',
            status=204,
            headers={
                'Access-Control-Allow-Origin': '*',
                'Access-Control-Allow-Methods': 'POST',
                'Access-Control-Allow-Headers': 'Content-Type',
                'Access-Control-Max-Age': '3600'
            }
        )

    # Cabeceras para la respuesta
    headers = {
        'Access-Control-Allow-Origin': '*',
        'Content-Type': 'image/jpeg'
    }

    try:
        # Solo POST permitido
        if req.method != 'POST':
            error = {'error': 'Solo se aceptan solicitudes POST'}
            return https_fn.Response(json.dumps(error), status=405, headers=headers)

        # Parsear JSON
        payload = req.get_json(silent=True)
        if not payload:
            error = {'error': 'No se recibieron datos JSON'}
            return https_fn.Response(json.dumps(error), status=400, headers=headers)

        # Validar campos
        for field in ('start_date', 'end_date', 'data'):
            if field not in payload:
                error = {'error': f"Campo requerido '{field}' no encontrado"}
                return https_fn.Response(json.dumps(error), status=400, headers=headers)

        # Validar formato de fechas
        if not validate_date_format(payload['start_date']) or not validate_date_format(payload['end_date']):
            error = {'error': 'Las fechas deben tener formato YYYY-MM-DD'}
            return https_fn.Response(json.dumps(error), status=400, headers=headers)

        # Validar lista de datos
        data = payload['data']
        if not isinstance(data, list) or len(data) == 0:
            error = {'error': 'Los datos deben ser una lista no vacía'}
            return https_fn.Response(json.dumps(error), status=400, headers=headers)

        # Crear DataFrame
        df = pd.DataFrame(data)
        if 'date' not in df or 'calories' not in df:
            error = {'error': "Cada entrada debe tener 'date' y 'calories'"}
            return https_fn.Response(json.dumps(error), status=400, headers=headers)

        # Procesar fechas
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d')
        df = df.sort_values('date')

        # Generar gráfica
        plt.figure(figsize=(10, 6))
        plt.plot(df['date'], df['calories'], 'o-', linewidth=2, markersize=6)
        plt.xlabel('RANGO DE FECHAS', fontsize=12)
        plt.ylabel('CALORÍAS QUEMADAS', fontsize=12)
        plt.title('Seguimiento de Calorías Quemadas', fontsize=14)
        plt.xticks(rotation=45)
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.tight_layout()

        # Guardar en buffer
        buf = BytesIO()
        plt.savefig(buf, format='jpg', dpi=100)
        plt.close()
        buf.seek(0)

        # Devolver imagen
        return https_fn.Response(buf.getvalue(), headers=headers)

    except Exception as e:
        logger.error(f"Error al generar gráfica: {e}")
        error = {'error': str(e)}
        return https_fn.Response(json.dumps(error), status=500, headers=headers)
