import dash
from dash import html, dcc
import plotly.express as px
import plotly.graph_objects as go
from dash.dependencies import Input, Output
import pandas as pd
from flask_sqlalchemy import SQLAlchemy
from models import Evaluacion
from weights import COMPONENT_WEIGHTS, DIMENSION_WEIGHTS
from datetime import datetime
import dash_bootstrap_components as dbc

def create_card_header(title, tooltip_text):
    return html.Div([
        html.Div([
            html.H5(title, className="mb-0"),
            html.Div([
                html.I(className="fas fa-info-circle tooltip-icon"),
                html.Div(tooltip_text, className="custom-tooltip")
            ], className="tooltip-container")
        ], className="header-content")
    ], className="card-header bg-dark text-white")

def init_dashboard(server):
    dash_app = dash.Dash(
        server=server,
        routes_pathname_prefix='/dashboard/',
        external_stylesheets=[
            'https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css',
            'https://use.fontawesome.com/releases/v5.15.4/css/all.css',
            '/static/dashboard.css'
        ]
    )

    # Layout del dashboard
    dash_app.layout = html.Div([
        # Agregar un header más elaborado
        html.Div([
            html.Div([
                html.H1("Dashboard Analítico de Gestión del Riesgo", 
                       className="text-center mb-4 mt-3 dashboard-title"),
                html.P("Análisis integral del nivel de madurez y oportunidades de mejora",
                      className="text-center text-muted mb-4")
            ], className="col-12")
        ], className="dashboard-header row"),

        # Contenedor principal
        html.Div([
            # Filtro de empresas (ajustado para mejor responsividad)
            html.Div([
                html.Div([
                    html.Label("Seleccionar Empresa:", className="font-weight-bold"),
                    dcc.Dropdown(
                        id='empresa-dropdown',
                        options=[],
                        className="mb-4"
                    )
                ], className="col-12 col-lg-6 mx-auto")
            ], className="row mb-4"),

            # KPIs (ajustados para mejor responsividad)
            html.Div([
                html.Div([
                    # Primera fila de KPIs
                    html.Div([
                        # KPI Puntaje Total
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-chart-line mb-2", style={'font-size': '20px'}),
                                html.H6("Puntaje Total", className="text-muted mb-1 small"),
                                html.H4(id="kpi-puntaje-total", className="mb-0"),
                                html.Span("Nivel de Madurez", className="text-muted small")
                            ], className="card-body text-center")
                        ], className="card kpi-card shadow-sm border-left border-primary"),
                        
                        # KPI Mejor Dimensión
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-arrow-up mb-2", style={'font-size': '20px'}),
                                html.H6("Mejor Dimensión", className="text-muted mb-1 small"),
                                html.H4(id="kpi-mejor-dimension", className="mb-0"),
                                html.Span(id="kpi-mejor-dimension-valor", className="text-muted small")
                            ], className="card-body text-center")
                        ], className="card kpi-card shadow-sm border-left border-success"),
                        
                        # KPI Peor Dimensión
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-arrow-down mb-2", style={'font-size': '20px'}),
                                html.H6("Peor Dimensión", className="text-muted mb-1 small"),
                                html.H4(id="kpi-peor-dimension", className="mb-0"),
                                html.Span(id="kpi-peor-dimension-valor", className="text-muted small")
                            ], className="card-body text-center")
                        ], className="card kpi-card shadow-sm border-left border-danger"),
                        
                        # KPI Mayor Brecha
                        html.Div([
                            html.Div([
                                html.I(className="fas fa-exclamation-triangle mb-2", style={'font-size': '20px'}),
                                html.H6("Mayor Brecha", className="text-muted mb-1 small"),
                                html.H4(id="kpi-mayor-brecha", className="mb-0"),
                                html.Span(id="kpi-mayor-brecha-valor", className="text-muted small")
                            ], className="card-body text-center")
                        ], className="card kpi-card shadow-sm border-left border-warning")
                    ], className="row row-cols-2 row-cols-sm-2 row-cols-lg-4 g-2 g-lg-3 mb-3"),
                ], className="container-fluid px-2")
            ], className="bg-light p-3 rounded shadow-sm mb-4"),

            # Gráficos (ajustados para mejor responsividad)
            html.Div([
                # Primera fila de gráficos
                html.Div([
                    html.Div([
                        create_card_header(
                            "Nivel de Madurez por Dimensión",
                            "Visualización radial que muestra el nivel de madurez alcanzado en cada dimensión. "
                            "Permite identificar rápidamente las áreas más fuertes y débiles de la organización."
                        ),
                        html.Div([
                            dcc.Graph(
                                id='radar-chart',
                                config={'responsive': True}
                            )
                        ], className="card-body")
                    ], className="card chart-card shadow-sm mb-4 col-12 col-lg-6"),
                    
                    html.Div([
                        create_card_header("Puntaje Total de Madurez", "Medidor que indica el nivel general de madurez de la organización. El color indica el estado: rojo (crítico), amarillo (en desarrollo), verde (óptimo)."),
                        html.Div([
                            dcc.Graph(
                                id='gauge-chart',
                                config={
                                    'responsive': True,
                                    'displayModeBar': False,
                                    'staticPlot': False
                                },
                                style={
                                    'height': '100%',
                                    'width': '100%'
                                }
                            )
                        ], className="card-body graph-container")
                    ], className="card chart-card shadow-sm mb-4 col-12 col-lg-6")
                ], className="row"),

                # Segunda fila de gráficos
                html.Div([
                    html.Div([
                        create_card_header("Componentes por Dimensión", "Gráfico de barras que muestra la contribución de cada componente dentro de su dimensión. Permite comparar la distribución de componentes entre diferentes dimensiones."),
                        html.Div([
                            dcc.Graph(
                                id='stacked-bar-chart',
                                config={'responsive': True}
                            )
                        ], className="card-body graph-container")
                    ], className="card chart-card shadow-sm mb-4 col-12 col-lg-6"),
                    
                    html.Div([
                        create_card_header("Mapa de Calor de Componentes", "Visualización que muestra la intensidad de los valores de cada componente mediante colores. Rojo indica valores bajos, amarillo valores medios y verde valores altos."),
                        html.Div([
                            dcc.Graph(
                                id='heatmap-chart',
                                config={'responsive': True}
                            )
                        ], className="card-body graph-container")
                    ], className="card chart-card shadow-sm mb-4 col-12 col-lg-6")
                ], className="row"),

                # Tercera fila de gráficos
                html.Div([
                    html.Div([
                        create_card_header("Análisis de Pareto", "Gráfico que combina barras y línea acumulativa para identificar los componentes más significativos y su contribución al total del sistema."),
                        html.Div([
                            dcc.Graph(
                                id='pareto-chart',
                                config={'responsive': True}
                            )
                        ], className="card-body graph-container")
                    ], className="card chart-card shadow-sm mb-4 col-12 col-lg-6"),
                    
                    html.Div([
                        create_card_header("Análisis de Brechas", "Visualización que muestra la diferencia entre el estado actual y el objetivo (100%) para cada componente, identificando las mayores oportunidades de mejora."),
                        html.Div([
                            dcc.Graph(
                                id='gap-chart',
                                config={'responsive': True}
                            )
                        ], className="card-body graph-container")
                    ], className="card chart-card shadow-sm mb-4 col-12 col-lg-6")
                ], className="row")
            ], className="container-fluid")
        ], className="container-fluid px-2 px-md-4 pb-4")
    ], className="container-fluid px-4 pb-4")

    @dash_app.callback(
        [Output('empresa-dropdown', 'options'),
         Output('empresa-dropdown', 'value')],
        [Input('empresa-dropdown', 'search_value')]
    )
    def update_dropdown_options(search_value):
        empresas = Evaluacion.query.with_entities(
            Evaluacion.id, 
            Evaluacion.empresa
        ).distinct().all()
        
        options = [{'label': emp.empresa, 'value': emp.id} for emp in empresas]
        return options, options[0]['value'] if options else None

    @dash_app.callback(
        [Output('radar-chart', 'figure'),
         Output('stacked-bar-chart', 'figure'),
         Output('gauge-chart', 'figure'),
         Output('heatmap-chart', 'figure'),
         Output('pareto-chart', 'figure'),
         Output('gap-chart', 'figure')],
        [Input('empresa-dropdown', 'value')]
    )
    def update_graphs(evaluacion_id):
        if not evaluacion_id:
            return {}, {}, {}, {}, {}, {}

        evaluacion = Evaluacion.query.get(evaluacion_id)
        
        def simplificar_componente(comp_name):
            return comp_name.split('_')[0].upper()  # P1, P2, EQ1, etc.

        # Gráfico de radar
        dimensiones = list(DIMENSION_WEIGHTS.keys())
        valores = [evaluacion.calcular_puntaje_dimension(dim) for dim in dimensiones]
        
        radar_fig = go.Figure(data=go.Scatterpolar(
            r=valores,
            theta=[dim.upper() for dim in dimensiones],
            fill='toself',
            name='Nivel de Madurez',
            line=dict(color='#dc3545')
        ))
        
        radar_fig.update_layout(
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
            margin=dict(t=20, b=20, l=30, r=30),
            autosize=True
        )

        # Gráfico de barras apiladas
        data_bars = []
        for dimension in DIMENSION_WEIGHTS.keys():
            componentes = COMPONENT_WEIGHTS[dimension].keys()
            for comp in componentes:
                valor = getattr(evaluacion, comp)
                if valor is not None:
                    data_bars.append({
                        'Dimensión': dimension.upper(),
                        'Componente': simplificar_componente(comp),
                        'Valor': valor,
                        'Porcentaje': evaluacion.valor_a_porcentaje(valor)
                    })

        df_bars = pd.DataFrame(data_bars)
        stacked_fig = px.bar(
            df_bars,
            x='Dimensión',
            y='Porcentaje',
            color='Componente',
            title=''
        )
        stacked_fig.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=True,
            legend_title_text='',
            xaxis_title="",
            yaxis_title="Porcentaje (%)"
        )

        # Gauge chart
        puntaje_total = evaluacion.calcular_puntaje_total()
        gauge_fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=puntaje_total,
            domain={'x': [0, 1], 'y': [0, 1]},
            number={'suffix': "%"},
            gauge={
                'axis': {'range': [0, 100]},
                'bar': {'color': "#000000"},
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
        gauge_fig.update_layout(
            paper_bgcolor='white',
            font={'color': "black", 'family': "Arial"},
            height=350,
            margin=dict(t=20, b=20, l=30, r=30),
            autosize=True
        )

        # Heatmap
        heatmap_data = []
        for dimension in DIMENSION_WEIGHTS.keys():
            componentes = COMPONENT_WEIGHTS[dimension].keys()
            for comp in componentes:
                valor = getattr(evaluacion, comp)
                if valor is not None:
                    heatmap_data.append({
                        'Dimensión': dimension.upper(),
                        'Componente': simplificar_componente(comp),
                        'Valor': evaluacion.valor_a_porcentaje(valor)
                    })

        df_heatmap = pd.DataFrame(heatmap_data)
        df_pivot = df_heatmap.pivot(
            index='Dimensión', 
            columns='Componente', 
            values='Valor'
        )
        
        heatmap_fig = px.imshow(
            df_pivot,
            color_continuous_scale=["#dc3545", "#ffc107", "#4caf50"],
            aspect="auto"
        )
        heatmap_fig.update_layout(
            paper_bgcolor='white',
            plot_bgcolor='white',
            xaxis_title="",
            yaxis_title=""
        )

        # Gráfico de Pareto
        pareto_data = []
        for dimension in DIMENSION_WEIGHTS.keys():
            componentes = COMPONENT_WEIGHTS[dimension].keys()
            for comp in componentes:
                valor = getattr(evaluacion, comp)
                if valor is not None:
                    valor_porcentaje = evaluacion.valor_a_porcentaje(valor)
                    pareto_data.append({
                        'Componente': simplificar_componente(comp),
                        'Valor': valor_porcentaje
                    })

        df_pareto = pd.DataFrame(pareto_data)
        df_pareto = df_pareto.sort_values('Valor', ascending=False)
        df_pareto['Acumulado'] = df_pareto['Valor'].cumsum() / df_pareto['Valor'].sum() * 100

        pareto_fig = go.Figure()
        pareto_fig.add_scatter(
            x=df_pareto['Componente'],
            y=df_pareto['Acumulado'],
            name='% Acumulado',
            fill='tozeroy',
            fillcolor='rgba(0,0,0,0.1)',
            line=dict(color='#000000', width=2)
        )
        pareto_fig.add_trace(go.Bar(
            x=df_pareto['Componente'],
            y=df_pareto['Valor'],
            name='Valor',
            marker_color='#dc3545'
        ))
        pareto_fig.update_layout(
            yaxis=dict(
                title='Valor (%)',
                range=[0, 100],
                tickfont=dict(size=10),
                automargin=True
            ),
            yaxis2=dict(
                title='Acumulado (%)',
                overlaying='y',
                side='right',
                range=[0, 100],
                showgrid=False,
                tickfont=dict(size=10)
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.15,
                xanchor="center",
                x=0.5,
                font=dict(size=10)
            ),
            margin=dict(
                l=50,
                r=50,
                t=20,
                b=80
            ),
            height=400,
            xaxis=dict(
                tickangle=45,
                tickfont=dict(size=10)
            )
        )

        # Asegurarse de que los gráficos se ajusten al contenedor
        pareto_fig.update_layout(
            autosize=False,
            width=None
        )

        # Gráfico de Gap
        gap_data = []
        for dimension in DIMENSION_WEIGHTS.keys():
            componentes = COMPONENT_WEIGHTS[dimension].keys()
            for comp in componentes:
                valor = getattr(evaluacion, comp)
                if valor is not None:
                    valor_actual = evaluacion.valor_a_porcentaje(valor)
                    gap = 100 - valor_actual  # Brecha hasta el valor máximo (100%)
                    gap_data.append({
                        'Componente': simplificar_componente(comp),
                        'Valor Actual': valor_actual,
                        'Brecha': gap
                    })

        df_gap = pd.DataFrame(gap_data)
        gap_fig = go.Figure()
        gap_fig.add_trace(go.Bar(
            x=df_gap['Componente'],
            y=df_gap['Valor Actual'],
            name='Valor Actual',
            marker_color='#4caf50'
        ))
        gap_fig.add_trace(go.Bar(
            x=df_gap['Componente'],
            y=df_gap['Brecha'],
            name='Brecha',
            marker_color='#dc3545'
        ))
        gap_fig.update_layout(
            barmode='stack',
            showlegend=True,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.15,
                xanchor="center",
                x=0.5,
                bgcolor='rgba(255, 255, 255, 0.8)',
                font=dict(size=10)
            ),
            margin=dict(
                l=50,
                r=50,
                t=20,
                b=80
            ),
            paper_bgcolor='white',
            plot_bgcolor='white',
            height=400,
            bargap=0.15,
            yaxis=dict(
                title="Porcentaje (%)",
                gridcolor='lightgray',
                range=[0, 100],
                tickfont=dict(size=10),
                automargin=True
            ),
            xaxis=dict(
                tickangle=45,
                showgrid=False,
                tickfont=dict(size=10)
            )
        )

        # Asegurarse de que los gráficos se ajusten al contenedor
        gap_fig.update_layout(
            autosize=False,
            width=None
        )

        return radar_fig, stacked_fig, gauge_fig, heatmap_fig, pareto_fig, gap_fig

    @dash_app.callback(
        [Output('kpi-puntaje-total', 'children'),
         Output('kpi-mejor-dimension', 'children'),
         Output('kpi-mejor-dimension-valor', 'children'),
         Output('kpi-peor-dimension', 'children'),
         Output('kpi-peor-dimension-valor', 'children'),
         Output('kpi-mayor-brecha', 'children'),
         Output('kpi-mayor-brecha-valor', 'children')],
        [Input('empresa-dropdown', 'value')]
    )
    def update_kpis(evaluacion_id):
        if not evaluacion_id:
            return "-", "-", "-", "-", "-", "-", "-"

        evaluacion = Evaluacion.query.get(evaluacion_id)
        
        # Calcular puntaje total
        puntaje_total = evaluacion.calcular_puntaje_total()
        
        # Calcular puntajes por dimensión
        dimensiones = list(DIMENSION_WEIGHTS.keys())
        puntajes = {dim: evaluacion.calcular_puntaje_dimension(dim) for dim in dimensiones}
        
        # Encontrar mejor y peor dimensión
        mejor_dimension = max(puntajes.items(), key=lambda x: x[1])
        peor_dimension = min(puntajes.items(), key=lambda x: x[1])
        
        # Calcular brechas por componente
        brechas = {}
        for dimension in DIMENSION_WEIGHTS.keys():
            for comp in COMPONENT_WEIGHTS[dimension].keys():
                valor = getattr(evaluacion, comp)
                if valor is not None:
                    valor_porcentaje = evaluacion.valor_a_porcentaje(valor)
                    brecha = 100 - valor_porcentaje
                    brechas[comp] = brecha
        
        # Encontrar la mayor brecha
        mayor_brecha = max(brechas.items(), key=lambda x: x[1])
        
        return (
            f"{puntaje_total:.1f}%",
            mejor_dimension[0].upper(),
            f"Puntaje: {mejor_dimension[1]:.1f}%",
            peor_dimension[0].upper(),
            f"Puntaje: {peor_dimension[1]:.1f}%",
            mayor_brecha[0].split('_')[0].upper(),
            f"Brecha: {mayor_brecha[1]:.1f}%"
        )

    @dash_app.callback(
        Output("loading-output", "children"),
        [Input('empresa-dropdown', 'value')]
    )
    def loading_output(value):
        if not value:
            return ""
        return html.Div(
            html.Div(className="loading-spinner"),
            className="loading-container"
        )

    return dash_app.server