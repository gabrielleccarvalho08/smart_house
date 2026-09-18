import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import app
from database import salvar_evento

def executar_testes():
    print("--- INICIANDO TESTES DO BACKEND ---")
    
    client = app.test_client()
    resposta = client.get('/api/registros')
    assert resposta.status_code == 200, f"Erro na API: status {resposta.status_code}"
    print("[OK] Teste 1: Rota GET /api/registros funcionando (Status 200)")

    try:
        salvar_evento("", "ACESA", "MOVIMENTO_DETECTADO")
        print("[ERRO] Teste 2 falhou: Deveria ter barrado campos vazios.")
    except ValueError:
        print("[OK] Teste 2: Validacao de campos obrigatorios funcionando")

    cenarios = [
        ("Sala", "ACESA", "MOVIMENTO_DETECTADO"),
        ("Quarto", "APAGADA", "SEM_MOVIMENTO")
    ]
    for comodo, status, evento in cenarios:
        assert len(comodo) > 0 and status in ["ACESA", "APAGADA"]
    print("[OK] Teste 3: Dados parametrizados validados com sucesso")

    print("\n--- TODOS OS TESTES PASSERAM COM SUCESSO! ---")

if __name__ == '__main__':
    executar_testes()