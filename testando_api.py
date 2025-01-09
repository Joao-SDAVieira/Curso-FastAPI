import requests

# URL da API para obtenção do token
def token():
    url_token = 'http://192.168.1.6:8000/token'

    # Credenciais
    email = 'useruser@example.com'
    senha = '123'

    data = {
        'username': email,
        'password': senha
    }

    # Cabeçalhos (se necessário)
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

    try:
        # Fazendo a requisição para obter o token
        response = requests.post(url_token, data=data, headers=headers)

        # Verificando se a requisição foi bem-sucedida
        if response.status_code == 200:
            # Extraindo o token da resposta
            print(response.json())
            token = response.json().get('access_token', None)
            return response.json()
            
        
        else:
            print(f'Erro ao obter token: {response.status_code} - {response.text}')

    except requests.RequestException as e:
        print(f'Erro na requisição: {e}')
        
meu_token = token()
print(meu_token)

def deletando(token):
    # URL base da API
    base_url = 'http://192.168.1.6:8000/users'

    # Recurso a ser deletado
    recurso_id = '10'

    # URL completa para a requisição DELETE
    url = f'{base_url}/{recurso_id}'

    # Cabeçalhos (incluindo token de autenticação, se necessário)
    headers = {
        'Authorization': f'Bearer {token}',  # Substitua SEU_TOKEN_AQUI pelo token real
    }

    try:
        # Fazendo a requisição DELETE
        response = requests.delete(url, headers=headers)

        # Verificando a resposta
        if response.status_code == 204:
            print(f'Recurso com ID {recurso_id} deletado com sucesso.')
        elif response.status_code == 404:
            print(f'Recurso com ID {recurso_id} não encontrado.')
        else:
            print(f'Erro ao deletar o recurso: {response.status_code} - {response.text}')

    except requests.RequestException as e:
        print(f'Erro na requisição DELETE: {e}')
deletando(meu_token)