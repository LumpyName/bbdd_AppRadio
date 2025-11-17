from supabase import create_client, Client

from zone_pruebas.recurso_to_JSON import leer_json

SUPABASE_URL = "https://cvzscfcciaegdgnyrkgg.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6ImN2enNjZmNjaWFlZ2Rnbnlya2dnIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NjA3OTQwMjMsImV4cCI6MjA3NjM3MDAyM30.dmAE84YXEtc9667I3b31fehIn_m8-9DIyBGrpppDRMY"

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

def agregar_contenido(data: dict):
    response = supabase.table("content").insert(data).execute()
    return response

# Ejemplo:
res = agregar_contenido(leer_json(12))

print(res)

