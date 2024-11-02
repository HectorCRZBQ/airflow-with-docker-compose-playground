# dags/merged_population_city_pipeline.py
from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import pandas as pd
import requests

# URLs y paths
DATA_URL_1 = "https://raw.githubusercontent.com/datasets/population/master/data/population.csv"  # Datos de población
DATA_URL_2 = "https://raw.githubusercontent.com/datasets/world-cities/refs/heads/main/data/world-cities.csv"  # Datos de ciudades
RAW_DATA_PATH_1 = "/tmp/raw_data_1.csv"
RAW_DATA_PATH_2 = "/tmp/raw_data_2.csv"
MERGED_PATH = "/tmp/merged_data.csv"
REPORT_PATH = "/tmp/merged_report.txt"

# Funciones de procesamiento
def download_data_1():
    response = requests.get(DATA_URL_1)
    with open(RAW_DATA_PATH_1, "w") as f:
        f.write(response.text)

def download_data_2():
    response = requests.get(DATA_URL_2)
    with open(RAW_DATA_PATH_2, "w") as f:
        f.write(response.text)

def merge_data():
    # Cargar ambos archivos descargados
    df1 = pd.read_csv(RAW_DATA_PATH_1)
    df2 = pd.read_csv(RAW_DATA_PATH_2)

    # Para el merge, asumimos que ambos datasets tienen una columna "Country Name" en común.
    # Necesitamos asegurarnos de que df2 tenga la columna "Country Name". 
    # Añadimos una columna "Country Name" a df2 si es necesario.
    df2['Country Name'] = df2['country']  # Renombramos la columna si es necesario.

    # Combinar en función de "Country Name"
    merged_df = pd.merge(df1, df2, on=["Country Name"], how='inner')  # Hacemos un inner join por país

    # Guardar datos combinados
    merged_df.to_csv(MERGED_PATH, index=False)

def generate_merged_report():
    df = pd.read_csv(MERGED_PATH)
    with open(REPORT_PATH, "w") as f:
        f.write("Informe Combinado de Datos de Población y Ciudades\n")
        f.write("===================================================\n\n")
        # Ejemplo: listar los países, población y nombres de ciudades
        for _, row in df.iterrows():
            f.write(f"{row['Country Name']}: Población: {row['Value']:,.0f}, Ciudad: {row['name']}, Región: {row['subcountry']}\n")

# Definición del DAG
default_args = {
    'owner': 'student',
    'depends_on_past': False,
    'start_date': datetime(2024, 1, 1),
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'merged_population_city_analysis',
    default_args=default_args,
    description='Pipeline de análisis combinado de población y ciudades',
    schedule_interval=timedelta(days=1),
)

# Tareas
t1 = PythonOperator(
    task_id='download_data_1',
    python_callable=download_data_1,
    dag=dag,
)

t2 = PythonOperator(
    task_id='download_data_2',
    python_callable=download_data_2,
    dag=dag,
)

t3 = PythonOperator(
    task_id='merge_data',
    python_callable=merge_data,
    dag=dag,
)

t4 = PythonOperator(
    task_id='generate_merged_report',
    python_callable=generate_merged_report,
    dag=dag,
)

# Definir dependencias
[t1, t2] >> t3 >> t4
