import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io
from io import BytesIO

# Configuração da página PROFISSIONAL
st.set_page_config(
    page_title="Dashboard Profissional - Analytics Pro",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS PROFISSIONAL QUE FUNCIONA
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
        font-weight: bold;
        padding: 1rem;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
    }
    .metric-card {
        background: linear-gradient(135deg, #1f77b4 0%, #29487d 100%);
        padding: 1.5rem;
        border-radius: 15px;
        color: white;
        text-align: center;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
        margin: 5px;
    }
    .section-header {
        font-size: 1.5rem;
        color: #2c3e50;
        margin: 2rem 0 1rem 0;
        border-left: 5px solid #FF4B4B;
        padding-left: 1rem;
        background-color: #f8f9fa;
        padding: 1rem;
        border-radius: 5px;
    }
    .stButton>button {
        background: linear-gradient(135deg, #FF4B4B 0%, #FF6B6B 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.5rem 1rem;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Cache para performance
@st.cache_data
def carregar_dados(uploaded_file):
    try:
        if uploaded_file.name.endswith('.csv'):
            return pd.read_csv(uploaded_file)
        else:
            return pd.read_excel(uploaded_file)
    except Exception as e:
        st.error(f"Erro ao carregar arquivo: {e}")
        return None

@st.cache_data
def gerar_dados_exemplo():
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=100, freq='D')
    return pd.DataFrame({
        'Data': dates,
        'Vendas': np.random.normal(1000, 200, 100).cumsum(),
        'Usuários': np.random.normal(500, 100, 100).cumsum(),
        'Receita': np.random.normal(2000, 500, 100).cumsum(),
        'Região': np.random.choice(['Norte', 'Sul', 'Leste', 'Oeste'], 100),
        'Custo': np.random.uniform(50, 500, 100)
    })

# Função para exportar Excel
def to_excel(df):
    output = BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df.to_excel(writer, index=False, sheet_name='Relatório')
    return output.getvalue()

# Header profissional
st.markdown('<h1 class="main-header">🚀 DASHBOARD PROFISSIONAL</h1>', unsafe_allow_html=True)
st.markdown("**Sistema de Análise de Dados em Tempo Real**")

# Sidebar profissional
with st.sidebar:
    st.markdown("### ⚙️ Controles")
    
    st.markdown("---")
    st.subheader("📈 Configurações")
    tema = st.selectbox("Tema dos Gráficos:", ["plotly_white", "plotly", "plotly_dark"])
    
    st.subheader("🎛️ Parâmetros")
    n_points = st.slider("Período de Análise:", 30, 365, 100)
    
    st.markdown("---")
    st.success("💡 **Dica:** Faça upload de seus dados ou use os exemplos.")

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["📈 Dashboard", "📊 Análise", "📁 Dados", "⚙️ Configurações"])

with tab1:
    st.markdown('<div class="section-header">📈 Métricas de Performance</div>', unsafe_allow_html=True)
    
    # Métricas profissionais em cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("""
        <div class="metric-card">
            <div style='font-size: 1.2rem;'>🎯 Vendas</div>
            <div style='font-size: 2rem; font-weight: bold;'>R$ 154K</div>
            <div style='font-size: 0.9rem;'>+12% vs anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="metric-card">
            <div style='font-size: 1.2rem;'>👥 Usuários</div>
            <div style='font-size: 2rem; font-weight: bold;'>2.4K</div>
            <div style='font-size: 0.9rem;'>+8% vs anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("""
        <div class="metric-card">
            <div style='font-size: 1.2rem;'>💰 Receita</div>
            <div style='font-size: 2rem; font-weight: bold;'>R$ 298K</div>
            <div style='font-size: 0.9rem;'>+15% vs anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    with col4:
        st.markdown("""
        <div class="metric-card">
            <div style='font-size: 1.2rem;'>📊 ROI</div>
            <div style='font-size: 2rem; font-weight: bold;'>127%</div>
            <div style='font-size: 0.9rem;'>+5% vs anterior</div>
        </div>
        """, unsafe_allow_html=True)
    
    # Gráficos profissionais
    st.markdown('<div class="section-header">📊 Visualizações Interativas</div>', unsafe_allow_html=True)
    
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        dados = gerar_dados_exemplo()
        fig = px.line(dados, x='Data', y=['Vendas', 'Receita'], 
                     title="📈 Evolução de Vendas e Receita",
                     template=tema)
        st.plotly_chart(fig, use_container_width=True)
    
    with col_graf2:
        fig2 = px.pie(dados, names='Região', values='Vendas',
                     title="🗺️ Distribuição por Região",
                     template=tema)
        st.plotly_chart(fig2, use_container_width=True)

with tab2:
    st.markdown('<div class="section-header">🔍 Análise Detalhada</div>', unsafe_allow_html=True)
    
    # Análise estatística
    col_anal1, col_anal2 = st.columns(2)
    
    with col_anal1:
        st.subheader("📋 Estatísticas Descritivas")
        st.dataframe(dados[['Vendas', 'Usuários', 'Receita', 'Custo']].describe(), use_container_width=True)
    
    with col_anal2:
        st.subheader("🔗 Matriz de Correlação")
        correlacao = dados[['Vendas', 'Usuários', 'Receita', 'Custo']].corr()
        fig_corr = px.imshow(correlacao, text_auto=True, aspect="auto",
                           color_continuous_scale='RdBu_r',
                           title="Correlação entre Variáveis")
        st.plotly_chart(fig_corr, use_container_width=True)

with tab3:
    st.markdown('<div class="section-header">📁 Gerenciamento de Dados</div>', unsafe_allow_html=True)
    
    col_up1, col_up2 = st.columns(2)
    
    with col_up1:
        st.subheader("📤 Upload de Dados")
        uploaded_file = st.file_uploader("Carregue seus dados:", type=['csv', 'xlsx'])
        
        if uploaded_file is not None:
            if uploaded_file.size > 10_000_000:  # 10MB limite
                st.error("❌ Arquivo muito grande! Máximo 10MB.")
            else:
                dados_usuario = carregar_dados(uploaded_file)
                if dados_usuario is not None:
                    st.success(f"✅ Dados carregados! {dados_usuario.shape[0]} linhas, {dados_usuario.shape[1]} colunas")
                    st.dataframe(dados_usuario.head(), use_container_width=True)
    
    with col_up2:
        st.subheader("📥 Exportação")
        st.info("Exporte relatórios e análises")
        
        # Botão de exportação
        excel_data = to_excel(dados)
        st.download_button(
            label="📊 Exportar para Excel",
            data=excel_data,
            file_name=f"relatorio_{datetime.now().strftime('%Y%m%d')}.xlsx",
            mime="application/vnd.ms-excel"
        )

with tab4:
    st.markdown('<div class="section-header">⚙️ Configurações do Sistema</div>', unsafe_allow_html=True)
    
    col_conf1, col_conf2 = st.columns(2)
    
    with col_conf1:
        st.subheader("🛠️ Preferências")
        auto_update = st.checkbox("Atualização automática", value=True)
        notificacoes = st.checkbox("Receber notificações", value=True)
        tema_escuro = st.checkbox("Modo escuro")
        
        if st.button("💾 Salvar Configurações"):
            st.success("Configurações salvas com sucesso!")
    
    with col_conf2:
        st.subheader("ℹ️ Sobre")
        st.markdown("""
        **Dashboard Profissional v2.0**
        
        🚀 **Desenvolvido com:**
        - Streamlit
        - Pandas
        - Plotly
        - Python
        
        📧 **Suporte:** seu-email@empresa.com
        """)

# Rodapé profissional
st.markdown("---")
col_foot1, col_foot2, col_foot3 = st.columns(3)
with col_foot2:
    st.markdown(f"""
    <div style='text-align: center; color: #666;'>
        <strong>Dashboard Profissional v2.0</strong><br>
        Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}<br>
        © 2024 - Todos os direitos reservados
    </div>
    """, unsafe_allow_html=True)
