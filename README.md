# API De Carrinho de Compras

Esse projeto é uma API REST que simula funcionalidades de um carrinho de compras

### Principais Tecnologias utilizadas

- Python 3.9.7
- Flask Framework 2.0.2
- Mysql 8

### Setup opção 1 (Sem docker)

É necessário ter instalado e funcionando:

- Python 3.9.7
- Mysql 8 (**o mysql precisa estar stardado corretamente**)
- Git (para clonar o projeto)

1. Clonar o projeto:

    `git clone https://github.com/armandodelcol-coder/shopping-cart-challenge`


2. Instalar as dependências:

    Acesse com o terminal a pasta raiz do projeto e rode o comando:

    windows: `pip install -r .\requirements.txt`

    linux: `pip install -r requirements.txt`


3. Iniciar o banco de dados e rodar a aplicação

    **Atenção: os arquivos create_db.py e .env estão
    com a url de conexão para o mysql com usuário root
    e senha 123, configure de acordo com o seu ambiente**

    Acesse com o terminal a pasta raiz do projeto e
    
    para iniciar o banco de dados:

    windows: `python .\create_db.py`

    linux: `python create_db.py`

### Setup opção 2 (com docker)

É necessário ter instalado e funcionando:

- Docker e docker-compose

1. Clonar o projeto:

    `git clone https://github.com/armandodelcol-coder/shopping-cart-challenge`


2. Rodar o projeto:

    Acesse com o terminal a pasta raiz do projeto e execute o comando:

    `docker-compose run`

    **Obs: as portas 3306 e 5000 devem estar livres**

## Sobre testes

O projeto foi desenvolvido com a prática de TDD com testes de integração
realizando as chamadas paras as APIs, o projeto está com 100% de cobertura
e com muitos casos de uso testados.

Comando para rodar os testes com cobertura:

`python -m pytest .\tests\ --cov .\src\`

## Utilizando a API

*Disponibilizei uma collection do Postman com exemplos prontos para
serem utilizados*

arquivo: challenge-shopping-cart.postman_collection.json

A api disponibiliza 10 endpoints:

### Listar produtos

REQUEST:

GET para /products

ex: http://localhost:5000/products

RESPONSE:

status 200:

{
    "products": [
        {}
    ]
}

### Mostrar produto

REQUEST

GET para /produtos/product_id

ex: http://localhost:5000/products/c92b2b5c-809a-11ec-a47e-0242c0a89002

RESPONSE:

status 200:

```json
{
    "id": "c92b2b5c-809a-11ec-a47e-0242c0a89002",
    "name": "PRODUTO A",
    "price": "10.99",
    "stock": 5
}
```

status 404:

{}

### Criar Carrinho de compras

REQUEST:

POST para /shoppingcarts

ex: http://localhost:5000/shoppingcarts

enviando um json body:

```json
{
  "items": [
    {
      "product_id": "c92b2b5c-809a-11ec-a47e-0242c0a89002",
      "quantity": 1
    },
    {
      "product_id": "c92c2946-809a-11ec-a47e-0242c0a89002",
      "quantity": 1
    },
    {
      "product_id": "c92cdbba-809a-11ec-a47e-0242c0a89002",
      "quantity": 1
    }
  ]
}
```
podendo enviar items ou não.

RESPONSE:

status 201:

```json
{
    "id": "6bc6d486-95b3-4b20-9afc-fb24ba096cc9"
}
```

status 422
quando o estoque não é o bastante para a quantidade desejada:

````json
{
    "message": "Estoque não é suficiente para o produto: c92b2b5c-809a-11ec-a47e-0242c0a89002"
}
````

status 422
quando faz uma requisição sem enviar a propriedades items:

````json
{
    "message": "Deve informar uma lista de items"
}
````

status 422
quando informa um item sem os atributos necessários que são product_id e quantity:

````json
{
    "message": "Atributo: product_id não informado. Verifique se o item contem product_id e quantity"
}
````

### Adicionando item no carrinho

*Obs: quando o produto já existe, a quantidade é somada*

REQUEST:

POST para /shoppingcarts/cart_id

ex: http://localhost:5000/shoppingcarts/510193a1-d025-4467-8179-1716e51182af

enviando um json body:

````json
{
    "product_id": "c92cdbba-809a-11ec-a47e-0242c0a89002",
    "quantity": 2
}
````

RESPONSE:

status 200:

````json
{
    "id": "aa27b5ac-73df-42ef-97f5-29da40d34589",
    "items": [
        {
            "name": "PRODUTO A",
            "price": "10.99",
            "product_id": "c92b2b5c-809a-11ec-a47e-0242c0a89002",
            "quantity": 2,
            "subtotal": "21.98"
        }
    ],
    "total": "21.98"
}
````

status 404
quando carrinho não encontrado:

````json
{
    "message": "Carrinho não encontrado"
}
````

status 422
quando o estoque for insuficiente para quantidade desejada.


status 422
quando o produto não for encontrado:

````json
{
    "message": "Não foi encontrado o produto com id: c92b2b5c-809a-11ec-a47e-0242c0a89002-"
}
````

status 422
quando quantiade for menor ou igual a 0:

````json
{
    "message": "Quantidade deve ser maior que zero"
}
````

### Remover um item do carrinho

REQUEST:

DELETE para /shoppingcarts/cart_id/product_id

ex: http://localhost:5000/shoppingcarts/aa27b5ac-73df-42ef-97f5-29da40d34589/c92b2b5c-809a-11ec-a47e-0242c0a89002

RESPONSE:

status 200:

````json
{
    "id": "aa27b5ac-73df-42ef-97f5-29da40d34589",
    "items": [],
    "total": "0.00"
}
````

status 404
quando carrinho não encontrado

status 422
quando produto não econtrado no carrinho

````json
{
    "message": "Produto de id c92b2b5c-809a-11ec-a47e-0242c0a89002 não foi encontrado no carrinho"
}
````

### Atualizar quantidade de item no carrinho

REQUEST:

PATCH para /shoppingcarts/cart_id

ex: http://localhost:5000/shoppingcarts/6d99388f-2d90-42a8-b245-a17c604d1626

envinado o body:

````json
{
    "product_id": "057d5d27-2ef4-4f84-a1eb-9f0e0b3c406b",
    "quantity": 3
}
````

RESPONSE:

status 200
com a quantidade do item atualizada:

````json
{
    "id": "057d5d27-2ef4-4f84-a1eb-9f0e0b3c406b",
    "items": [
        {
            "name": "PRODUTO A",
            "price": "10.99",
            "product_id": "c92b2b5c-809a-11ec-a47e-0242c0a89002",
            "quantity": 3,
            "subtotal": "32.97"
        }
    ],
    "total": "32.97"
}
````

status 404
quando carrinho não encontrado

status 422
quando produto não está no carrinho

status 422
quando estoque insuficiente

status 422
quando quantidade a atualziar for menor ou igual a 0

### Limpar carrinho

REQUEST:

POST para /shoppingcarts/cart_id/clear

ex: http://localhost:5000/shoppingcarts/3bd74f72-ce23-40e1-9dde-fceb52868f10/clear

RESPONSE:

status 200:

````json
{
    "id": "3bd74f72-ce23-40e1-9dde-fceb52868f10",
    "items": [],
    "total": "0.00"
}
````

status 404
quando carrinho não encontrado

### Mostrar carrinho

REQUEST:

GET para /shoppingcarts/cart_id

ex: http://localhost:5000/shoppingcarts/3bd74f72-ce23-40e1-9dde-fceb52868f10

RESPONSE:

status 200:

````json
{
    "discount": "0",
    "id": "510193a1-d025-4467-8179-1716e51182af",
    "items": [
        {
            "name": "PRODUTO A",
            "price": "10.99",
            "product_id": "c92b2b5c-809a-11ec-a47e-0242c0a89002",
            "quantity": 1,
            "subtotal": "10.99"
        },
        {
            "name": "PRODUTO B",
            "price": "1.99",
            "product_id": "c92c2946-809a-11ec-a47e-0242c0a89002",
            "quantity": 1,
            "subtotal": "1.99"
        },
        {
            "name": "PRODUTO C",
            "price": "5.00",
            "product_id": "c92cdbba-809a-11ec-a47e-0242c0a89002",
            "quantity": 2,
            "subtotal": "10.00"
        },
        {
            "name": "PRODUTO F",
            "price": "12.00",
            "product_id": "c92f3ea8-809a-11ec-a47e-0242c0a89002",
            "quantity": 1,
            "subtotal": "12.00"
        }
    ],
    "subtotal": "34.98",
    "total": "34.98"
}
````

status 404
quando carrinho não encontrado

### Listar Cupons

REQUEST:

GET para /shoppingcarts/coupons

ex: http://localhost:5000/shoppingcarts/coupons

RESPONSE:

status 200:
retorna uma lista de cupons

### Adicionar cupom ao carrinho

REQUEST:

GET para /shoppingcarts/coupons

ex: http://localhost:5000/shoppingcarts/cart_id/add-coupon

envinado o json:

````json
{
    "code": "VALE12"
}
````

RESPONSE:

status 200
cupom adicionado com sucesso

status 404
quando carrinho não econtrado

status 404
quando o cupom não existe

status 422
quando o cupom não for mais válido

### Exemplo de carrinho completo com cupom de desconto aplicado

````json
{
    "discount": "3.50",
    "id": "510193a1-d025-4467-8179-1716e51182af",
    "items": [
        {
            "name": "PRODUTO A",
            "price": "10.99",
            "product_id": "c92b2b5c-809a-11ec-a47e-0242c0a89002",
            "quantity": 1,
            "subtotal": "10.99"
        },
        {
            "name": "PRODUTO B",
            "price": "1.99",
            "product_id": "c92c2946-809a-11ec-a47e-0242c0a89002",
            "quantity": 1,
            "subtotal": "1.99"
        },
        {
            "name": "PRODUTO C",
            "price": "5.00",
            "product_id": "c92cdbba-809a-11ec-a47e-0242c0a89002",
            "quantity": 2,
            "subtotal": "10.00"
        },
        {
            "name": "PRODUTO F",
            "price": "12.00",
            "product_id": "c92f3ea8-809a-11ec-a47e-0242c0a89002",
            "quantity": 1,
            "subtotal": "12.00"
        }
    ],
    "subtotal": "34.98",
    "total": "31.48"
}
````