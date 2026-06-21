# Documentação de Análise e Projeto (APS)

## 1. Descrição e Delimitação do Escopo
- **Propósito:** Automatizar e gerenciar o processo de venda de ingressos de um cinema e seu catálogo de exibição.
- **Contexto de Uso:** O sistema operará em totens de autoatendimento ou guichês do cinema. O ambiente é dividido entre a área do usuário final (cliente comprando o ingresso) e a área restrita para os administradores.
- **Público-Alvo:** Clientes do cinema e Gerentes/Atendentes do estabelecimento.
- **Problema Resolvido:** Elimina o controle manual de lotação de salas, previne a venda duplicada de um mesmo assento e padroniza a persistência financeira e gerencial das vendas diárias.

---

## 2. Fase de Análise

### a) Requisitos Funcionais (RF)
| ID | Descrição |
|---|---|
| **RF01** | O sistema deve permitir ao administrador cadastrar, listar, atualizar e excluir **Filmes**. |
| **RF02** | O sistema deve permitir ao administrador cadastrar, listar, atualizar e excluir **Salas**, com suas capacidades limite. |
| **RF03** | O sistema deve permitir ao administrador gerenciar **Sessões** (vincular Filme, Sala, Data/Hora e Preço Base). |
| **RF04** | O sistema deve exibir para o cliente apenas Sessões com status ativo/disponível. |
| **RF05** | O sistema deve permitir ao cliente digitar o número do assento desejado para a sessão. |
| **RF06** | O sistema deve verificar a disponibilidade do assento e bloquear vendas duplicadas na mesma sessão. |
| **RF07** | O sistema deve permitir a escolha do tipo de ingresso (Comum, Meia-Entrada, VIP). |
| **RF08** | O sistema deve calcular o preço final do ingresso com base no tipo escolhido e no preço base da sessão. |
| **RF09** | O sistema deve permitir ao cliente escolher a forma de pagamento (PIX, Cartão, Dinheiro). |
| **RF10** | O sistema deve permitir ao administrador consultar o relatório/histórico completo de Vendas realizadas. |

### b) Requisitos Não Funcionais (RNF)
| ID | Descrição | Categoria |
|---|---|---|
| **RNF01** | O sistema deve ser desenvolvido em Python 3.10+ com interface gráfica desktop via `Tkinter`. | Usabilidade / Tecnológico |
| **RNF02** | Os dados devem ser persistidos em um banco de dados relacional `PostgreSQL`. | Armazenamento |
| **RNF03** | O sistema deve adotar a arquitetura MVC (Model-View-Controller) e o padrão DAO. | Arquitetura |
| **RNF04** | O sistema deve utilizar `PlantUML` ou equivalente para a geração dos artefatos de documentação. | Documentação |
| **RNF05** | A integridade referencial do banco de dados deve ser garantida via `Foreign Keys` e `Constraints`. | Segurança |

### c) Regras de Negócio (RN)
| ID | Descrição |
|---|---|
| **RN01** | **Limite de Capacidade:** Não é permitido vender um assento cujo número seja maior que a capacidade máxima da sala vinculada à sessão. |
| **RN02** | **Precificação (Factory):** O ingresso tipo "Meia" custa 50% do valor base; o tipo "VIP" custa 150% do valor base; o "Comum" custa 100%. |
| **RN03** | **Imutabilidade de Vendas:** Uma venda consolidada não pode ser excluída no CRUD tradicional por motivos de auditoria financeira. |

---

## 3. Diagramas de Casos de Uso e Documentação

### Diagrama de Casos de Uso (PlantUML)

![Casos de Uso](./uml/casos_de_uso.png)

### Documentação dos Casos de Uso

**UC01 - Gerenciar Catálogo**
- **Atores:** Administrador
- **Pré-condições:** O sistema e o banco de dados devem estar conectados.
- **Fluxo Principal:** 1. O Admin seleciona a aba de Filmes, Salas ou Sessões.
  2. Preenche os dados solicitados no formulário.
  3. Clica no botão de ação (Salvar/Atualizar/Excluir).
  4. O sistema valida as entradas (Controllers) e atualiza o banco de dados (DAO).
- **Fluxo Alternativo:** Se um dado for inválido (ex: duração negativa), o sistema exibe um Pop-up de erro e aborta.

**UC02 - Comprar Ingresso**
- **Atores:** Cliente
- **Pré-condições:** Devem existir sessões cadastradas como "Disponíveis".
- **Fluxo Principal:** 1. O Cliente seleciona uma sessão na listagem (Treeview).
  2. Insere o número do assento e seleciona o Tipo de Ingresso.
  3. Seleciona a Forma de Pagamento e clica em Confirmar.
  4. O sistema gera a instância de Ingresso.
  5. O sistema chama o UC03 (Processar Pagamento).
  6. A Venda é salva e o assento torna-se indisponível.

**UC03 - Processar Pagamento**
- **Atores:** Cliente (Sistema)
- **Pré-condições:** O Ingresso deve ter sido instanciado e seu valor calculado.
- **Fluxo Principal:** O sistema repassa o valor à classe `Strategy` selecionada (PIX, Cartão, Dinheiro), valida a aprovação e consolida o recibo.

---

## 4. Fase de Projeto: Diagramas UML

### a) Diagrama de Classes - Modelo Conceitual
*(Representa as entidades do domínio e seus relacionamentos sem detalhes de implementação)*

![Diagrama de Classes](./uml/diagrama_de_classes.png)

### b) Diagrama de Classes de Projeto (UML Detalhado)
*(Este diagrama reflete a arquitetura física implementada: Models, MVC, DAO, Factory e Strategy)*

![Classes de Projeto](./uml/classes_de_projeto.png)

### c) Diagrama de Sequência (Fluxo de Venda)
*(Ilustra o fluxo comportamental entre os objetos MVC durante a compra)*

![Diagrama de Sequência](./uml/diagrama_de_sequencia.png)

---

## 5. Considerações Finais
O desenvolvimento deste sistema demonstrou a modelagem UML aliada à programação orientada a objetos. Os principais desafios envolveram mapear corretamente os relacionamentos no SGBD PostgreSQL e garantir que a Interface de Usuário (View/Tkinter) ficasse "cega" em relação ao banco de dados, comunicando-se exclusivamente por meio dos `Controllers`. 

**Melhorias Futuras:** Implementar um módulo de autenticação (Login) para separar fisicamente e proteger a interface do Administrador, e adicionar um mapa visual (Grid) onde o cliente possa clicar diretamente no assento desejado, substituindo o campo de digitação textual, mostrando a disponibilidade de cada assento.

## 6. Referências
- GUEDES, Gilleanes T. A. *UML 2: uma abordagem prática*. 2. ed. São Paulo: Novatec, 2011.
- Documentação Oficial do Python (Tkinter e ABC). Disponível em: https://docs.python.org/3/
- PlantUML (Geração de Diagramas como Código). Disponível em: https://plantuml.com/
- Inteligência Artificial Gemini (Google) para revisão de código e auxílio na notação UML.