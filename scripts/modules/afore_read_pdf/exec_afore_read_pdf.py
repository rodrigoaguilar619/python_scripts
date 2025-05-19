import pandas as pd
from datetime import datetime
from calendar import monthrange
import math
import pymysql

# Leer archivo CSV
df = pd.read_csv("G:/work/configuration/projects/statement_track/afore/afore_data.csv")

# Limpiar columnas
df.columns = [col.strip() for col in df.columns]
df = df.rename(columns={
    'Fecha': 'fecha',
    'Concepto': 'concepto',
    'Período - Referencia': 'periodo_referencia',
    'Días cotizados': 'dias_cotizados',
    'Salario base': 'salario_base',
    'Monto': 'monto',
    'Seccion': 'seccion',
    'Periodo': 'periodo'
})

# map for catalog
seccion_ids = {
    'Ahorro para el Retiro': 1,
    'Ahorro para la Vivienda': 2,
    'Ahorro Voluntario/Solidario': 3,
}

concepto_ids = {
    'COMISION DEL PERIODO': 1,
    'RENDIMIENTO DEL PERIODO': 2,
    'Intereses en Transito IMSS del periodo': 3,
    'Aportacion PATRONAL en Subcuenta RETIRO IMSS': 4,
    'Aportacion en Subcta CESANTIA EN EDAD AVANZADA Y VEJEZ IMSS': 5,
    "Aportacion en Subcuenta CESANTIA EN EDAD AVANZADA Y VEJEZ IMSS": 5,
    "Aportacion en Subcuenta de CESANTIA EN EDAD AVANZADA Y VEJEZ IMSS": 5,
    'Aportacion CV Gobierno': 6,
    'Aportacion en Subcuenta CUOTA SOCIAL IMSS': 7,
    'APORTACION VOLUNTARIA VIA DOMICILIACION': 8,
    'Interes de Vivienda INFONAVIT del periodo': 9,
    'Aportacion INFONAVIT 97': 10,
    'DESFASE': 11,
    'Aportacion Complementaria de Retiro via VENTANILLA': 12,
    "Actualizaciones y Recargos IMSS del periodo": 13,
    "Aportacion Voluntaria via VENTANILLA": 14,
    "Retiro de Ahorro Voluntario de Corto Plazo": 15,
    "Importe Retirado": 16
}

concepto_unificado_ids = {
    'COMISION DEL PERIODO': 1,
    'RENDIMIENTO DEL PERIODO': 2,
    'Intereses en Transito IMSS del periodo': 3,
    'Aportacion PATRONAL en Subcuenta RETIRO IMSS': 4,
    'Aportacion en Subcta CESANTIA EN EDAD AVANZADA Y VEJEZ IMSS': 5,
    "Aportacion en Subcuenta CESANTIA EN EDAD AVANZADA Y VEJEZ IMSS": 5,
    "Aportacion en Subcuenta de CESANTIA EN EDAD AVANZADA Y VEJEZ IMSS": 5,
    'Aportacion CV Gobierno': 6,
    'Aportacion en Subcuenta CUOTA SOCIAL IMSS': 7,
    'APORTACION VOLUNTARIA VIA DOMICILIACION': 8,
    'Interes de Vivienda INFONAVIT del periodo': 9,
    'Aportacion INFONAVIT 97': 10,
    'DESFASE': 11,
    'Aportacion Complementaria de Retiro via VENTANILLA': 8,
    "Actualizaciones y Recargos IMSS del periodo": 13,
    "Aportacion Voluntaria via VENTANILLA": 8,
    "Retiro de Ahorro Voluntario de Corto Plazo": 15,
    "Importe Retirado": 15
}

def add_last_day_of_month(date_str):
  """Adds the last day of the month to a date string in 'YYYY-MM' format.

  Args:
    date_str: A string representing a date in 'YYYY-MM' format.

  Returns:
    A string representing the date with the last day of the month in 'YYYY-MM-DD' format.
    Returns None if the input string is not in the correct format.
  """
  try:
    year, month = map(int, date_str.split('-'))
    last_day = monthrange(year, month)[1]
    return f"{year}-{month:02d}-{last_day:02d}"
  except ValueError:
    return None

def get_db_connection():
    """Establish a connection to the database."""
    try:
        connection = pymysql.connect(
            host='localhost',
            user='root',
            password='',
            database='afore_track',
            cursorclass=pymysql.cursors.DictCursor
        )
        print("Connected to the database!")
        with connection.cursor() as cursor:
            cursor.execute("SELECT VERSION();")
            version = cursor.fetchone()
            print("Database version:", version)
        return connection
    except pymysql.MySQLError as e:
        print("Error while connecting to MySQL:", e)
        return None


try:
    connection = get_db_connection()
    if connection is None:
        print("Failed to connect to the database. Exiting...")
        exit(1)
    with connection.cursor() as cursor:

        for _, row in df.iterrows():
            # Procesar y limpiar datos
            fecha = None
            if pd.notna(row['fecha']):
                try:
                    fecha = datetime.strptime(row['fecha'].strip(), "%d-%b-%y").date()
                except:
                    fecha = None
            #periodo = datetime.strptime(row['periodo'], "%Y-%m").date()
            periodo = add_last_day_of_month(row['periodo'])

            dias_cotizados = int(row['dias_cotizados']) if not pd.isna(row['dias_cotizados']) else None
            salario_base = float(row['salario_base']) if not pd.isna(row['salario_base']) else None
            monto = float(row['monto']) if not pd.isna(row['monto']) else None
            seccion_id = seccion_ids[row['seccion']] if row['seccion'] in seccion_ids else None
            periodo_referencia = row['periodo_referencia'] if not pd.isna(row['periodo_referencia']) else None
            concepto_id = concepto_ids[row['concepto'].strip()] if row['concepto'] in concepto_ids else None
            concepto_unificado_id = concepto_unificado_ids[row['concepto'].strip()] if row['concepto'] in concepto_unificado_ids else None

            # Insertar en aportaciones
            print(f"{row['concepto']} - {row['seccion']} - {row['monto']}")
            print(f"DATOS fecha: {fecha} - concepto: {concepto_id} - periodo_referencia: {row['periodo_referencia']} - dias_cotizados: {dias_cotizados} - salario_base: {salario_base} - monto: {monto} - seccion_id: {seccion_id} - periodo: {periodo}")
            query = "INSERT INTO afore_contribution (date_inserted, id_concept, id_concept_unified,  period_reference, quoted_days, base_salary, amount, id_section, period) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            '''with open('query.txt', 'a') as f:
                f.write(query)
                f.write('\n')'''
            cursor.execute(query, (fecha, concepto_id, concepto_unificado_id, periodo_referencia, dias_cotizados, salario_base, monto, seccion_id, periodo))
            cursor.connection.commit()

finally:
    if connection:
        connection.close()
        print("Connection closed.")