# API de Gestão de Hotéis

Uma API RESTful desenvolvida em Flask para gerenciar informações de hotéis, permitindo operações de CRUD (Create, Read, Update, Delete). A API suporta filtros dinâmicos, como faixa de preço, estrelas e localização, para facilitar a busca de hotéis.

## Funcionalidades

- **GET /hoteis**: Recupera uma lista de hotéis, com suporte a filtros opcionais como:
  - `cidade`: Filtrar por cidade.
  - `estrelas_min` e `estrelas_max`: Intervalo de estrelas do hotel.
  - `diaria_min` e `diaria_max`: Intervalo de preço da diária.
  - `limit` e `offset`: Paginação de resultados.
  
- **GET /hoteis/{hotel_id}**: Recupera detalhes de um hotel específico.

- **POST /hoteis/{hotel_id}**: Cria um novo hotel.

- **PUT /hoteis/{hotel_id}**: Atualiza informações de um hotel existente.

- **DELETE /hoteis/{hotel_id}**: Remove um hotel do banco de dados.

## Tecnologias Utilizadas

- **Python 3.12**
- **Flask** e **Flask-RESTful**
- **Flask-JWT-Extended**: Autenticação baseada em JWT.
- **SQLAlchemy**: ORM para manipulação do banco de dados.
- **SQLite**: Banco de dados relacional.
