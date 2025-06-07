import os
from dotenv import load_dotenv
import requests
import json
import boto3
import time
from datetime import datetime

# Load environment variables from .env file
load_dotenv()

# AWS configurations
region = "us-east-1"
bucket_name = "lab3-sports-analytics-data-lake"  # Asegúrate de que este nombre sea único globalmente
glue_database_name = "glue_nba_data_lake"
athena_output_location = f"s3://{bucket_name}/athena-results/"

# Sportsdata.io configurations (loaded from .env)
api_key = os.getenv("SPORTS_DATA_API_KEY")

# Nuevo endpoint para juegos, usando el formato con {season}
# Puedes definir el año de la temporada aquí directamente o como variable de entorno
NBA_GAMES_SEASON = "2024" # Por ejemplo, para la temporada 2024
nba_games_endpoint = f"https://api.sportsdata.io/v3/nba/scores/json/Games/{NBA_GAMES_SEASON}?key={api_key}"

# Create AWS clients
s3_client = boto3.client("s3", region_name=region)
glue_client = boto3.client("glue", region_name=region)
athena_client = boto3.client("athena", region_name=region)

def create_s3_bucket():
    """Create an S3 bucket for storing sports data."""
    try:
        if region == "us-east-1":
            s3_client.create_bucket(Bucket=bucket_name)
        else:
            s3_client.create_bucket(
                Bucket=bucket_name,
                CreateBucketConfiguration={"LocationConstraint": region},
            )
        print(f"S3 bucket '{bucket_name}' created successfully.")
    except Exception as e:
        print(f"Error creating S3 bucket: {e}")

def create_glue_database():
    """Create a Glue database for the data lake."""
    try:
        glue_client.create_database(
            DatabaseInput={
                "Name": glue_database_name,
                "Description": "Glue database for NBA sports analytics.",
            }
        )
        print(f"Glue database '{glue_database_name}' created successfully.")
    except Exception as e:
        print(f"Error creating Glue database: {e}")

def fetch_nba_games_data():
    """Fetch NBA game data from sportsdata.io."""
    try:
        headers = {"Ocp-Apim-Subscription-Key": api_key}
        # Asegúrate de que el endpoint ya incluye la API key si la construyes así
        response = requests.get(nba_games_endpoint, headers=headers)
        response.raise_for_status()
        print(f"Fetched NBA game data successfully for season {NBA_GAMES_SEASON}.")
        return response.json()
    except Exception as e:
        print(f"Error fetching NBA game data: {e}")
        return []

def convert_to_line_delimited_json(data):
    """Convert data to line-delimited JSON format."""
    print("Converting data to line-delimited JSON format...")
    return "\n".join([json.dumps(record) for record in data])

def upload_games_data_to_s3(data):
    """Upload NBA game data to the S3 bucket."""
    try:
        line_delimited_data = convert_to_line_delimited_json(data)
        file_key = f"raw-data/nba_game_data_season_{NBA_GAMES_SEASON}.jsonl" # Nombre de archivo más específico

        s3_client.put_object(
            Bucket=bucket_name,
            Key=file_key,
            Body=line_delimited_data
        )
        print(f"Uploaded game data to S3: {file_key}")
    except Exception as e:
        print(f"Error uploading game data to S3: {e}")

def create_glue_games_table():
    """Create a Glue table for NBA game data."""
    try:
        glue_client.create_table(
            DatabaseName=glue_database_name,
            TableInput={
                "Name": "nba_games",
                "StorageDescriptor": {
                    "Columns": [
                        {"Name": "GameID", "Type": "int"},
                        {"Name": "Season", "Type": "int"},
                        {"Name": "SeasonType", "Type": "int"},
                        {"Name": "Status", "Type": "string"},
                        {"Name": "Day", "Type": "string"},
                        {"Name": "DateTime", "Type": "string"},
                        {"Name": "AwayTeam", "Type": "string"},
                        {"Name": "HomeTeam", "Type": "string"},
                        {"Name": "AwayTeamID", "Type": "int"},
                        {"Name": "HomeTeamID", "Type": "int"},
                        {"Name": "StadiumID", "Type": "int"},
                        {"Name": "Channel", "Type": "string"},
                        {"Name": "Attendance", "Type": "int"}, # Campo clave
                        {"Name": "AwayTeamScore", "Type": "int"},
                        {"Name": "HomeTeamScore", "Type": "int"},
                        {"Name": "Updated", "Type": "string"},
                        {"Name": "Quarter", "Type": "string"},
                        {"Name": "TimeRemainingMinutes", "Type": "int"},
                        {"Name": "TimeRemainingSeconds", "Type": "int"},
                        {"Name": "PointSpread", "Type": "double"},
                        {"Name": "OverUnder", "Type": "double"},
                        {"Name": "AwayTeamMoneyLine", "Type": "int"},
                        {"Name": "HomeTeamMoneyLine", "Type": "int"},
                        {"Name": "GlobalGameID", "Type": "int"},
                        {"Name": "GlobalAwayTeamID", "Type": "int"},
                        {"Name": "GlobalHomeTeamID", "Type": "int"},
                        {"Name": "PointSpreadAwayTeamMoneyLine", "Type": "int"},
                        {"Name": "PointSpreadHomeTeamMoneyLine", "Type": "int"},
                        {"Name": "LastPlay", "Type": "string"},
                        {"Name": "IsClosed", "Type": "boolean"},
                        {"Name": "GameEndDateTimed", "Type": "string"}, # Ojo con el nombre, lo mantengo como en la API
                        {"Name": "HomeRotationNumber", "Type": "int"},
                        {"Name": "AwayRotationNumber", "Type": "int"},
                        {"Name": "NeutralVenue", "Type": "boolean"},
                        {"Name": "OverPayout", "Type": "int"},
                        {"Name": "UnderPayout", "Type": "int"},
                        {"Name": "CrewChiefID", "Type": "int"},
                        {"Name": "UmpireID", "Type": "int"},
                        {"Name": "RefereeID", "Type": "int"},
                        {"Name": "AlternateID", "Type": "int"},
                        {"Name": "DateTimeUTC", "Type": "string"},
                        # SeriesInfo y Quarters son arrays de objetos. Para simplificar en este workshop inicial,
                        # si no se van a consultar a fondo sus sub-campos, se pueden omitir o declarar como STRING
                        # para que el SerDe los capture como una cadena JSON completa.
                        # {"Name": "SeriesInfo", "Type": "string"}, # Omitir o manejar con un tipo más complejo si es necesario
                        # {"Name": "Quarters", "Type": "string"}, # Omitir o manejar con un tipo más complejo si es necesario
                        {"Name": "InseasonTournament", "Type": "boolean"}
                    ],
                    "Location": f"s3://{bucket_name}/raw-data/",
                    "InputFormat": "org.apache.hadoop.mapred.TextInputFormat",
                    "OutputFormat": "org.apache.hadoop.hive.ql.io.HiveIgnoreKeyTextOutputFormat",
                    "SerdeInfo": {
                        "SerializationLibrary": "org.openx.data.jsonserde.JsonSerDe",
                        "Parameters": {
                            "ignore.malformed.json": "true"
                        }
                    },
                    "Compressed": False,
                },
                "TableType": "EXTERNAL_TABLE",
            },
        )
        print(f"Glue table 'nba_games' created successfully.")
    except Exception as e:
        print(f"Error creating Glue table: {e}")

def configure_athena():
    """Set up Athena output location."""
    try:
        # Aunque aquí solo creamos la base de datos si no existe,
        # la configuración del output location es crucial para cualquier query de Athena
        athena_client.start_query_execution(
            QueryString=f"CREATE DATABASE IF NOT EXISTS {glue_database_name}",
            ResultConfiguration={"OutputLocation": athena_output_location},
        )
        print("Athena output location configured successfully.")
    except Exception as e:
        print(f"Error configuring Athena: {e}")

def run_athena_query(query_string, database_name, output_location):
    """Executes an Athena query and prints the results."""
    try:
        print(f"\nExecuting Athena query:\n{query_string}")
        response = athena_client.start_query_execution(
            QueryString=query_string,
            QueryExecutionContext={"Database": database_name},
            ResultConfiguration={"OutputLocation": output_location},
        )
        query_execution_id = response["QueryExecutionId"]

        state = "RUNNING"
        while state in ["RUNNING", "QUEUED"]:
            query_status = athena_client.get_query_execution(
                QueryExecutionId=query_execution_id
            )
            state = query_status["QueryExecution"]["Status"]["State"]
            print(f"Query status: {state}")
            if state == "FAILED":
                print(
                    f"Query failed: {query_status['QueryExecution']['Status']['StateChangeReason']}"
                )
                return None
            elif state == "SUCCEEDED":
                print("Query succeeded!")
                break
            time.sleep(5)

        results = athena_client.get_query_results(
            QueryExecutionId=query_execution_id, MaxResults=100 # Puedes ajustar MaxResults
        )

        column_info = results["ResultSet"]["ResultSetMetadata"]["ColumnInfo"]
        column_names = [col["Name"] for col in column_info]
        print(f"Results for '{query_string.splitlines()[0].strip()}':")
        print(" | ".join(column_names))
        print("-" * (sum(len(name) for name in column_names) + (len(column_names) - 1) * 3))

        for row in results["ResultSet"]["Rows"][1:]:
            print(" | ".join([col.get("VarCharValue", "NULL") for col in row["Data"]]))
        return results

    except Exception as e:
        print(f"Error running Athena query: {e}")
        return None

# Main workflow
def main():
    print("Setting up data lake for NBA sports analytics...")
    create_s3_bucket()
    time.sleep(5)
    create_glue_database()

    print("\n--- Fetching and uploading NBA Game Data ---")
    nba_games = fetch_nba_games_data()
    if nba_games:
        upload_games_data_to_s3(nba_games)
    
    print("\n--- Creating Glue Table for NBA Games ---")
    create_glue_games_table()
    
    print("\n--- Configuring Athena Output Location ---")
    configure_athena()

    print("\n--- Executing Athena Queries for NBA Game Analysis ---")

    # Query 1: Asistencia total por equipo como local
    total_attendance_by_home_team_query = f"""
    SELECT
        "hometeam",
        SUM("attendance") AS total_attendance
    FROM
        "{glue_database_name}"."nba_games"
    WHERE
        "status" = 'Final'
        AND "attendance" IS NOT NULL
        AND "attendance" > 0
    GROUP BY
        "hometeam"
    ORDER BY
        total_attendance DESC;
    """
    run_athena_query(total_attendance_by_home_team_query, glue_database_name, athena_output_location)

    # Query 2: Asistencia promedio por estadio
    avg_attendance_by_stadium_query = f"""
    SELECT
        "stadiumid",
        AVG("attendance") AS average_attendance
    FROM
        "{glue_database_name}"."nba_games"
    WHERE
        "status" = 'Final'
        AND "attendance" IS NOT NULL
        AND "attendance" > 0
    GROUP BY
        "stadiumid"
    ORDER BY
        average_attendance DESC;
    """
    run_athena_query(avg_attendance_by_stadium_query, glue_database_name, athena_output_location)

    # Query 3: Top 5 partidos con mayor asistencia
    top_5_games_attendance_query = f"""
    SELECT
        "day",
        "hometeam",
        "awayteam",
        "attendance"
    FROM
        "{glue_database_name}"."nba_games"
    WHERE
        "status" = 'Final'
        AND "attendance" IS NOT NULL
        AND "attendance" > 0
    ORDER BY
        "attendance" DESC
    LIMIT 5;
    """
    run_athena_query(top_5_games_attendance_query, glue_database_name, athena_output_location)

    print("\nData lake setup complete and initial analysis queries executed.")

if __name__ == "__main__":
    main()