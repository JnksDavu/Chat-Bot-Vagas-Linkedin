## Chat-Bot-Vagas-Linkedin

# Descrição

Esta aplicação realiza a análise de aderência de perfis do LinkedIn a uma vaga de trabalho.
Ela utiliza a API Gemini (Google AI) para avaliar e pontuar automaticamente os candidatos com base em critérios da vaga, como escolaridade, experiência e habilidades técnicas.

Os dados dos candidatos são coletados automaticamente através do Phantombuster, e depois transformados e analisados localmente.

## Estrutura do Projeto

<img width="680" height="698" alt="image" src="https://github.com/user-attachments/assets/542972bc-ef3a-41d4-88c5-4aeb3b4fb1f1" />


## Requisitos

- Certifique-se de ter o Python 3.10+ instalado.

# Dependências principais

- streamlit – Interface web

- google-genai – SDK oficial da API Gemini

- pandas – Exibição tabular dos resultados

- requests – Consumo da API do Phantombuster

- python-dotenv – Leitura das variáveis de ambiente

## Configurações

- Crie e ative o ambiente virtual: python3 -m venv venv && source venv/bin/activate
- pip install -r requirements.txt
- Crie o arquivo .env na raiz do projeto:
    - GEMINI_API_KEY=suachave_google_ai
    - apiKey=suachave_phantombuster

## Coleta e Processamento dos Dados
1. Obter os perfis do LinkedIn

- Execute o script que acessa o Phantombuster e baixa o resultado mais recente do seu Phantom configurado:
    - python run_phantom.py
    - O arquivo dataset/candidatos_linkedin_raw.json será gerado.

2. Converter para JSON processável
 - Execute o script que baixa e converte o JSON final: python make_profiles_json.py
 - Isso criará dataset/candidatos_linkedin.json, usado pela aplicação principal.

## Execução da Aplicação
 - streamlit run app.py
 - A aplicação abrirá no navegador (por padrão em http://localhost:8501).

## Resultados:

<img width="1503" height="909" alt="Captura de Tela 2025-10-31 às 13 57 26" src="https://github.com/user-attachments/assets/d402d852-eb97-4ed7-b855-176a1c17796b" />

