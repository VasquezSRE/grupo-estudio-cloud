import boto3
import json
import time
import requests
import os
from dotenv import load_dotenv # Para cargar variables de entorno
from datetime import datetime # Para posibles transformaciones de fecha si las usas

# --- Configuración Inicial ---

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuración de AWS
region = "us-east-1"  # Cambia a tu región AWS preferida si es diferente
# Asegúrate de que el nombre del bucket sea globalmente único
bucket_name = "sports-analytics-data-lake-nba-workshop-2024" 
glue_database_name = "glue_nba_data_lake"
athena_output_location = f"s3://{bucket_name}/athena-results/"

# Configuración de Sportsdata.io (cargada desde .env)
api_key = os.getenv("SPORTS_DATA_API_KEY")

# Endpoint para Player Season Stats (Estadísticas de Jugadores por Temporada)
NBA_STATS_SEASON = "2024"  # Define la temporada para las estadísticas de jugadores (ej. 2024 para la temporada actual)
nba_player_stats_endpoint = f"https://api.sportsdata.io/v3/nba/stats/json/PlayerSeasonStats/{NBA_STATS_SEASON}?key={api_key}"

# Crear clientes de AWS
s3_client = boto3.client("s3", region_name=region)
glue_client = boto3.client("glue", region_name=region)
athena_client = boto3.client("athena", region_name=region)

# --- Funciones de AWS y ETL ---

def create_s3_bucket():
    """
    Crea un bucket de S3 para almacenar los datos deportivos.
    Maneja la creación del bucket según la región de AWS.
    """
    try:
        # Para us-east-1, no se especifica LocationConstraint en create_bucket
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"S3 bucket '{bucket_name}' creado exitosamente.")
    except Exception as e:
        # Ignora el error si el bucket ya existe
        if "BucketAlreadyOwnedByYou" in str(e):
            print(f"S3 bucket '{bucket_name}' ya existe y te pertenece. Continuando.")
        else:
            print(f"Error creando S3 bucket: {e}")

def create_glue_database():
    """
    Crea una base de datos de Glue para el data lake.
    Esta base de datos es donde se registrarán las tablas para Athena.
    """
    try:
        glue_client.create_database(
            DatabaseInput={
                "Name": glue_database_name,
                "Description": "Glue database for NBA sports analytics.",
            }
        )
        print(f"Glue database '{glue_database_name}' creada exitosamente.")
    except Exception as e:
        # Ignora el error si la base de datos ya existe
        if "AlreadyExistsException" in str(e):
            print(f"Glue database '{glue_database_name}' ya existe. Continuando.")
        else:
            print(f"Error creando Glue database: {e}")

def fetch_nba_player_stats_data():
    """
    Extrae los datos de estadísticas de temporada de jugadores de la API de Sportsdata.io.
    Utiliza el endpoint configurado para la temporada específica.
    """
    try:
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        response = requests.get(nba_player_stats_endpoint, headers=headers)
        response.raise_for_status()  # Lanza un error para códigos de estado HTTP incorrectos (ej. 4xx, 5xx)
        print(f"Datos de estadísticas de jugadores de la NBA extraídos exitosamente para la temporada {NBA_STATS_SEASON}.")
        return response.json()
    except Exception as e:
        print(f"Error extrayendo datos de estadísticas de jugadores de la NBA: {e}")
        return []

def convert_to_line_delimited_json(data):
    """
    Convierte una lista de diccionarios JSON en un formato JSON delimitado por líneas.
    Cada diccionario se serializa a una línea separada.
    """
    print("Convirtiendo datos a formato JSON delimitado por líneas...")
    return "\n".join([json.dumps(record) for record in data])

def upload_player_stats_data_to_s3(data):
    """
    Carga los datos de estadísticas de temporada de jugadores de la NBA al bucket de S3.
    Los datos se suben en formato JSON delimitado por líneas.
    """
    try:
        line_delimited_data = convert_to_line_delimited_json(data)
        # Define la clave del objeto S3 con el nombre de la temporada para mayor claridad
        file_key = f"raw-data/nba_player_season_stats_season_{NBA_STATS_SEASON}.jsonl"

        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=line_delimited_data
        )
        print(f"Datos de estadísticas de jugadores cargados a S3: {file_key}")
    except Exception as e:
        print(f"Error cargando datos de estadísticas de jugadores a S3: {e}")

def create_glue_player_stats_table():
    """
    Crea una tabla de Glue para los datos de estadísticas de temporada de jugadores de la NBA.
    Define el esquema de la tabla y su ubicación en S3, usando un SerDe JSON.
    """
    table_name = "nba_player_season_stats"
    try:
        glue_client.create_table(
            DatabaseName=glue_database_name,
            TableInput={
                "Name": table_name,
                "StorageDescriptor": {
                    "Columns": [
                        {"Name": "StatID", "Type": "int"},
                        {"Name": "TeamID", "Type": "int"},
                        {"Name": "PlayerID", "Type": "int"},
                        {"Name": "SeasonType", "Type": "int"},
                        {"Name": "Season", "Type": "int"},
                        {"Name": "Name", "Type": "string"},
                        {"Name": "Team", "Type": "string"},
                        {"Name": "Position", "Type": "string"},
                        {"Name": "Started", "Type": "int"},
                        {"Name": "GlobalTeamID", "Type": "int"},
                        {"Name": "Updated", "Type": "string"},
                        {"Name": "Games", "Type": "int"},
                        {"Name": "FantasyPoints", "Type": "double"},
                        {"Name": "Minutes", "Type": "int"},
                        {"Name": "Seconds", "Type": "int"},
                        {"Name": "FieldGoalsMade", "Type": "double"},
                        {"Name": "FieldGoalsAttempted", "Type": "double"},
                        {"Name": "FieldGoalsPercentage", "Type": "double"},
                        {"Name": "EffectiveFieldGoalsPercentage", "Type": "double"},
                        {"Name": "TwoPointersMade", "Type": "double"},
                        {"Name": "TwoPointersAttempted", "Type": "double"},
                        {"Name": "TwoPointersPercentage", "Type": "double"},
                        {"Name": "ThreePointersMade", "Type": "double"},
                        {"Name": "ThreePointersAttempted", "Type": "double"},
                        {"Name": "ThreePointersPercentage", "Type": "double"},
                        {"Name": "FreeThrowsMade", "Type": "double"},
                        {"Name": "FreeThrowsAttempted", "Type": "double"},
                        {"Name": "FreeThrowsPercentage", "Type": "double"},
                        {"Name": "OffensiveRebounds", "Type": "double"},
                        {"Name": "DefensiveRebounds", "Type": "double"},
                        {"Name": "Rebounds", "Type": "double"},
                        {"Name": "OffensiveReboundsPercentage", "Type": "double"},
                        {"Name": "DefensiveReboundsPercentage", "Type": "double"},
                        {"Name": "TotalReboundsPercentage", "Type": "double"},
                        {"Name": "Assists", "Type": "double"},
                        {"Name": "Steals", "Type": "double"},
                        {"Name": "BlockedShots", "Type": "double"},
                        {"Name": "Turnovers", "Type": "double"},
                        {"Name": "PersonalFouls", "Type": "double"},
                        {"Name": "Points", "Type": "double"},
                        {"Name": "TrueShootingAttempts", "Type": "double"},
                        {"Name": "TrueShootingPercentage", "Type": "double"},
                        {"Name": "PlayerEfficiencyRating", "Type": "double"},
                        {"Name": "AssistsPercentage", "Type": "double"},
                        {"Name": "StealsPercentage", "Type": "double"},
                        {"Name": "BlocksPercentage", "Type": "double"},
                        {"Name": "TurnOversPercentage", "Type": "double"},
                        {"Name": "UsageRatePercentage", "Type": "double"},
                        {"Name": "FantasyPointsFanDuel", "Type": "double"},
                        {"Name": "FantasyPointsDraftKings", "Type": "double"},
                        {"Name": "FantasyPointsYahoo", "Type": "double"},
                        {"Name": "PlusMinus", "Type": "double"},
                        {"Name": "DoubleDoubles", "Type": "int"},
                        {"Name": "TripleDoubles", "Type": "int"},
                        {"Name": "FantasyPointsFantasyDraft", "Type": "double"},
                        {"Name": "IsClosed", "Type": "boolean"},
                        {"Name": "LineupConfirmed", "Type": "boolean"},
                        {"Name": "LineupStatus", "Type": "string"}
                    ],
                    "Location": f"s3://{bucket_name}/raw-data/", # Apunta a la carpeta donde se suben los JSONL
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe",
                        "Parameters": {
                            "ignore.malformed.json": "true" # Ignora errores de formato JSON para evitar fallos
                        }
                    },
                    "Compressed": False,
                },
                "TableType": "EXTERNAL_TABLE",
            },
        )
        print(f"Glue table '{table_name}' creada exitosamente.")
    except Exception as e:
        # Ignora el error si la tabla ya existe
        if "AlreadyExistsException" in str(e):
            print(f"Glue table '{table_name}' ya existe. Continuando.")
        else:
            print(f"Error creando Glue table: {e}")

def configure_athena():
    """
    Configura la ubicación de salida para las consultas de Athena.
    También crea la base de datos de Athena si no existe, lo cual es redundante si Glue ya la creó,
    pero asegura que el output location esté configurado.
    """
    try:
        athena_client.start_query_execution(
            QueryString=f"CREATE DATABASE IF NOT EXISTS {glue_database_name}",
            ResultConfiguration={"OutputLocation": athena_output_location},
        )
        print("Ubicación de salida de Athena configurada exitosamente.")
    except Exception as e:
        print(f"Error configurando Athena: {e}")

def run_athena_query(query_string, database_name, output_location):
    """
    Ejecuta una consulta SQL en Athena y muestra los resultados en la consola.
    Espera a que la consulta finalice y maneja posibles errores.
    """
    try:
        print(f"\nEjecutando consulta de Athena:\n{query_string}")
        response = athena_client.start_query_execution(
            QueryString=query_string,
            QueryExecutionContext={"Database": database_name},
            ResultConfiguration={"OutputLocation": output_location},
        )
        query_execution_id = response["QueryExecutionId"]

        # Esperar a que la consulta complete
        state = "RUNNING"
        while state in ["RUNNING", "QUEUED"]:
            query_status = athena_client.get_query_execution(
                QueryExecutionId=query_execution_id
            )
            state = query_status["QueryExecution"]["Status"]["State"]
            print(f"Estado de la consulta: {state}")
            if state == "FAILED":
                print(
                    f"Consulta fallida: {query_status['QueryExecution']['Status']['StateChangeReason']}"
                )
                return None
            elif state == "SUCCEEDED":
                print("¡Consulta exitosa!")
                break
            time.sleep(5) # Espera 5 segundos antes de verificar el estado nuevamente

        # Obtener los resultados de la consulta
        results = athena_client.get_query_results(
            QueryExecutionId=query_execution_id, MaxResults=100 # Puedes ajustar MaxResults
        )

        # Procesar e imprimir los resultados
        column_info = results["ResultSet"]["ResultSetMetadata"]["ColumnInfo"]
        column_names = [col["Name"] for col in column_info]
        print(f"Resultados para '{query_string.splitlines()[0].strip()}':")
        print(" | ".join(column_names))
        # Imprime una línea divisoria para mejor legibilidad
        print("-" * (sum(len(name) for name in column_names) + (len(column_names) - 1) * 3))

        # Recorre las filas de resultados (omite la fila de encabezado)
        for row in results["ResultSet"]["Rows"][1:]:
            print(" | ".join([col.get("VarCharValue", "NULL") for col in row["Data"]]))
        return results

    except Exception as e:
        print(f"Error ejecutando consulta de Athena: {e}")
        return None

# --- Flujo Principal de ETL y Análisis ---

def main():
    """
    Función principal que orquesta el proceso ETL:
    1. Crea el bucket S3 y la base de datos Glue.
    2. Extrae datos de estadísticas de jugadores de la API.
    3. Carga los datos crudos a S3.
    4. Crea (o actualiza) la tabla Glue para los datos.
    5. Configura Athena.
    6. Ejecuta consultas SQL en Athena para generar rankings de jugadores.
    """
    print("Configurando el Data Lake para el análisis deportivo de la NBA...")
    
    # 1. Crear S3 Bucket
    create_s3_bucket()
    time.sleep(5) # Pequeña pausa para asegurar la propagación del bucket
    
    # 2. Crear Glue Database
    create_glue_database()

    # 3. y 4. Extraer y Cargar Datos de Estadísticas de Jugadores
    print("\n--- Extrayendo y cargando datos de estadísticas de temporada de jugadores de la NBA ---")
    nba_player_stats = fetch_nba_player_stats_data()
    if nba_player_stats:
        upload_player_stats_data_to_s3(nba_player_stats)
    
    # 5. Crear Tabla Glue para Estadísticas de Jugadores
    print("\n--- Creando tabla Glue para estadísticas de temporada de jugadores de la NBA ---")
    create_glue_player_stats_table()
    
    # 6. Configurar la ubicación de salida de Athena
    print("\n--- Configurando la ubicación de salida de Athena ---")
    configure_athena()

    # 7. Ejecutar consultas de Athena para análisis (Rankings)
    print("\n--- Ejecutando consultas de Athena para el análisis de estadísticas de jugadores (Rankings) ---")

    # Consideración importante: filtrar jugadores con pocos minutos/juegos para rankings significativos
    MIN_MINUTES_PLAYED = 500 # Un umbral razonable para jugadores con participación real en la temporada
    # MIN_GAMES_PLAYED = 20 # Otra opción de umbral

    # Query 1: Top 10 jugadores por Puntos Totales
    top_10_points_query = f"""
    SELECT
        "name",
        "team",
        "points",
        "games"
    FROM
        "{glue_database_name}"."nba_player_season_stats"
    WHERE
        "Season" = {NBA_STATS_SEASON}
        AND "SeasonType" = 1 -- 1 = Regular Season. Asegúrate de que los datos de la API se corresponden.
        AND "Minutes" >= {MIN_MINUTES_PLAYED}
    ORDER BY
        "points" DESC
    LIMIT 10;
    """
    run_athena_query(top_10_points_query, glue_database_name, athena_output_location)

    # Query 2: Top 10 jugadores por Asistencias Totales
    top_10_assists_query = f"""
    SELECT
        "name",
        "team",
        "assists",
        "games"
    FROM
        "{glue_database_name}"."nba_player_season_stats"
    WHERE
        "Season" = {NBA_STATS_SEASON}
        AND "SeasonType" = 1
        AND "Minutes" >= {MIN_MINUTES_PLAYED}
    ORDER BY
        "assists" DESC
    LIMIT 10;
    """
    run_athena_query(top_10_assists_query, glue_database_name, athena_output_location)

    # Query 3: Top 10 jugadores por Eficiencia (Player Efficiency Rating - PER)
    top_10_per_query = f"""
    SELECT
        "name",
        "team",
        "playerefficiencyrating",
        "games",
        "minutes"
    FROM
        "{glue_database_name}"."nba_player_season_stats"
    WHERE
        "Season" = {NBA_STATS_SEASON}
        AND "SeasonType" = 1
        AND "Minutes" >= {MIN_MINUTES_PLAYED}
    ORDER BY
        "playerefficiencyrating" DESC
    LIMIT 10;
    """
    run_athena_query(top_10_per_query, glue_database_name, athena_output_location)

    # Query 4: Top 5 equipos por puntos totales (sumando puntos de todos sus jugadores)
    top_5_teams_by_points_query = f"""
    SELECT
        "team",
        SUM("points") AS total_team_points
    FROM
        "{glue_database_name}"."nba_player_season_stats"
    WHERE
        "Season" = {NBA_STATS_SEASON}
        AND "SeasonType" = 1
    GROUP BY
        "team"
    ORDER BY
        total_team_points DESC
    LIMIT 5;
    """
    run_athena_query(top_5_teams_by_points_query, glue_database_name, athena_output_location)

    print("\nConfiguración del Data Lake completada y consultas de análisis iniciales ejecutadas.")

if __name__ == "__main__":
    main()

