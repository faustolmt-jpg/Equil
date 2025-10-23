# Documentação Completa do Projeto Equil

Esta documentação detalha o desenvolvimento do aplicativo web "Equil", abordando a implementação da nova identidade visual, correção de erros críticos e a adição de funcionalidades de acompanhamento de medidas corporais, humor, aprimoramento do dashboard e integração de dropshipping.

## Sumário

1.  [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2.  [Configuração do Ambiente](#2-configuração-do-ambiente)
3.  [Backend (vidafit_backend)](#3-backend-vidafit_backend)
    *   [Estrutura do Projeto](#estrutura-do-projeto-backend)
    *   [Modelos de Dados](#modelos-de-dados-backend)
    *   [Rotas da API](#rotas-da-api-backend)
    *   [Serviços](#serviços-backend)
    *   [Correções de Erros Críticos](#correções-de-erros-críticos)
4.  [Frontend (vidafit-frontend)](#4-frontend-vidafit-frontend)
    *   [Estrutura do Projeto](#estrutura-do-projeto-frontend)
    *   [Componentes Principais](#componentes-principais-frontend)
    *   [Serviços de API](#serviços-de-api-frontend)
    *   [Implementação da Nova Identidade Visual](#implementação-da-nova-identidade-visual)
    *   [Novas Funcionalidades](#novas-funcionalidades-frontend)
5.  [Conclusão](#5-conclusão)

---

## 1. Visão Geral do Projeto

O projeto Equil é um aplicativo web focado em bem-estar e saúde, oferecendo funcionalidades para acompanhamento de dieta, treinos, medidas corporais, humor e recomendações personalizadas por IA. Ele também inclui uma loja de suplementos integrada com dropshipping.

## 2. Configuração do Ambiente

Para configurar e executar o projeto localmente, siga as instruções detalhadas nos `README.md` de cada subprojeto (`vidafit_backend` e `vidafit-frontend`).

## 3. Backend (vidafit_backend)

O backend é construído com Flask e SQLAlchemy, fornecendo a API RESTful para o frontend.

### Estrutura do Projeto (Backend)

```
vidafit_backend/
├── src/
│   ├── models/             # Definições dos modelos de dados (SQLAlchemy)
│   │   ├── __init__.py
│   │   ├── usuario.py
│   │   ├── medida_corporal.py
│   │   ├── registro_humor.py
│   │   └── ... (outros modelos)
│   ├── routes/             # Definições das rotas da API (Blueprints)
│   │   ├── __init__.py
│   │   ├── auth.py
│   │   ├── medidas_corporais.py
│   │   ├── registros_humor.py
│   │   └── ... (outras rotas)
│   ├── services/           # Lógica de negócio e integração com serviços externos
│   │   ├── ia_recomendacao.py
│   │   └── ...
│   ├── utils/              # Utilitários (autenticação, etc.)
│   │   └── auth.py
│   └── main.py             # Ponto de entrada da aplicação Flask
├── .env.example            # Exemplo de variáveis de ambiente
├── requirements.txt        # Dependências Python
└── README.md               # Documentação específica do backend
```

### Modelos de Dados (Backend)

#### `MedidaCorporal`

Modelo para armazenar medidas corporais dos usuários.

| Campo             | Tipo      | Descrição                                         |
| :---------------- | :-------- | :------------------------------------------------ |
| `id`              | `Integer` | Chave primária                                    |
| `usuario_id`      | `Integer` | Chave estrangeira para `Usuario`                  |
| `data_medicao`    | `DateTime`| Data e hora da medição                            |
| `peso`            | `Float`   | Peso em kg                                        |
| `braco`           | `Float`   | Circunferência do braço em cm                     |
| `peito`           | `Float`   | Circunferência do peito em cm                     |
| `coxa`            | `Float`   | Circunferência da coxa em cm                      |
| `quadril`         | `Float`   | Circunferência do quadril em cm                   |
| `panturrilha`     | `Float`   | Circunferência da panturrilha em cm               |
| `cintura`         | `Float`   | Circunferência da cintura em cm                   |

#### `RegistroHumor`

Modelo para armazenar registros de humor e bem-estar dos usuários.

| Campo                 | Tipo        | Descrição                                         |
| :-------------------- | :---------- | :------------------------------------------------ |
| `id`                  | `Integer`   | Chave primária                                    |
| `usuario_id`          | `Integer`   | Chave estrangeira para `Usuario`                  |
| `data_registro`       | `DateTime`  | Data e hora do registro                           |
| `humor`               | `Integer`   | Nível de humor (1-10)                             |
| `energia`             | `Integer`   | Nível de energia (1-10)                           |
| `estresse`            | `Integer`   | Nível de estresse (1-10)                          |
| `sono`                | `Integer`   | Qualidade do sono (1-10)                          |
| `motivacao`           | `Integer`   | Nível de motivação (1-10)                         |
| `dormiu_bem`          | `Boolean`   | Indicador se dormiu bem                           |
| `teve_ansiedade`      | `Boolean`   | Indicador se teve ansiedade                       |
| `sentiu_deprimido`    | `Boolean`   | Indicador se sentiu deprimido                     |
| `teve_dor`            | `Boolean`   | Indicador se teve dor                             |
| `notas`               | `Text`      | Observações adicionais                            |

### Rotas da API (Backend)

#### Medidas Corporais (`/api/medidas_corporais`)

| Método | Endpoint                    | Descrição                                 |
| :----- | :-------------------------- | :---------------------------------------- |
| `POST` | `/`                         | Cria um novo registro de medida corporal  |
| `GET`  | `/`                         | Lista todas as medidas corporais do usuário |
| `GET`  | `/<int:medida_id>`          | Obtém uma medida corporal específica      |
| `PUT`  | `/<int:medida_id>`          | Atualiza uma medida corporal existente    |
| `DELETE`| `/<int:medida_id>`          | Deleta uma medida corporal                |
| `GET`  | `/evolucao/<tipo>`          | Obtém a evolução de uma medida específica |
| `GET`  | `/ultima`                   | Obtém a última medida corporal registrada |

#### Registros de Humor (`/api/registros_humor`)

| Método | Endpoint                    | Descrição                                 |
| :----- | :-------------------------- | :---------------------------------------- |
| `POST` | `/`                         | Cria um novo registro de humor            |
| `GET`  | `/`                         | Lista todos os registros de humor do usuário |
| `GET`  | `/<int:registro_id>`        | Obtém um registro de humor específico     |
| `PUT`  | `/<int:registro_id>`        | Atualiza um registro de humor existente   |
| `DELETE`| `/<int:registro_id>`        | Deleta um registro de humor               |
| `GET`  | `/dia/<data>`               | Obtém o registro de humor de um dia específico |
| `GET`  | `/estatisticas/<dias>`      | Obtém estatísticas de humor dos últimos N dias |
| `GET`  | `/ultima`                   | Obtém o último registro de humor registrado |

#### Outras Rotas (Principais)

*   `/api/auth/register`: Registro de usuário
*   `/api/auth/login`: Login de usuário
*   `/api/usuarios/<int:usuario_id>/foto`: Upload de foto de perfil
*   `/api/recomendacoes`: Geração e listagem de recomendações de IA
*   `/api/alimentos`: CRUD de alimentos
*   `/api/registros_refeicao`: CRUD de registros de refeição
*   `/api/treinos`: CRUD de treinos
*   `/api/dropshipping/suplementos`: Gerenciamento de suplementos para dropshipping

### Serviços (Backend)

*   **`ia_recomendacao.py`**: Serviço responsável por gerar recomendações personalizadas de dieta, treino e suplementos utilizando modelos de IA.

### Correções de Erros Críticos

Durante o desenvolvimento, foram identificadas e corrigidas as seguintes questões críticas:

*   **Rota de Upload de Foto**: A rota de upload de foto no backend (`src/routes/usuarios.py`) foi ajustada para `/foto` para corresponder à chamada do frontend, resolvendo um problema de acesso ao endpoint.
*   **Indentação no Serviço de IA**: Corrigida uma falha de indentação na função `analisar_perfil_nutricional` em `src/services/ia_recomendacao.py`, que causava um erro interno no servidor (500) ao gerar recomendações.
*   **Retorno de ID na Criação de Alimento**: O endpoint de criação de alimento (`/api/alimentos`) foi modificado para retornar explicitamente o `id` do alimento criado na resposta JSON, facilitando a integração com o frontend.

## 4. Frontend (vidafit-frontend)

O frontend é desenvolvido em React, utilizando Tailwind CSS para estilização e Lucide Icons para ícones.

### Estrutura do Projeto (Frontend)

```
vidafit-frontend/
├── public/
├── src/
│   ├── assets/             # Imagens, ícones, etc.
│   ├── components/         # Componentes React reutilizáveis
│   │   ├── Layout.jsx
│   │   ├── DashboardMetricas.jsx
│   │   ├── MedidasCorporais.jsx
│   │   ├── AcompanhamentoHumor.jsx
│   │   └── ...
│   ├── pages/              # Páginas principais da aplicação
│   │   ├── Login.jsx
│   │   ├── Dashboard.jsx
│   │   ├── Suplementos.jsx
│   │   ├── Carrinho.jsx
│   │   ├── Perfil.jsx
│   │   └── ...
│   ├── services/           # Funções de interação com a API do backend
│   │   └── api.js
│   ├── App.css             # Estilos globais
│   ├── App.jsx             # Componente raiz do React, define rotas
│   ├── main.jsx            # Ponto de entrada da aplicação React
│   └── index.css           # Estilos Tailwind CSS
├── package.json            # Dependências Node.js
├── tailwind.config.js      # Configuração do Tailwind CSS
└── README.md               # Documentação específica do frontend
```

### Componentes Principais (Frontend)

*   **`Layout.jsx`**: Componente de layout principal que define a estrutura da página, incluindo cabeçalho, navegação lateral/superior e rodapé. Foi atualizado com a nova identidade visual Equil.
*   **`DashboardMetricas.jsx`**: Novo componente para exibir um resumo visual das métricas do usuário no Dashboard, incluindo IMC, peso atual, humor, bem-estar geral, gráficos de evolução e distribuição de macronutrientes.
*   **`MedidasCorporais.jsx`**: Novo componente para o Perfil do usuário, permitindo registrar, visualizar e acompanhar a evolução de medidas corporais (peso, braço, peito, coxa, quadril, panturrilha, cintura) com gráficos interativos.
*   **`AcompanhamentoHumor.jsx`**: Novo componente para o Dashboard, que permite ao usuário registrar seu humor e outros indicadores de bem-estar (energia, estresse, sono, motivação), além de visualizar um histórico e estatísticas.
*   **`Carrinho.jsx`**: Nova página para gerenciar os itens adicionados à loja de suplementos, permitindo ajustar quantidades, remover itens e calcular o total da compra.

### Serviços de API (Frontend)

O arquivo `src/services/api.js` foi atualizado para incluir os métodos de interação com as novas rotas de medidas corporais e registros de humor, além de melhorias nos métodos de upload de foto e manipulação de pedidos.

### Implementação da Nova Identidade Visual

A nova identidade visual "Equil" foi aplicada aos principais componentes do frontend:

*   **Cores**: Utilização de gradientes suaves (verde menta, azul-claro, lilás) para elementos como o logo, botões e cards.
*   **Tipografia**: Fontes arredondadas e modernas para uma sensação de leveza e bem-estar.
*   **Logo e Slogan**: O logo foi atualizado com um gradiente e o slogan "Seu equilíbrio, sua jornada" foi incorporado.
*   **Cards e Layouts**: Redesenho de cards e seções para refletir a nova paleta de cores e estilo, como no Dashboard e Perfil.

### Novas Funcionalidades (Frontend)

*   **Acompanhamento de Medidas Corporais**: Interface completa no `Perfil.jsx` para adicionar, editar, deletar e visualizar a evolução de diversas medidas corporais através de gráficos e tabelas.
*   **Sistema de Acompanhamento de Humor**: Interface completa no `Dashboard.jsx` para registrar o humor diário, energia, estresse, sono, motivação e outros indicadores, com visualização de histórico e estatísticas.
*   **Dashboard Aprimorado**: O `Dashboard.jsx` agora integra os novos componentes `DashboardMetricas` e `AcompanhamentoHumor`, fornecendo uma visão holística do progresso e bem-estar do usuário.
*   **Carrinho de Compras**: Implementação de uma página de carrinho (`Carrinho.jsx`) para a loja de suplementos, permitindo aos usuários gerenciar seus itens antes de finalizar a compra. A funcionalidade de adicionar ao carrinho foi integrada à página de `Suplementos.jsx`.

## 5. Conclusão

O projeto Equil foi significativamente aprimorado com a implementação da nova identidade visual, correção de bugs importantes e a adição de funcionalidades cruciais para o acompanhamento de saúde e bem-estar do usuário. As novas features de medidas corporais, humor e o dashboard unificado oferecem uma experiência mais completa e engajadora. A integração do carrinho de compras para a loja de suplementos conclui a jornada do usuário dentro da plataforma, desde o acompanhamento pessoal até a aquisição de produtos recomendados.

---

