<<<<<<< HEAD
# Pipeline-de-Dados-IoT
=======
# Pipeline de Dados com IoT e Docker

## 📌 Sobre o projeto

Nesse projeto eu desenvolvi um pipeline de dados simples para trabalhar com leituras de temperatura de dispositivos IoT.

A ideia foi simular um cenário real, onde sensores coletam dados e essas informações precisam ser organizadas, armazenadas e depois analisadas.

O sistema basicamente lê um arquivo CSV, trata os dados com Python, salva tudo em um banco PostgreSQL usando Docker e depois mostra os resultados em gráficos usando Streamlit.

## 🛠 Tecnologias usadas

- Python  
- Pandas  
- PostgreSQL  
- Docker  
- SQLAlchemy  
- Streamlit  
- Plotly  

## 📁 Organização do projeto

iot-pipeline-docker/
├── data/
├── sql/
├── src/
├── dashboard.py
├── requirements.txt
├── docker-compose.yml
├── README.md


## 📊 Dataset

Os dados usados no projeto são de temperatura de dispositivos IoT.

O arquivo CSV foi baixado do Kaggle e colocado dentro da pasta:

data/temperature_readings.csv


## ⚙️ Como rodar o projeto

### 1. Criar o ambiente virtual


python -m venv venv
venv\Scripts\activate


### 2. Instalar as dependências


pip install -r requirements.txt


### 3. Subir o banco com Docker


docker compose up -d


### 4. Colocar o CSV na pasta data/

### 5. Rodar o pipeline


python src/pipeline.py

### 6. Abrir o dashboard

streamlit run dashboard.py

## 🔄 O que o pipeline faz

- identifica as colunas do arquivo  
- organiza os nomes das colunas  
- converte os dados  
- remove valores inválidos  
- cria a tabela no banco  
- insere os dados no PostgreSQL  
- cria views para análise  

## 📈 Views criadas

- média de temperatura por dispositivo  
- quantidade de leituras por hora  
- temperatura máxima e mínima por dia  


## 📊 Dashboard

Mostra:

- total de leituras  
- média geral de temperatura  
- maior e menor temperatura  
- gráficos e tabela de dados  

## 💡 O que dá pra analisar

- dispositivos com maior temperatura  
- horários com mais leituras  
- variação ao longo do tempo  
- possíveis picos  

>>>>>>> 3042d0d (Pipeline de Dados IoT)
