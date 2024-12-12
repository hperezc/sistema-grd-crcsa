from dash import Dash, html, dcc, Input, Output
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from flask import Flask
from flask.helpers import get_root_path
import dash_bootstrap_components as dbc
from models import Evaluacion, db

def init_dashboard(server):
    dash_app = Dash(
        server=server,
        routes_pathname_prefix="/dashboard/",
        external_stylesheets=[dbc.themes.BOOTSTRAP]
    )

    # Obtener datos
    def get_dashboard_data():
        evaluaciones = Evaluacion.query.all()
        df = pd.DataFrame([{
            'empresa': e.empresa,
            'fecha': e.fecha,
            'estado': e.estado,
            'procesos_gestion': float(e.p1_identificacion_amenazas or 0)/4 + \
                               float(e.p2_identificacion_vulnerabilidades or 0)/4 + \
                               float(e.p3_analisis_riesgos or 0)/4 + \
                               float(e.p4_valoracion_riesgos or 0)/4 + \
                               float(e.p5_reduccion_riesgos or 0)/4 + \
                               float(e.p6_monitoreo_revision or 0)/4 + \
                               float(e.p7_seguimiento_estrategias or 0)/4 + \
                               float(e.p8_comunicacion or 0)/4,
            'regulaciones': float(e.pt1_adopcion_certificaciones or 0)/4 + \
                           float(e.pt2_regulaciones_nacionales or 0)/4 + \
                           float(e.pt3_plan_gestion_riesgo or 0)/4 + \
                           float(e.pt4_politica_gestion_riesgo or 0)/4 + \
                           float(e.pt5_politica_seguridad or 0)/4 + \
                           float(e.pt6_sistema_sarlaft or 0)/4 + \
                           float(e.pt7_memoria_emergencias or 0)/4 + \
                           float(e.pt8_planes_emergencia or 0)/4 + \
                           float(e.pt9_seguros_polizas or 0)/4,
            'equipamiento': float(e.eq1_control_acceso or 0)/4 + \
                           float(e.eq2_controles_seguridad or 0)/4 + \
                           float(e.eq3_controles_ciberseguridad or 0)/4 + \
                           float(e.eq4_redes_deteccion or 0)/4 + \
                           float(e.eq5_brigadas_respuesta or 0)/4 + \
                           float(e.eq6_formacion_capacitacion or 0)/4,
            'integracion': float(e.it1_transversalizacion or 0)/4 + \
                          float(e.it2_protocolos_comunicacion or 0)/4 + \
                          float(e.it3_planes_ayuda or 0)/4 + \
                          float(e.it5_retroalimentacion or 0)/4 + \
                          float(e.it6_mecanismos_articulacion or 0)/4,
            'organizacion': float(e.or1_area_gestion or 0)/4 + \
                           float(e.or2_presupuesto or 0)/4 + \
                           float(e.or3_personal_dedicacion or 0)/4 + \
                           float(e.or4_proyectos_gestion or 0)/4 + \
                           float(e.or5_inclusion_gestion or 0)/4
        } for e in evaluaciones])
        
        # Filtrar solo evaluaciones completas para los cálculos
        df_completas = df[df['estado'] == 'completo']
        
        return df_completas  # Retornar solo las evaluaciones completas

    # Layout del dashboard
    dash_app.layout = dbc.Container([
        html.H1("Dashboard Analítico de Evaluaciones", className="text-center mb-4 text-danger"),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Filtros", className="bg-dark text-white"),
                    dbc.CardBody([
                        html.Label("Empresa:", className="mb-2"),
                        dcc.Dropdown(
                            id='empresa-filter',
                            options=[],  # Se llenará dinámicamente
                            multi=True,
                            placeholder="Seleccione empresa(s)",
                            className="mb-3"
                        ),
                        html.Label("Dimensión:", className="mb-2"),
                        dcc.Dropdown(
                            id='dimension-filter',
                            options=[
                                {'label': 'Procesos de Gestión', 'value': 'procesos_gestion'},
                                {'label': 'Regulaciones y Protección', 'value': 'regulaciones'},
                                {'label': 'Equipamiento y Capacidades', 'value': 'equipamiento'},
                                {'label': 'Integración', 'value': 'integracion'},
                                {'label': 'Organización', 'value': 'organizacion'}
                            ],
                            multi=True,
                            placeholder="Seleccione dimensión(es)",
                        ),
                        html.Label("Fecha:", className="mb-2 mt-3"),
                        dcc.DatePickerRange(
                            id='date-filter',
                            start_date_placeholder_text="Fecha inicial",
                            end_date_placeholder_text="Fecha final",
                            display_format='DD/MM/YYYY',
                            className="mb-3"
                        ),
                    ])
                ], className="shadow mb-4")
            ], width=12)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Total Evaluaciones", className="text-center text-muted mb-2"),
                        html.H2(id="kpi-total", className="text-center text-danger")
                    ])
                ], className="shadow mb-4")
            ], xs=6, md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Evaluaciones Completas", className="text-center text-muted mb-2"),
                        html.H2(id="kpi-completas", className="text-center text-success")
                    ])
                ], className="shadow mb-4")
            ], xs=6, md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Promedio Global", className="text-center text-muted mb-2"),
                        html.H2(id="kpi-promedio", className="text-center text-primary")
                    ])
                ], className="shadow mb-4")
            ], xs=6, md=3),
            dbc.Col([
                dbc.Card([
                    dbc.CardBody([
                        html.H4("Dimensión más Fuerte", className="text-center text-muted mb-2"),
                        html.H2(id="kpi-dimension", className="text-center text-info")
                    ])
                ], className="shadow mb-4")
            ], xs=6, md=3)
        ]),
        dcc.Interval(
            id='interval-component',
            interval=30*1000,
            n_intervals=0
        ),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Promedio por Dimensión", className="bg-dark text-white"),
                    dbc.CardBody(
                        dcc.Graph(id='promedio-dimensiones')
                    )
                ], className="shadow mb-4")
            ], xs=12, md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Estado de Evaluaciones", className="bg-dark text-white"),
                    dbc.CardBody(
                        dcc.Graph(id='distribucion-estados')
                    )
                ], className="shadow mb-4")
            ], xs=12, md=6)
        ]),
        dbc.Row([
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Nivel de Madurez Global", className="bg-dark text-white"),
                    dbc.CardBody(
                        dcc.Graph(id='gauge-global')
                    )
                ], className="shadow mb-4")
            ], xs=12, md=6),
            dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Análisis por Dimensiones", className="bg-dark text-white"),
                    dbc.CardBody(
                        dcc.Graph(id='radar-dimensiones')
                    )
                ], className="shadow mb-4")
            ], xs=12, md=6)
        ])
    ], fluid=True, className="p-4")

    def init_callbacks(dash_app):
        # Callback para actualizar las opciones del dropdown de empresas
        @dash_app.callback(
            Output('empresa-filter', 'options'),
            [Input('interval-component', 'n_intervals')]
        )
        def update_empresa_options(_):
            df = get_dashboard_data()
            return [{'label': empresa, 'value': empresa} for empresa in df['empresa'].unique()]

        # Callback principal actualizado para incluir los filtros
        @dash_app.callback(
            [Output('promedio-dimensiones', 'figure'),
             Output('distribucion-estados', 'figure'),
             Output('radar-dimensiones', 'figure'),
             Output('gauge-global', 'figure')],
            [Input('interval-component', 'n_intervals'),
             Input('empresa-filter', 'value'),
             Input('dimension-filter', 'value'),
             Input('date-filter', 'start_date'),
             Input('date-filter', 'end_date')]
        )
        def update_graphs(_, selected_empresas, selected_dimensiones, start_date, end_date):
            df = get_dashboard_data()
            if df.empty:
                return [{} for _ in range(4)]

            # Aplicar filtros
            if selected_empresas:
                df = df[df['empresa'].isin(selected_empresas)]
            
            numeric_columns = ['procesos_gestion', 'regulaciones', 'equipamiento', 'integracion', 'organizacion']
            if selected_dimensiones:
                numeric_columns = [col for col in numeric_columns if col in selected_dimensiones]

            if df.empty or not numeric_columns:
                return [{} for _ in range(4)]

            # Configuración común para todos los gráficos en móviles
            mobile_layout = dict(
                autosize=True,
                margin=dict(l=20, r=20, t=30, b=20),
                height=350,  # Altura fija para móviles
                legend=dict(
                    orientation="h",
                    yanchor="bottom",
                    y=1.02,
                    xanchor="right",
                    x=1
                )
            )

            # Actualizar gráfico de barras con configuración responsiva
            fig1 = px.bar(
                df[numeric_columns].mean().reset_index(),
                x='index', y=0,
                title='',
                labels={'index': 'Dimensión', '0': 'Promedio'},
                color_discrete_sequence=['#FFB2B2']
            )
            fig1.update_layout(
                **mobile_layout,
                plot_bgcolor='white',
                paper_bgcolor='white',
                showlegend=False,
                xaxis_title='',
                yaxis_title='Puntaje Promedio',
                yaxis=dict(range=[0, 4]),
                xaxis=dict(tickangle=-45)
            )
            
            # Actualizar gráfico dona con configuración responsiva
            fig2 = px.pie(
                df, names='estado',
                title='',
                color_discrete_sequence=['#E31837', '#FFB2B2'],
                hole=0.6
            )
            fig2.update_layout(
                **mobile_layout,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            # Actualizar gráfico radar con configuración responsiva
            ultima_eval = df.iloc[-1]
            fig3 = go.Figure(data=go.Scatterpolar(
                r=[ultima_eval[col] for col in numeric_columns],
                theta=[col.replace('_', ' ').title() for col in numeric_columns],
                fill='toself',
                fillcolor='rgba(227, 24, 55, 0.3)',
                line_color='#E31837'
            ))
            fig3.update_layout(
                **mobile_layout,
                plot_bgcolor='white',
                paper_bgcolor='white',
                polar=dict(
                    radialaxis=dict(
                        visible=True,
                        range=[0, 4],
                        gridcolor='#506784',
                        showline=True
                    ),
                    angularaxis=dict(
                        gridcolor='#506784'
                    )
                ),
                showlegend=False
            )
            
            # Actualizar gauge con configuración responsiva
            fig4 = go.Figure(go.Indicator(
                mode="gauge+number",
                value=df[numeric_columns].mean().mean(),
                title={'text': "Nivel de Madurez Global"},
                domain={'x': [0, 1], 'y': [0, 1]},
                gauge={
                    'axis': {'range': [0, 4]},
                    'bar': {'color': "#E31837"},
                    'steps': [
                        {'range': [0, 1], 'color': "#FFE5E5"},
                        {'range': [1, 2], 'color': "#FFB2B2"},
                        {'range': [2, 3], 'color': "#FF8080"},
                        {'range': [3, 4], 'color': "#FF4D4D"}
                    ],
                    'threshold': {
                        'line': {'color': "red", 'width': 4},
                        'thickness': 0.75,
                        'value': 3
                    }
                }
            ))
            fig4.update_layout(
                **mobile_layout,
                plot_bgcolor='white',
                paper_bgcolor='white'
            )
            
            return fig1, fig2, fig3, fig4

        @dash_app.callback(
            [Output('kpi-total', 'children'),
             Output('kpi-completas', 'children'),
             Output('kpi-promedio', 'children'),
             Output('kpi-dimension', 'children')],
            [Input('interval-component', 'n_intervals'),
             Input('empresa-filter', 'value'),
             Input('dimension-filter', 'value'),
             Input('date-filter', 'start_date'),
             Input('date-filter', 'end_date')]
        )
        def update_kpis(_, selected_empresas, selected_dimensiones, start_date, end_date):
            df = get_dashboard_data()
            
            # Definir numeric_columns
            numeric_columns = ['procesos_gestion', 'regulaciones', 'equipamiento', 'integracion', 'organizacion']
            if selected_dimensiones:
                numeric_columns = [col for col in numeric_columns if col in selected_dimensiones]
            
            # Aplicar filtros
            if selected_empresas:
                df = df[df['empresa'].isin(selected_empresas)]
            if start_date and end_date:
                df = df[(df['fecha'] >= start_date) & (df['fecha'] <= end_date)]
            
            if df.empty or not numeric_columns:
                return "0", "0", "0.00", "No hay datos"
            
            total = len(df)
            completas = len(df[df['estado'] == 'completo'])
            promedio = round(df[numeric_columns].mean().mean(), 2)
            dimension_fuerte = df[numeric_columns].mean().idxmax().replace('_', ' ').title()
            
            return f"{total}", f"{completas}", f"{promedio}", f"{dimension_fuerte}"

        

    init_callbacks(dash_app)
    
    return dash_app.server 