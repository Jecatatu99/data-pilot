# Data Pilot

Aplicação desenvolvida em Python para análise interativa de vendas. O projeto reúne um painel com indicadores e gráficos e uma interface de conversa em português para consultar métricas calculadas pelo próprio código.

## Sobre o projeto

O Data Pilot foi desenvolvido como projeto prático de análise de dados e integração de ferramentas.

A aplicação possui dois menus:

1. **Painel de vendas**
   - receita total;
   - pedidos concluídos;
   - ticket médio;
   - clientes únicos;
   - taxa de cancelamento;
   - receita média por cliente;
   - receita mensal;
   - cinco cidades com maior receita;
   - filtro por categoria.

2. **Converse com os dados**
   - recebe perguntas em português;
   - identifica a métrica solicitada;
   - seleciona uma função Python;
   - executa o cálculo;
   - apresenta a resposta;
   - informa qual ferramenta foi utilizada.

A regra central do projeto é:

> **O Python calcula e a camada de conversa apenas seleciona a ferramenta e explica o resultado.**

## Origem dos dados

A aplicação utiliza uma base fictícia criada exclusivamente para fins educacionais.

O arquivo original contém 603 registros, incluindo três duplicidades adicionadas intencionalmente para praticar a etapa de limpeza.

Após o tratamento, a base possui:

- 600 registros;
- 13 colunas;
- zero duplicidades;
- zero valores ausentes;
- zero datas inválidas.

Os dados não representam clientes, pedidos ou transações reais.

## Estrutura dos dados

A base tratada possui as seguintes colunas:

| Coluna | Descrição |
|---|---|
| `order_id` | Identificador do pedido |
| `order_date` | Data do pedido |
| `customer_id` | Identificador do cliente |
| `customer_name` | Nome fictício do cliente |
| `category` | Categoria do produto |
| `product` | Produto |
| `city` | Cidade |
| `state` | Estado |
| `quantity` | Quantidade |
| `unit_price` | Preço unitário |
| `status` | Situação do pedido |
| `payment_method` | Forma de pagamento |
| `revenue` | Receita calculada |

A receita é calculada por:

```text
revenue = quantity * unit_price
```

## Indicadores do painel

Considerando todas as categorias, os resultados da base são:

| Indicador | Resultado |
|---|---:|
| Receita total | R$ 1.457.854,66 |
| Pedidos concluídos | 459 |
| Ticket médio | R$ 3.176,15 |
| Clientes únicos | 171 |
| Taxa de cancelamento | 13,33% |
| Receita média por cliente | R$ 8.525,47 |

As métricas monetárias, os pedidos e os clientes únicos consideram somente pedidos com status `Concluido`.

A taxa de cancelamento compara os pedidos com status `Cancelado` com o total de pedidos.

## Melhorias implementadas

Além dos requisitos principais, foram implementadas:

### Receita média por cliente

```text
Receita média por cliente =
Receita total dos pedidos concluídos / clientes únicos
```

### Cinco cidades com maior receita

Gráfico horizontal que apresenta as cinco cidades com maior receita de pedidos concluídos.

### Filtro compartilhado

O filtro de categoria afeta:

- cards;
- gráficos;
- amostra dos dados;
- respostas da conversa.

### Tratamento de erros

A aplicação trata:

- arquivo ausente;
- base vazia;
- colunas obrigatórias ausentes;
- pergunta fora do escopo;
- ferramenta inválida;
- indisponibilidade do provedor externo.

## Ferramentas disponíveis

| Ferramenta | Finalidade |
|---|---|
| `calculate_total_