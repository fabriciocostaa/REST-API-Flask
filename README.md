# API de Gestão de Hotéis

Uma API RESTful desenvolvida em Flask para gerenciar informações de hotéis, permitindo operações de CRUD (Create, Read, Update, Delete). A API suporta filtros dinâmicos, como faixa de preço, estrelas e localização, para facilitar a busca de hotéis. O relacionamento entre as tabelas de **sites** e **hotéis** é do tipo "um para muitos", onde um site pode ter muitos hotéis.

## Funcionalidades

### **Autenticação e Usuários**
- **POST /cadastro**: Cria um usuário no sistema. exemplo:
  ```text 
{ "login" : "usuario"
"email" : "teste@gmail.com"
"senha" : "abc"
} ```

- **POST /login**: Realiza o login e retorna um token JWT, necessário para autenticação nas operações de CRUD em hotéis.
- **POST /logout**: Finaliza a sessão do usuário, invalidando o token JWT.
- **GET /usuarios/{user_id}**: Recupera dados do usuário com base no `user_id`.
- **DELETE /usuarios/{user_id}**: Deleta o usuário do sistema.

### **Gestão de Hotéis**
- **GET /hoteis**: Recupera uma lista de hotéis, com suporte a filtros opcionais como:
  - `cidade`: Filtra os hotéis por cidade.
  - `estrelas_min` e `estrelas_max`: Intervalo de estrelas do hotel.
  - `diaria_min` e `diaria_max`: Intervalo de preço da diária.
  - `limit` e `offset`: Paginação de resultados.
  
- **GET /hoteis/{hotel_id}**: Recupera detalhes de um hotel específico com base no `hotel_id`.

- **POST /hoteis/{hotel_id}**: Cria um novo hotel. **(Requer token de autenticação no header)** exemplo: 
  ```text 
{ "hotel_id": "teste1"
"nome" : "hotel1",
"estrelas" : 5.0,
"diaria" : 500,
"cidade" : Santo André,
"site_id" : 1
} ```

- **PUT /hoteis/{hotel_id}**: Atualiza as informações de um hotel existente. **(Requer token de autenticação no header)**

- **DELETE /hoteis/{hotel_id}**: Remove um hotel do banco de dados. **(Requer token de autenticação no header)**

### **Sites**
- **GET /sites** : Recupera uma lista com os sites cadastrados.
- **POST /sites/{url_site}** : Cadastra um novo site. `Não precisa de body`
- **PUT /sites/{url_site}** : Atualiza os sites. `Não precisa de body`
- **DELETE /sites/{url_site}**: Deleta site com todos os hotéis associado ao site. 

## Tecnologias Utilizadas

- **Python**
- **Flask** e **Flask-RESTful**
- **Flask-JWT-Extended**: Autenticação baseada em JWT.
- **SQLAlchemy**: ORM para manipulação do banco de dados.
- **SQLite**: Banco de dados relacional.
- **Blacklist**: Para gerenciamento de tokens revogados.
- **SendGrid**: Para envio de e-mail e confirmação da conta.

## Requisitos

- **Content-Type**: Todas as operações `POST` e `PUT` requerem que o cabeçalho `Content-Type` seja configurado para `application/json`.

### **Cabeçalhos obrigatórios**
1. **Autenticação**: Para as operações de `logout`, `deletar usuário`, `criar novo hotel`, `atualizar hotel`, e `deletar hotel`, o cabeçalho `Authorization` deve conter o token JWT válido:
   ```text
   Authorization: Bearer {token}
