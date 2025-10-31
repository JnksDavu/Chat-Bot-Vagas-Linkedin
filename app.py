import os
import json
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from google import genai

# ---------------- CONFIGURAÇÕES ---------------- #
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Chave da API Gemini não encontrada. Defina GEMINI_API_KEY no .env")
    st.stop()

client = genai.Client(api_key=api_key)

# ---------------- FUNÇÃO GEMINI ---------------- #
def analisar_aderencia(vaga, candidatos):
    prompt = f"""
    Você é um recrutador especialista em tecnologia e deve avaliar a aderência de perfis do LinkedIn a uma vaga descrita.

    **Descrição da vaga:**
    {vaga}

    **Tarefas:**
    - Leia os dados dos candidatos (em JSON).
    - Avalie compatibilidade considerando escolaridade, experiências, habilidades e contexto da vaga.
    - Calcule um percentual de aderência (0 a 100%).
    - Retorne os 5 candidatos mais aderentes, em formato JSON com os campos:
      nome, linkedin, empresa_atual, aderencia (%), justificativa curta.

    **Candidatos:**
    {json.dumps(candidatos, ensure_ascii=False, indent=2)}
    """

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=prompt
    )
    return response.text


# ---------------- FRONTEND ---------------- #
st.set_page_config(page_title="Analisador de Aderência de Vagas - LinkedIn", layout="wide")
st.title("Analisador de Aderência de Vagas - LinkedIn")

col1, col2 = st.columns(2)
with col1:
    escolaridade = st.text_input("Grau de escolaridade", "Ensino Superior Completo")
    experiencia = st.text_input("Tempo mínimo de experiência", "2 anos")
with col2:
    obrigatorios = st.text_area("Conhecimentos obrigatórios", "Python, SQL, Power BI")
    desejaveis = st.text_area("Conhecimentos desejáveis", "ETL, GCP, Docker")

observacoes = st.text_area("Outras observações", "Perfil analítico e boa comunicação")

vaga_descricao = f"""
Grau de escolaridade: {escolaridade}
Tempo de experiência: {experiencia}
Conhecimentos obrigatórios: {obrigatorios}
Conhecimentos desejáveis: {desejaveis}
Outras observações: {observacoes}
"""

# ---------------- AÇÃO ---------------- #
if st.button("Analisar Candidatos"):
    with st.spinner("Analisando perfis... isso pode levar alguns segundos..."):
        with open("dataset/candidatos_linkedin.json", "r", encoding="utf-8") as f:
            candidatos = json.load(f)

        try:
            resultado = analisar_aderencia(vaga_descricao, candidatos)

            # 🔍 Tenta extrair JSON do retorno do Gemini
            try:
                inicio = resultado.find('[')
                fim = resultado.rfind(']') + 1
                resultado_json = resultado[inicio:fim]
                candidatos_top5 = json.loads(resultado_json)
            except Exception:
                st.error("Erro ao interpretar o JSON retornado pelo Gemini.")
                st.text(resultado)
                st.stop()

            # ✅ Exibe o resultado em tabela bonita
            df = pd.DataFrame(candidatos_top5)
            df = df.rename(columns={
                "nome": "Nome",
                "linkedin": "LinkedIn",
                "empresa_atual": "Empresa Atual",
                "aderencia (%)": "Aderência (%)",
                "justificativa curta": "Justificativa"
            })

            st.success("Análise concluída!")
            st.subheader("Top 5 Candidatos Mais Aderentes")
            st.dataframe(df, use_container_width=True)

        except Exception as e:
            st.error(f"Erro ao chamar Gemini: {e}")
