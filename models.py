from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin

db = SQLAlchemy()

class Evaluacion(db.Model):
    __tablename__ = 'evaluacion'
    
    id = db.Column(db.Integer, primary_key=True)
    empresa = db.Column(db.String(100), nullable=False)
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

class Admin(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
