import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import io

# Configuração da página
st.set_page_config(
    page_title="Dashboard Incrível",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personalizado
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
</style>
""", unsafe_allow_html=True)

# Título principal
st.markdown('<h1 class="main-header">📊 Dashboard Interativo Completo</h1>', unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.header("⚙️ Configurações")
    
    st.subheader("🎨 Personalização")
    tema = st.selectbox("Escolha o tema dos gráficos:", ["plotly", "plotly_white", "plotly_dark"])
    
    st.subheader("📈 Tipo de Gráfico")
    tipo_grafico = st.radio("Selecione:", ["Linha", "Barras", "Área", "Pizza"])
    
    st.subheader("🔢 Parâmetros")
    n_points = st.slider("Número de pontos:", 10, 1000, 100)
    faixa_valores = st.slider("Faixa de valores:", -100.0, 100.0, (-50.0, 50.0))
    
    st.markdown("---")
    st.info("Feito com ❤️ usando Streamlit")

# Abas principais
tab1, tab2, tab3, tab4 = st.tabs(["📈 Dashboard", "📊 Análise", "📁 Upload", "ℹ️ Sobre"])

with tab1:
    st.header("📈 Visualização de Dados em Tempo Real")
    
    # Gerar dados aleatórios
    np.random.seed(42)
    dates = pd.date_range(start='2024-01-01', periods=n_points, freq='D')
    
    data = pd.DataFrame({
        'Data': dates,
        'Vendas': np.random.normal(1000, 200, n_points).cumsum(),
        'Usuários': np.random.normal(500, 100, n_points).cumsum(),
        'Receita': np.random.normal(2000, 500, n_points).cumsum(),
        'Custo': np.random.uniform(faixa_valores[0], faixa_valores[1], n_points)
    })
    
    # Métricas em colunas
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="📊 Total de Vendas",
            value=f"R$ {data['Vendas'].iloc[-1]:,.0f}",
            delta=f"{data['Vendas'].iloc[-1] - data['Vendas'].iloc[-2]:.0f}"
        )
    
    with col2:
        st.metric(
            label="👥 Total de Usuários",
            value=f"{data['Usuários'].iloc[-1]:,.0f}",
            delta=f"{data['Usuários'].iloc[-1] - data['Usuários'].iloc[-2]:.0f}"
        )
    
    with col3:
        st.metric(
            label="💰 Receita Total",
            value=f"R$ {data['Receita'].iloc[-1]:,.0f}",
            delta=f"{data['Receita'].iloc[-1] - data['Receita'].iloc[-2]:.0f}"
        )
    
    with col4:
        custo_atual = data['Custo'].iloc[-1]
        st.metric(
            label="⚡ Custo Atual",
            value=f"R$ {custo_atual:.2f}",
            delta=f"{custo_atual - data['Custo'].iloc[-2]:.2f}",
            delta_color="inverse" if custo_atual > 0 else "normal"
        )
    
    # Gráficos
    col_graf1, col_graf2 = st.columns(2)
    
    with col_graf1:
        st.subheader("📊 Evolução ao Longo do Tempo")
        
        if tipo_grafico == "Linha":
            fig = px.line(data, x='Data', y=['Vendas', 'Usuários', 'Receita'], 
                         template=tema, title="Evolução Temporal")
        elif tipo_grafico == "Barras":
            fig = px.bar(data.tail(30), x='Data', y=['Vendas', 'Usuários'], 
                        template=tema, title="Últimos 30 Dias (Barras)")
        elif tipo_grafico == "Área":
            fig = px.area(data, x='Data', y=['Vendas', 'Receita'], 
                         template=tema, title="Evolução (Área)")
        else:
            # Gráfico de pizza para distribuição
            ultimos_dados = data[['Vendas', 'Usuários']].iloc[-1]
            fig = px.pie(values=ultimos_dados.values, names=ultimos_dados.index, 
                        title="Distribuição Atual")
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col_graf2:
        st.subheader("🎯 Análise de Dispersão")
        
        fig2 = px.scatter(data, x='Vendas', y='Receita', 
                         color='Custo', size='Usuários',
                         hover_data=['Data'],
                         template=tema,
                         title="Relação Vendas vs Receita")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Tabela interativa
    st.subheader("📋 Dados Brutos")
    st.dataframe(data.tail(10), use_container_width=True)

with tab2:
    st.header("📊 Análise Estatística")
    
    col_analise1, col_analise2 = st.columns(2)
    
    with col_analise1:
        st.subheader("Estatísticas Descritivas")
        st.dataframe(data[['Vendas', 'Usuários', 'Receita', 'Custo']].describe())
    
    with col_analise2:
        st.subheader("Correlações")
        correlacoes = data[['Vendas', 'Usuários', 'Receita', 'Custo']].corr()
        fig_corr = px.imshow(correlacoes, text_auto=True, aspect="auto", 
                           color_continuous_scale='RdBu_r',
                           title="Matriz de Correlação")
        st.plotly_chart(fig_corr, use_container_width=True)
    
    # Histograma
    st.subheader("Distribuição dos Dados")
    coluna_selecionada = st.selectbox("Selecione a coluna:", ['Vendas', 'Usuários', 'Receita', 'Custo'])
    
    fig_hist = px.histogram(data, x=coluna_selecionada, 
                           nbins=50, 
                           title=f"Distribuição de {coluna_selecionada}",
                           template=tema)
    st.plotly_chart(fig_hist, use_container_width=True)

with tab3:
    st.header("📁 Upload e Análise de Arquivos")
    
    uploaded_file = st.file_uploader("Escolha um arquivo CSV ou Excel", 
                                   type=['csv', 'xlsx'])
    
    if uploaded_file is not None:
        try:
            if uploaded_file.name.endswith('.csv'):
                df_upload = pd.read_csv(uploaded_file)
            else:
                df_upload = pd.read_excel(uploaded_file)
            
            st.success(f"✅ Arquivo carregado com sucesso! Shape: {df_upload.shape}")
            
            col_upload1, col_upload2 = st.columns(2)
            
            with col_upload1:
                st.subheader("Pré-visualização")
                st.dataframe(df_upload.head(), use_container_width=True)
            
            with col_upload2:
                st.subheader("Informações do Dataset")
                st.write(f"**Linhas:** {df_upload.shape[0]}")
                st.write(f"**Colunas:** {df_upload.shape[1]}")
                st.write(f"**Valores nulos:** {df_upload.isnull().sum().sum()}")
                
                # Selecionar colunas para gráfico
                if len(df_upload.columns) >= 2:
                    col_x = st.selectbox("Eixo X:", df_upload.columns)
                    col_y = st.selectbox("Eixo Y:", df_upload.columns)
                    
                    if st.button("Gerar Gráfico"):
                        fig_upload = px.scatter(df_upload, x=col_x, y=col_y, 
                                              title=f"{col_y} vs {col_x}")
                        st.plotly_chart(fig_upload, use_container_width=True)
        
        except Exception as e:
            st.error(f"❌ Erro ao carregar arquivo: {e}")

with tab4:
    st.header("ℹ️ Sobre Este Dashboard")
    
    st.markdown("""
    ### 🚀 Recursos Incríveis Incluídos:
    
    - **📊 Múltiplos Gráficos Interativos** com Plotly
    - **📈 Métricas em Tempo Real** com indicadores de performance
    - **🎨 Personalização** de temas e tipos de gráficos
    - **📁 Upload de Arquivos** para análise personalizada
    - **📊 Análise Estatística** completa
    - **💫 Design Responsivo** que se adapta a qualquer tela
    
    ### 🛠 Tecnologias Utilizadas:
    - **Streamlit** - Framework web
    - **Plotly** - Gráficos interativos
    - **Pandas** - Manipulação de dados
    - **NumPy** - Cálculos numéricos
    
    ### 👨‍💻 Como Usar:
    1. Explore as diferentes abas
    2. Ajuste os parâmetros na sidebar
    3. Faça upload de seus próprios dados
    4. Analise as métricas em tempo real
    """)
    
    st.success("🎉 Parabéns! Seu dashboard está incrível e PROFISSIONAL!")

# Rodapé
st.markdown("---")
st.markdown("*Dashboard criado com ❤️ usando Streamlit | Atualizado em: {}*".format(
    datetime.now().strftime("%d/%m/%Y %H:%M:%S")
))
