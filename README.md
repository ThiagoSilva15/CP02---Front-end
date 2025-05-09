
**Nome:** Thiago Almança da Silva **RM:** 558108

* **Link do Repositório GitHub do primeiro CP:** https://github.com/criswd/checkpoint-ifood-pycaret
* **📓 Notebook no Colab:** https://colab.research.google.com/drive/1Tl3wDeVi_1gYCofGjFRZi0TzNDA-n8bI?usp=sharing
---

**Instruções de Uso do Aplicativo**

# Simulador de Conversão de Vendas iFood

Este aplicativo Streamlit simula a probabilidade de conversão de vendas de clientes, utilizando um modelo de Machine Learning.

## 1. Visão Geral

O aplicativo permite que você carregue dados de clientes a partir de um arquivo CSV e, em seguida, utiliza um modelo de Machine Learning pré-treinado para prever quais clientes têm maior probabilidade de realizar uma compra. Você pode ajustar um limiar (threshold) para controlar a classificação dos clientes como "Propensos" ou "Não Propensos" à conversão. O aplicativo também fornece visualizações para ajudar a entender os dados e os resultados da previsão.

## 2. Como Usar

### 2.1. Carregar Dados

1.  **Fonte de Dados:**
    * Na barra lateral esquerda, selecione a opção "CSV".
    * Clique em "📂 Carregar CSV" para abrir o seletor de arquivos.
    * Selecione o arquivo CSV que contém os dados dos seus clientes. O arquivo deve incluir as seguintes colunas:
        * `Age`: Idade do cliente.
        * `Income`: Renda do cliente.
        * `Recency`: Número de dias desde a última compra.
        * `Frequency`: Número de compras realizadas pelo cliente.
        * `Spent`: Valor total gasto pelo cliente.
    * O aplicativo irá carregar os dados do CSV. Se o arquivo não contiver as colunas esperadas, uma mensagem de erro será exibida.

### 2.2. Configurar o Threshold

1.  **Threshold:**
    * Na barra lateral esquerda, você encontrará um slider e um campo de texto rotulado como "Threshold".
    * O threshold é um valor que determina a partir de qual probabilidade um cliente é considerado "Propenso" a converter.
    * Você pode ajustar o threshold movendo o slider ou digitando um valor no campo de texto. Os valores devem estar entre 0 e 1.
    * Clique no botão "Aplicar Threshold" para aplicar o valor selecionado. O threshold atual será exibido abaixo do botão.

### 2.3. Visualizar Predições

1.  **Predições:**
    * Após carregar os dados do CSV, a aba "📊 Predições" exibirá os resultados da previsão.
    * **Métricas:** O aplicativo mostrará a quantidade de clientes classificados como "Propensos (1)" e "Não Propensos (0)", com base no threshold atual.
    * **Gráfico de Barras:** Um gráfico de barras exibirá a distribuição dos clientes entre as duas classes (Propensos e Não Propensos).
    * **Tabela de Predições:** Uma tabela mostrará os dados dos clientes do seu CSV, juntamente com a probabilidade de conversão prevista (propensity_score) para cada cliente. A tabela também indicará a classe prevista (0 ou 1) para cada cliente, com base no threshold. As linhas da tabela são coloridas para facilitar a visualização (verde para propensos, vermelho para não propensos).
    * **Baixar Predições:** Você pode baixar a tabela de predições em formato CSV clicando no botão "⬇️ Baixar Predições".

### 2.4. Analisar Dados

1.  **Analytics:**
    * A aba "📈 Analytics" fornece visualizações para ajudar a entender os dados dos clientes e como eles se relacionam com a probabilidade de conversão.
    * Para cada uma das colunas numéricas (`Age`, `Income`, `Recency`, `Frequency`, `Spent`), o aplicativo exibirá:
        * **Boxplot:** Um boxplot que compara a distribuição da coluna para os clientes "Propensos" e "Não Propensos".
        * **Histograma:** Um histograma que mostra a frequência dos valores da coluna para os clientes "Propensos" e "Não Propensos".


### 3.como Rodar 
* ** 📦 Requisitos **
Antes de executar, certifique-se de ter as seguintes bibliotecas instaladas:

pip install streamlit pandas numpy pycaret plotly
💡 Recomendado: criar um ambiente virtual (venv) para isolar as dependências do projeto.

* **🚀 Como Rodar **
Clone o repositório ou baixe os arquivos.

Certifique-se de que o arquivo do modelo PyCaret (pickle_rf_pycaret2) esteja em ./deploy/pickle/.

Coloque a logo em ./images/logo_fiap.png (ou substitua por outra imagem de sua preferência).

* **Execute o Streamlit: **

streamlit run app.py
📂 Modos de Uso
🗂️ Modo CSV
No menu lateral, selecione "CSV" como fonte de dados.

Faça o upload de um arquivo .csv com as seguintes colunas obrigatórias:

Age

Income

Recency

Frequency

Spent

Ajuste o threshold de classificação se desejar.

Visualize:

Métricas gerais de classificação.

Distribuição de predições.

Tabelas estilizadas com scores.

Análises gráficas por feature (boxplots e histogramas).

Baixe as predições em CSV com o botão “⬇️ Baixar Predições”.

* ** 🌐 Modo Online **
Atualmente, este modo está desabilitado. Utilize o modo CSV com os dados de teste gerados previamente.

* ** 📊 Funcionalidades **
Classificação binária utilizando modelo treinado com PyCaret.

Upload de dados customizados via CSV.

Interface responsiva com tema personalizado.

Ajuste de threshold de classificação.

Métricas interativas com Plotly.

Download de resultados.

* ** 🧠 Sobre o Modelo **
O modelo carregado (pickle_rf_pycaret2) é um Random Forest Classifier treinado com dados simulados de comportamento de clientes e preparado via PyCaret.

📎 Estrutura de Pastas

├── app.py                   # Arquivo principal da aplicação
├── deploy/
│   └── pickle/
│       └── pickle_rf_pycaret2
├── images/
│   └── logo_fiap.png
📌 Observações
O código utiliza @st.cache_resource para otimizar o carregamento do modelo.

O threshold padrão de classificação é 0.5, mas pode ser ajustado dinamicamente.

Arquivos CSV com colunas incompletas serão rejeitados automaticamente.

