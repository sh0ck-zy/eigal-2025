import requests
import sys

def test_api():
    """
    Testa os principais endpoints da API
    """
    BASE_URL = "http://localhost:8000/api"
    
    # Testar endpoint de tipos de impressão
    try:
        print("Testando endpoint de tipos de impressão...")
        response = requests.get(f"{BASE_URL}/print-types")
        
        if response.status_code == 200:
            print(f"Sucesso! Status: {response.status_code}")
            print(f"Tipos de impressão: {response.json()}")
        else:
            print(f"Erro! Status: {response.status_code}")
            print(f"Resposta: {response.text}")
    except Exception as e:
        print(f"Erro ao acessar endpoint de tipos de impressão: {e}")
    
    print("\n" + "-" * 50 + "\n")
    
    # Testar endpoint de cálculo de desperdício
    try:
        print("Testando endpoint de cálculo de desperdício...")
        params = {
            "print_type": "4/0",
            "print_run": 1000
        }
        
        response = requests.get(f"{BASE_URL}/waste-calculation", params=params)
        
        if response.status_code == 200:
            print(f"Sucesso! Status: {response.status_code}")
            result = response.json()
            print(f"Tipo: {result['print_type']}")
            print(f"Tiragem: {result['print_run']}")
            print(f"Desperdício: {result['waste_amount']} folhas")
            if result.get('adjustment'):
                print(f"Ajuste: {result['adjustment']}")
            if result.get('is_special_case'):
                print("ATENÇÃO: Este é um caso especial!")
        else:
            print(f"Erro! Status: {response.status_code}")
            print(f"Resposta: {response.text}")
    except Exception as e:
        print(f"Erro ao acessar endpoint de cálculo de desperdício: {e}")

if __name__ == "__main__":
    test_api() 