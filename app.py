import streamlit as st
import pandas as pd
import numpy as np
import pickle
from pycaret.classification import load_model, predict_model, get_config
import plotly.express as px

# ------- Configuração de Página e Tema -------
st.set_page_config(
    page_title='Simulador - Case iFood [v2]',
    page_icon='./images/logo_fiap.png',
    layout='wide',
    initial_sidebar_state='expanded'
)
# CSS Customizado
st.markdown(
    """
    <style>
    .stApp { background-color: #f7f7f7; font-family: 'Helvetica', sans-serif; }
    .css-1d391kg { background-color: #ffffff; padding: 1rem; }
    .card { background-color: #ffffff; border-radius: 10px; padding: 1rem; box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 1rem; }
    h2, h3, h4 { color: #cc1f2f; }
    </style>
    """, unsafe_allow_html=True
)
st.title('🎯 Simulador - Conversão de Vendas')

# ------- Carregamento de Modelo -------
@st.cache_resource
def carregar_modelo():
    return load_model('./deploy/pickle/pickle_rf_pycaret2')
mdl_rf = carregar_modelo()

# get expected feature names from PyCaret pipeline config
try:
    expected_columns = list(get_config('X_columns'))
except Exception:
    # fallback to model attribute, excluding target
    expected_columns = [c for c in getattr(mdl_rf, 'feature_names_in_', []) if c != 'Response']
# always exclude target if present
expected_columns = [c for c in expected_columns if c != 'Response']

FEATURES = ['Age', 'Income', 'Recency', 'Frequency', 'Spent']

# ------- Sidebar -------
if 'thresh' not in st.session_state:
    st.session_state.thresh = 0.5
with st.sidebar:
    st.image('./images/logo_fiap.png', width=150)
    st.subheader('Auto ML - Fiap [v2]')
    st.markdown('---')
    fonte = st.radio('Fonte de dados:', ['CSV', 'Online'], horizontal=True)
    st.markdown('---')
    # Novo threshold temporário
    temp_slider = st.slider('🔧 Threshold', 0.0, 1.0, 0.5, 0.01)
    temp_text = st.text_input('✍️ Threshold (texto)', value=f'{temp_slider}')
    try:
        new_thresh = float(temp_text)
    except:
        new_thresh = temp_slider
    if st.button('Aplicar Threshold'):
        st.session_state.thresh = new_thresh
    st.markdown(f'*Threshold atual:* {st.session_state.thresh:.2f}')

thresh = st.session_state.thresh

# ------- Modo CSV -------
if fonte == 'CSV':
    file = st.file_uploader('📂 Carregar CSV', type='csv')
    if file:
        Xtest = pd.read_csv(file)
        # validate required columns
        missing = list(set(expected_columns) - set(Xtest.columns))
        if missing:
            st.error(f"Arquivo CSV ausente colunas obrigatórias: {missing}")
            st.stop()
        ypred = predict_model(mdl_rf, data=Xtest, raw_score=True)
        # standardize score column name to 'propensity_score'
        score_col = None
        # prefer Score_1
        if 'Score_1' in ypred.columns:
            score_col = 'Score_1'
        # then PyCaret v3's prediction_score
        elif 'prediction_score' in ypred.columns:
            score_col = 'prediction_score'
        else:
            # fallback: any column containing 'score'
            for c in ypred.columns:
                if 'score' in c.lower():
                    score_col = c
                    break
        if score_col:
            ypred.rename(columns={score_col: 'propensity_score'}, inplace=True)

        tab1, tab2 = st.tabs(['📊 Predições', '📈 Analytics'])
        with tab1:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            c1, c2, c3 = st.columns(3)
            qtd_true = (ypred['propensity_score'] > thresh).sum()
            qtd_false = len(ypred) - qtd_true
            c1.metric('✅ Propensos (1)', qtd_true)
            c2.metric('❌ Não Propensos (0)', qtd_false)
            fig_bar = px.bar(x=['Propensos','Não Propensos'], y=[qtd_true, qtd_false],
                             title='Distribuição de Predições', labels={'x':'Classe','y':'Quantidade'})
            st.plotly_chart(fig_bar, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
            def style_score(val):
                return 'background-color: #adebad' if val > thresh else 'background-color: #ff9999'
            st.dataframe(ypred.style.applymap(style_score, subset=['propensity_score']), use_container_width=True)
            csv = ypred.to_csv(index=False).encode('utf-8')
            st.download_button('⬇️ Baixar Predições', csv, 'predicoes.csv', 'text/csv')
        with tab2:
            st.markdown('<div class="card">', unsafe_allow_html=True)
            st.write('### Análise de Features por Grupo')
            ypred['label'] = np.where(ypred['propensity_score'] > thresh, 1, 0)
            # dynamic numeric features for analysis
            numeric_feats = [col for col in ypred.select_dtypes(include=[int, float])
                             if col not in ['Score_1','Score_0','propensity_score']]
            for feat in numeric_feats:
                st.write(f'#### 🔍 {feat}')
                fig_box = px.box(ypred, x='label', y=feat,
                                 title=f'Boxplot de {feat}', labels={'label':'Classe','value':feat})
                st.plotly_chart(fig_box, use_container_width=True)
                fig_hist = px.histogram(ypred, x=feat, color='label', barmode='overlay',
                                        nbins=20, title=f'Histograma de {feat} por Classe')
                st.plotly_chart(fig_hist, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
    else:
        st.warning('📌 Por favor, carregue um arquivo CSV.')

# ------- Modo Online -------
else:
    st.warning('🔧 Modo Online indisponível. Por favor, use o modo CSV com Xtest.csv gerado pelo notebook.')