import psycopg2

def connect():
    conn = psycopg2.connect(
      database="linking_park", user='postgres', password='RTvAsfCAv3neSn', host='serverproyectoxdbbdd.postgres.database.azure.com ', port= '5432'
   )
    return conn