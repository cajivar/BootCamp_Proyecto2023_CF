# Importacion de librerias

import streamlit as st
import pandas as pd
import plotly.express as px

# Configuracion de la pagina

st.set_page_config(
    page_title="Dashboard",
    page_icon="X",
    layout="wide",
    initial_sidebar_state="expanded"
)

with st.sidebar:
    st.title("Dashboard")
    st.write("DLaboratorio Nutriendo")

# carga de datos

compras_raw = pd.read_csv('compra.csv', index_col=[0])

# quitar valores nulos

compras_raw = compras_raw.drop(compras_raw[compras_raw['Height']>210].index)
compras_raw = compras_raw.drop(compras_raw[compras_raw['Height']<120].index)
compras_raw = compras_raw.drop(compras_raw[compras_raw['Weight']>140].index)
compras_raw = compras_raw.drop(compras_raw[compras_raw['Weight']<30].index)



# mostrar momentaneamente los datos
# st.write(supertienda_raw)
st.write(compras_raw)


# Containner principal


with st.container():
    # Titulo
    st.title('Clientes Potenciales Dashboard')

# Containner para filtros por año, mes y region
with st.container():
    # creacion de columnas para filtros
    filtro_año, filtro_estado, filtro_compra = st.columns(3)
    
    with filtro_año:
        # filtro por año
        list_años = compras_raw['Año'].unique()
        list_años.sort()
        año = st.multiselect('Año', list_años, list_años[0])
    with filtro_estado:
        # filtro por estado
        list_estado = compras_raw['Estado'].unique()
        list_estado.sort()
        estado = st.multiselect('Estado', list_estado, list_estado[0])
    with filtro_compra:
        # filtro por compra
        list_compra = compras_raw['Compra'].unique()
        list_compra.sort()
        compra = st.multiselect('Compra', list_compra, list_compra[0])

# dataframe filtrado
compras_filter = compras_raw[
        (compras_raw['Año'].isin(año)) 
    &   (compras_raw['Estado'].isin(estado)) 
    &   (compras_raw['Compra'].isin(compra))
    ]

# Container para 2 KPI's
with st.container():
    # creacion de 2 columnas
    kpi1, kpi2 = st.columns(2)
    # Creacion de KPI's con st.metric
    with kpi1:
        st.metric(label='Total Compradores', value=f"{compras_filter['Compra'].count():,.0f}")
    # with kpi2:
    #    st.metric(label='Total Estado IMC', value=f"{compras_filter['Año'].count():,.0f}")

# Container para nuestros dos primeros graficos
st.header('Tendencia de Ventas')
with st.container():
    # creacion de 2 columnas para el grafico de lineas y de pie
    line_chart_total, pie_chart_total = st.columns((2,2))
    with line_chart_total:
        # grafico de lineas
        data_line = compras_filter.groupby('Año')['Compra'].count().reset_index()
        line_chart = px.line(data_line, 
                            x='Año', 
                            y='Compra', 
                            title='Tendencia de Ventas')
        line_chart.update_layout(height=600, 
                                width=500)
        st.plotly_chart(line_chart)
    
    with pie_chart_total:
        # grafico de pie para ventas totales por pais
        data_pie = compras_filter.groupby('Año')['Estado'].count().reset_index()
        pie_chart = px.pie(data_pie, 
                            values='Estado', 
                            names='Año', 
                            title='Ventas por Estado IMC')
        # cambiar el tamaño del grafico
        pie_chart.update_traces(textposition='inside', 
                                textinfo='percent+label+value')
        pie_chart.update_layout(uniformtext_minsize=12, 
                                uniformtext_mode='hide',
                                showlegend=False,
                                height=500, 
                                width=500)
        st.plotly_chart(pie_chart)
        
# Container para nuestros dos ultimos graficos
with st.container():
    # creacion de 2 columnas para el grafico de barras horizontales y de barras verticales
    st.markdown('## Ventas por Edad')
    bar_chart_total, bar_chart_total2 = st.columns((2,2))
    
    with bar_chart_total:
        # grafico de barras horizontales
        data_bar = compras_filter.groupby('Edad')['Compra'].count().reset_index()
        bar_chart = px.bar(data_bar, 
                            y='Edad', 
                            x='Compra', 
                            title='Ventas por Edad',
                            color='Edad',
                            orientation='h',
                            text_auto='.2s')
        bar_chart.update_layout(height=600, 
                                width=400)
        st.plotly_chart(bar_chart)
    
    with bar_chart_total2:
        # grafico de barras verticales
        data_bar2 = compras_filter.groupby('Weight')['Compra'].count().reset_index()
        bar_chart2 = px.bar(data_bar2, 
                            x='Weight', 
                            y='Compra', 
                            title='Ventas por Peso',
                            color='Weight',
                            text_auto='.2s')
        bar_chart2.update_layout(height=600, 
                                width=400)
        st.plotly_chart(bar_chart2)        