from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from weights import DIMENSION_WEIGHTS, COMPONENT_WEIGHTS, DIAGNOSTICS

db = SQLAlchemy()

class Evaluacion(db.Model):
    __tablename__ = 'evaluacion'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=True)
    sector = db.Column(db.String(50), nullable=True)
    fecha = db.Column(db.DateTime, default=datetime.utcnow)
    estado = db.Column(db.String(20), default='incompleto')
    ultima_dimension = db.Column(db.String(50))
    
    # Procesos de Gestión
    p1_identificacion_amenazas = db.Column(db.String(1))
    p2_identificacion_vulnerabilidades = db.Column(db.String(1))
    p3_analisis_riesgos = db.Column(db.String(1))
    p4_valoracion_riesgos = db.Column(db.String(1))
    p5_reduccion_riesgos = db.Column(db.String(1))
    p6_monitoreo_revision = db.Column(db.String(1))
    p7_seguimiento_estrategias = db.Column(db.String(1))
    p8_comunicacion = db.Column(db.String(1))
    
    # Regulaciones y Resiliencia
    pt1_adopcion_certificaciones = db.Column(db.String(1))
    pt2_regulaciones_nacionales = db.Column(db.String(1))
    pt3_plan_gestion_riesgo = db.Column(db.String(1))
    pt4_politica_gestion_riesgo = db.Column(db.String(1))
    pt5_politica_seguridad = db.Column(db.String(1))
    pt6_sistema_sarlaft = db.Column(db.String(1))
    pt7_memoria_emergencias = db.Column(db.String(1))
    pt8_planes_emergencia = db.Column(db.String(1))
    pt9_seguros_polizas = db.Column(db.String(1))
    
    # Equipamiento y Materiales
    eq1_control_acceso = db.Column(db.String(1))
    eq2_controles_seguridad = db.Column(db.String(1))
    eq3_controles_ciberseguridad = db.Column(db.String(1))
    eq4_redes_deteccion = db.Column(db.String(1))
    eq5_brigadas_respuesta = db.Column(db.String(1))
    eq6_formacion_capacitacion = db.Column(db.String(1))
    
    # Integración y Transversalidad
    it1_transversalizacion = db.Column(db.String(1))
    it2_protocolos_comunicacion = db.Column(db.String(1))
    it3_planes_ayuda = db.Column(db.String(1))
    it5_retroalimentacion = db.Column(db.String(1))
    it6_mecanismos_articulacion = db.Column(db.String(1))
    
    # Organización
    or1_area_gestion = db.Column(db.String(1))
    or2_presupuesto = db.Column(db.String(1))
    or3_personal_dedicacion = db.Column(db.String(1))
    or4_proyectos_gestion = db.Column(db.String(1))
    or5_inclusion_gestion = db.Column(db.String(1))
    
    dimensiones_completadas = db.Column(db.JSON, default=lambda: {
        'procesos_gestion': False,
        'regulaciones_resiliencia': False,
        'equipamiento_materiales': False,
        'integracion_transversalidad': False,
        'organizacion': False
    })

    def valor_a_porcentaje(self, valor):
        if valor is None:
            return 0
        try:
            # Convertir el valor a entero
            valor = int(valor)
            # Convierte valor 0-4 a porcentaje
            conversion = {0: 0, 1: 25, 2: 50, 3: 75, 4: 100}
            return conversion.get(valor, 0)
        except (ValueError, TypeError):
            return 0

    def calcular_puntaje_componente(self, dimension, componente):
        valor = getattr(self, componente)
        porcentaje = self.valor_a_porcentaje(valor)
        peso = COMPONENT_WEIGHTS[dimension][componente]
        return (porcentaje * peso) / 100

    def calcular_puntaje_dimension(self, dimension):
        """Calcula el puntaje de una dimensión específica"""
        componentes = COMPONENT_WEIGHTS[dimension].keys()
        # Suma de los puntajes ponderados de cada componente
        suma_ponderada = sum(self.calcular_puntaje_componente(dimension, comp) for comp in componentes)
        return suma_ponderada  # Ya está en porcentaje (0-100)

    def obtener_diagnostico(self, dimension):
        try:
            # Calcular el puntaje de la dimensión
            puntaje = self.calcular_puntaje_dimension(dimension)
            
            # Buscar el diagnóstico correspondiente
            for rango, diagnostico in DIAGNOSTICS[dimension].items():
                if rango[0] <= puntaje <= rango[1]:
                    return diagnostico
                    
            # Si no encuentra un rango que coincida
            print(f"No se encontró diagn��stico para dimensión {dimension} con puntaje {puntaje}")
            return "No hay diagnóstico disponible"
            
        except Exception as e:
            print(f"Error al obtener diagnóstico: {str(e)}")
            return "Error al obtener diagnóstico"

    def calcular_puntaje_total(self):
        """Calcula el puntaje total ponderado de todas las dimensiones"""
        puntaje_total = 0
        for dimension, peso in DIMENSION_WEIGHTS.items():
            # Obtener el puntaje de la dimensión (0-100)
            puntaje_dimension = self.calcular_puntaje_dimension(dimension)
            # Aplicar el peso de la dimensión
            puntaje_ponderado = (puntaje_dimension * peso) / 100
            puntaje_total += puntaje_ponderado
        return puntaje_total

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
