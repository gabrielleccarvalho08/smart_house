import os
import psycopg2

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://neondb_owner:npg_Ybcm2hKrGyl1@ep-cool-breeze-ac9khus8-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require&channel_binding=require")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL)

def criar_tabelas():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS registros_iluminacao (
            id SERIAL PRIMARY KEY,
            comodo VARCHAR(50) NOT NULL DEFAULT 'Sala',
            status_luz VARCHAR(20) NOT NULL,
            evento VARCHAR(50) NOT NULL,
            data_hora TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()
    cur.close()
    conn.close()

def salvar_evento(comodo, status_luz, evento):
    if not comodo or not status_luz or not evento:
        raise ValueError("Todos os campos sao obrigatorios")
        
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO registros_iluminacao (comodo, status_luz, evento) VALUES (%s, %s, %s);",
        (comodo, status_luz, evento)
    )
    conn.commit()
    cur.close()
    conn.close()
    return True

if __name__ == "__main__":
    try:
        print("Tentando conectar ao Neon...")
        criar_tabelas()
        print("Tabela verificada/criada com sucesso!")
        
        salvar_evento("Sala", "ACESA", "TESTE_MANUAL_VSCODE")
        print("Evento de teste salvo com sucesso no banco Neon!")
    except Exception as e:
        print(f"Erro ao conectar ou salvar no banco: {e}")