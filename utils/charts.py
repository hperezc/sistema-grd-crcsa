import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from weights import COMPONENT_WEIGHTS, DIMENSION_WEIGHTS

def create_radar_chart(evaluacion):
    """
    Crea el gráfico de radar que muestra el nivel de madurez por dimensión
    """
    dimensiones = list(DIMENSION_WEIGHTS.keys())
    valores = [evaluacion.calcular_puntaje_dimension(dim) for dim in dimensiones]
    
    fig = go.Figure(data=go.Scatterpolar(
        r=valores,
        theta=[dim.upper() for dim in dimensiones],
        fill='toself',
        name='Nivel de Madurez',
        line=dict(color='#dc3545')
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        showlegend=False,
        paper_bgcolor='white',
        plot_bgcolor='white',
        height=350,
        margin=dict(t=20, b=20, l=30, r=30)
    )
    
    return fig

def create_gauge_chart(evaluacion):
    """
    Crea el gráfico de medidor que muestra el puntaje total
    """
    puntaje_total = evaluacion.calcular_puntaje_total()
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=puntaje_total,
        domain={'x': [0, 1], 'y': [0, 1]},
        number={'suffix': "%"},
        gauge={
            'axis': {'range': [0, 100]},
            'bar': {'color': "#e0e0e0"},
            'steps': [
                {'range': [0, 40], 'color': "#dc3545"},
                {'range': [40, 80], 'color': "#ffc107"},
                {'range': [80, 100], 'color': "#4caf50"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': puntaje_total
            }
        }
    ))
    
    fig.update_layout(
        paper_bgcolor='white',
        font={'color': "black", 'family': "Arial"},
        height=350,
        margin=dict(t=20, b=20, l=30, r=30)
    )
    
    return fig

def create_stacked_chart(evaluacion):
    """
    Crea el gráfico de barras apiladas que muestra los componentes por dimensión
    """
    data_bars = []
    for dimension in DIMENSION_WEIGHTS.keys():
        componentes = COMPONENT_WEIGHTS[dimension].keys()
        for comp in componentes:
            valor = getattr(evaluacion, comp)
            if valor is not None:
                data_bars.append({
                    'Dimensión': dimension.upper(),
                    'Componente': comp.split('_')[0].upper(),
                    'Valor': valor,
                    'Porcentaje': evaluacion.valor_a_porcentaje(valor)
                })

    df_bars = pd.DataFrame(data_bars)
    fig = px.bar(
        df_bars,
        x='Dimensión',
        y='Porcentaje',
        color='Componente',
        title=''
    )
    
    fig.update_layout(
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True,
        legend_title_text='',
        xaxis_title="",
        yaxis_title="Porcentaje (%)",
        height=400
    )
    
    return fig

def create_heatmap_chart(evaluacion):
    """
    Crea el mapa de calor que muestra la intensidad de los valores por componente
    """
    # Diccionario de abreviaciones para dimensiones
    dimension_abrev = {
        'EQUIPAMIENTO': 'EQUIP',
        'INTEGRACION': 'INTEG',
        'ORGANIZACION': 'ORG',
        'PROCESOS': 'PROC',
        'REGULACIONES': 'REG'
    }
    
    heatmap_data = []
    for dimension in DIMENSION_WEIGHTS.keys():
        componentes = COMPONENT_WEIGHTS[dimension].keys()
        for comp in componentes:
            valor = getattr(evaluacion, comp)
            if valor is not None:
                heatmap_data.append({
                    'Dimensión': dimension_abrev[dimension.upper()],  # Usar abreviación
                    'Componente': comp.split('_')[0].upper(),
                    'Valor': evaluacion.valor_a_porcentaje(valor)
                })

    df_heatmap = pd.DataFrame(heatmap_data)
    df_pivot = df_heatmap.pivot(
        index='Dimensión', 
        columns='Componente', 
        values='Valor'
    )
    
    fig = go.Figure(data=go.Heatmap(
        z=df_pivot,
        x=df_pivot.columns,
        y=df_pivot.index,
        colorscale='RdYlGn',  # Rojo-Amarillo-Verde
        zmin=0,
        zmax=100,
        colorbar=dict(
            title=dict(
                text="Porcentaje (%)",
                side="right"
            ),
            ticktext=['0%', '20%', '40%', '60%', '80%', '100%'],
            tickvals=[0, 20, 40, 60, 80, 100],
            len=0.9,  # Longitud de la barra de color
            thickness=15,  # Grosor de la barra de color
            tickmode='array',
            ticks='outside'
        )
    ))

    fig.update_layout(
        margin=dict(l=50, r=50, t=30, b=50),  # Reducir márgenes
        plot_bgcolor='white',
        paper_bgcolor='white',
        xaxis=dict(
            side='bottom',
            tickangle=45,  # Rotar las etiquetas para mejor lectura
        ),
        yaxis=dict(
            side='left',
            autorange='reversed'  # Mantener el orden de las dimensiones
        ),
        width=None,  # Permitir que el ancho sea responsivo
        height=400,  # Aumentar altura para igualar con el gráfico de Pareto
        autosize=True  # Permitir que el gráfico sea responsivo
    )

    return fig

def create_pareto_chart(evaluacion):
    """
    Crea el gráfico de Pareto que muestra la distribución acumulada de los componentes
    """
    pareto_data = []
    for dimension in DIMENSION_WEIGHTS.keys():
        componentes = COMPONENT_WEIGHTS[dimension].keys()
        for comp in componentes:
            valor = getattr(evaluacion, comp)
            if valor is not None:
                valor_porcentaje = evaluacion.valor_a_porcentaje(valor)
                pareto_data.append({
                    'Componente': comp.split('_')[0].upper(),
                    'Valor': valor_porcentaje
                })

    df_pareto = pd.DataFrame(pareto_data)
    df_pareto = df_pareto.sort_values('Valor', ascending=False)
    df_pareto['Acumulado'] = df_pareto['Valor'].cumsum() / df_pareto['Valor'].sum() * 100

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_pareto['Componente'],
        y=df_pareto['Valor'],
        name='Valor',
        marker_color='#dc3545'
    ))
    fig.add_trace(go.Scatter(
        x=df_pareto['Componente'],
        y=df_pareto['Acumulado'],
        name='% Acumulado',
        line=dict(color='#000000', width=2),
        yaxis='y2'
    ))
    
    fig.update_layout(
        yaxis=dict(
            title='Valor (%)',
            range=[0, 100]
        ),
        yaxis2=dict(
            title='Acumulado (%)',
            overlaying='y',
            side='right',
            range=[0, 100],
            showgrid=False
        ),
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        height=400,
        margin=dict(t=30, b=30, l=30, r=30)
    )
    
    return fig

def create_gap_chart(evaluacion):
    """
    Crea el gráfico de brechas que muestra la diferencia hasta el valor objetivo
    """
    gap_data = []
    for dimension in DIMENSION_WEIGHTS.keys():
        componentes = COMPONENT_WEIGHTS[dimension].keys()
        for comp in componentes:
            valor = getattr(evaluacion, comp)
            if valor is not None:
                valor_actual = evaluacion.valor_a_porcentaje(valor)
                gap = 100 - valor_actual
                gap_data.append({
                    'Componente': comp.split('_')[0].upper(),
                    'Valor Actual': valor_actual,
                    'Brecha': gap
                })

    df_gap = pd.DataFrame(gap_data)
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=df_gap['Componente'],
        y=df_gap['Valor Actual'],
        name='Valor Actual',
        marker_color='#4caf50'
    ))
    fig.add_trace(go.Bar(
        x=df_gap['Componente'],
        y=df_gap['Brecha'],
        name='Brecha',
        marker_color='#dc3545'
    ))
    
    fig.update_layout(
        barmode='stack',
        paper_bgcolor='white',
        plot_bgcolor='white',
        showlegend=True,
        legend_title_text='',
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="center",
            x=0.5
        ),
        xaxis_title="",
        yaxis_title="Porcentaje (%)",
        height=400,
        margin=dict(t=50, b=30, l=30, r=30)
    )
    
    return fig 