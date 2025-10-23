#!/usr/bin/env python3
"""
Script de teste de integração para validar endpoints do Equil API
"""

import requests
import json
from datetime import datetime, timedelta

# URL base da API
API_BASE_URL = "https://dyh6i3ceqlmz.manus.space/api"

# Dados de teste
test_user = {
    "nome": "Teste Integration",
    "email": f"test_{datetime.now().timestamp()}@test.com",
    "senha": "TestPassword123!",
    "data_nascimento": "1990-01-15",
    "sexo": "M",
    "altura": 180,
    "peso_inicial": 80,
    "objetivo": "ganhar_massa"
}

def test_auth():
    """Testa autenticação"""
    print("\n=== TESTANDO AUTENTICAÇÃO ===")
    
    # Registro
    print("1. Testando registro...")
    response = requests.post(f"{API_BASE_URL}/auth/register", json=test_user)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        data = response.json()
        token = data.get('access_token')
        usuario_id = data.get('usuario', {}).get('id')
        print(f"✓ Registro bem-sucedido")
        print(f"  Token: {token[:20]}...")
        print(f"  Usuário ID: {usuario_id}")
        return token, usuario_id
    else:
        print(f"✗ Erro no registro: {response.text}")
        return None, None

def test_recomendacoes(token, usuario_id):
    """Testa geração de recomendações"""
    print("\n=== TESTANDO RECOMENDAÇÕES ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    print("1. Testando geração de recomendações...")
    response = requests.post(
        f"{API_BASE_URL}/recomendacoes",
        json={"usuario_id": usuario_id, "limite": 3},
        headers=headers
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        data = response.json()
        print(f"✓ Recomendações geradas com sucesso")
        print(f"  Recomendações gerais: {len(data.get('recomendacoes_gerais', []))}")
        print(f"  Recomendações de suplementos: {len(data.get('recomendacoes_suplementos', []))}")
        return data
    else:
        print(f"✗ Erro ao gerar recomendações: {response.text}")
        return None

def test_refeicoes(token, usuario_id):
    """Testa criação de refeições"""
    print("\n=== TESTANDO REFEIÇÕES ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Primeiro, criar um alimento
    print("1. Testando criação de alimento...")
    alimento_data = {
        "nome": "Frango Grelhado",
        "categoria": "Proteína",
        "calorias": 165,
        "proteinas": 31,
        "carboidratos": 0,
        "gorduras": 3.6,
        "fibras": 0,
        "marca": "Teste",
        "porcao": "100g"
    }
    
    response = requests.post(
        f"{API_BASE_URL}/alimentos",
        json=alimento_data,
        headers=headers
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 201:
        alimento = response.json()
        alimento_id = alimento.get('id')
        print(f"✓ Alimento criado com sucesso (ID: {alimento_id})")
        
        # Agora criar um registro de refeição
        print("2. Testando criação de registro de refeição...")
        refeicao_data = {
            "alimento_id": alimento_id,
            "data_refeicao": datetime.now().strftime("%Y-%m-%d"),
            "tipo_refeicao": "Almoço",
            "quantidade": 150,
            "observacoes": "Teste"
        }
        
        response = requests.post(
            f"{API_BASE_URL}/registros_refeicao",
            json=refeicao_data,
            headers=headers
        )
        print(f"Status: {response.status_code}")
        
        if response.status_code == 201:
            print(f"✓ Registro de refeição criado com sucesso")
        else:
            print(f"✗ Erro ao criar registro de refeição: {response.text}")
    else:
        print(f"✗ Erro ao criar alimento: {response.text}")

def test_treinos(token, usuario_id):
    """Testa criação de treinos"""
    print("\n=== TESTANDO TREINOS ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Primeiro, listar exercícios disponíveis
    print("1. Listando exercícios disponíveis...")
    response = requests.get(
        f"{API_BASE_URL}/exercicios",
        headers=headers
    )
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        exercicios = response.json()
        if exercicios:
            exercicio_id = exercicios[0].get('id')
            print(f"✓ {len(exercicios)} exercícios encontrados")
            print(f"  Usando exercício ID: {exercicio_id}")
            
            # Criar um treino
            print("2. Testando criação de treino...")
            treino_data = {
                "nome": "Treino Teste",
                "tipo": "musculacao",
                "duracao_minutos": 60,
                "calorias_queimadas": 300,
                "observacoes": "Teste de integração",
                "exercicios": [
                    {
                        "biblioteca_exercicio_id": exercicio_id,
                        "series": 3,
                        "repeticoes": 10,
                        "carga": 50,
                        "observacoes": "Teste"
                    }
                ]
            }
            
            response = requests.post(
                f"{API_BASE_URL}/treinos",
                json=treino_data,
                headers=headers
            )
            print(f"Status: {response.status_code}")
            
            if response.status_code == 201:
                print(f"✓ Treino criado com sucesso")
            else:
                print(f"✗ Erro ao criar treino: {response.text}")
        else:
            print("✗ Nenhum exercício disponível")
    else:
        print(f"✗ Erro ao listar exercícios: {response.text}")

def main():
    print("=" * 50)
    print("TESTE DE INTEGRAÇÃO - EQUIL API")
    print("=" * 50)
    
    # Teste de autenticação
    token, usuario_id = test_auth()
    
    if token and usuario_id:
        # Teste de recomendações
        test_recomendacoes(token, usuario_id)
        
        # Teste de refeições
        test_refeicoes(token, usuario_id)
        
        # Teste de treinos
        test_treinos(token, usuario_id)
        
        print("\n" + "=" * 50)
        print("TESTES CONCLUÍDOS")
        print("=" * 50)
    else:
        print("\n✗ Falha na autenticação. Testes abortados.")

if __name__ == "__main__":
    main()

