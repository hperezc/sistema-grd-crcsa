from flask import Blueprint, jsonify, request
from functools import wraps
import jwt
from datetime import datetime, timedelta
from models import Evaluacion, db
import os

api = Blueprint('api', __name__)

# Función para verificar el token JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'message': 'Token faltante'}), 401
        
        try:
            # Remover 'Bearer ' del token
            token = token.split(' ')[1]
            data = jwt.decode(token, os.getenv('JWT_SECRET_KEY'), algorithms=['HS256'])
        except:
            return jsonify({'message': 'Token inválido'}), 401
            
        return f(*args, **kwargs)
    return decorated

# Endpoint para obtener token
@api.route('/token', methods=['POST'])
def get_token():
    auth = request.authorization
    if not auth or not auth.username or not auth.password:
        return jsonify({'message': 'Credenciales inválidas'}), 401
        
    # Aquí deberías verificar las credenciales contra tu base de datos
    if auth.username == os.getenv('API_USERNAME') and auth.password == os.getenv('API_PASSWORD'):
        token = jwt.encode({
            'user': auth.username,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, os.getenv('JWT_SECRET_KEY'))
        
        return jsonify({'token': token})
    
    return jsonify({'message': 'Credenciales inválidas'}), 401

# Endpoint para obtener evaluaciones
@api.route('/evaluaciones', methods=['GET'])
@token_required
def get_evaluaciones():
    evaluaciones = Evaluacion.query.all()
    return jsonify([{
        'id': e.id,
        'empresa': e.empresa,
        'nit': e.nit,
        'email': e.email,
        'sector': e.sector,
        'fecha': e.fecha.isoformat(),
        'estado': e.estado,
        'puntaje_total': e.calcular_puntaje_total()
    } for e in evaluaciones])

# Endpoint para obtener una evaluación específica con todos sus detalles
@api.route('/evaluaciones/<int:id>', methods=['GET'])
@token_required
def get_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    
    # Convertir valores de None a cadenas vacías para evitar problemas en la serialización
    def safe_value(val):
        return val if val is not None else ""
    
    # Obtener todos los valores de dimensiones
    procesos_values = {
        'p1_identificacion_amenazas': safe_value(evaluacion.p1_identificacion_amenazas),
        'p2_identificacion_vulnerabilidades': safe_value(evaluacion.p2_identificacion_vulnerabilidades),
        'p3_analisis_riesgos': safe_value(evaluacion.p3_analisis_riesgos),
        'p4_valoracion_riesgos': safe_value(evaluacion.p4_valoracion_riesgos),
        'p5_reduccion_riesgos': safe_value(evaluacion.p5_reduccion_riesgos),
        'p6_monitoreo_revision': safe_value(evaluacion.p6_monitoreo_revision),
        'p7_seguimiento_estrategias': safe_value(evaluacion.p7_seguimiento_estrategias),
        'p8_comunicacion': safe_value(evaluacion.p8_comunicacion)
    }
    
    regulaciones_values = {
        'pt1_adopcion_certificaciones': safe_value(evaluacion.pt1_adopcion_certificaciones),
        'pt2_regulaciones_nacionales': safe_value(evaluacion.pt2_regulaciones_nacionales),
        'pt3_plan_gestion_riesgo': safe_value(evaluacion.pt3_plan_gestion_riesgo),
        'pt4_politica_gestion_riesgo': safe_value(evaluacion.pt4_politica_gestion_riesgo),
        'pt5_politica_seguridad': safe_value(evaluacion.pt5_politica_seguridad),
        'pt6_sistema_sarlaft': safe_value(evaluacion.pt6_sistema_sarlaft),
        'pt7_memoria_emergencias': safe_value(evaluacion.pt7_memoria_emergencias),
        'pt8_planes_emergencia': safe_value(evaluacion.pt8_planes_emergencia),
        'pt9_seguros_polizas': safe_value(evaluacion.pt9_seguros_polizas) if hasattr(evaluacion, 'pt9_seguros_polizas') else ""
    }
    
    equipamiento_values = {
        'eq1_control_acceso': safe_value(evaluacion.eq1_control_acceso),
        'eq2_controles_seguridad': safe_value(evaluacion.eq2_controles_seguridad),
        'eq3_controles_ciberseguridad': safe_value(evaluacion.eq3_controles_ciberseguridad),
        'eq4_redes_deteccion': safe_value(evaluacion.eq4_redes_deteccion),
        'eq5_brigadas_respuesta': safe_value(evaluacion.eq5_brigadas_respuesta),
        'eq6_formacion_capacitacion': safe_value(evaluacion.eq6_formacion_capacitacion)
    }
    
    integracion_values = {
        'it1_transversalizacion': safe_value(evaluacion.it1_transversalizacion),
        'it2_protocolos_comunicacion': safe_value(evaluacion.it2_protocolos_comunicacion),
        'it3_planes_ayuda': safe_value(evaluacion.it3_planes_ayuda),
        'it5_retroalimentacion': safe_value(evaluacion.it5_retroalimentacion),
        'it6_mecanismos_articulacion': safe_value(evaluacion.it6_mecanismos_articulacion)
    }
    
    organizacion_values = {
        'or1_area_gestion': safe_value(evaluacion.or1_area_gestion),
        'or2_presupuesto': safe_value(evaluacion.or2_presupuesto),
        'or3_personal_dedicacion': safe_value(evaluacion.or3_personal_dedicacion),
        'or4_proyectos_gestion': safe_value(evaluacion.or4_proyectos_gestion),
        'or5_inclusion_gestion': safe_value(evaluacion.or5_inclusion_gestion)
    }
    
    # Calcular puntajes por dimensión
    puntajes = {
        'puntaje_total': evaluacion.calcular_puntaje_total(),
        'puntaje_procesos': evaluacion.calcular_puntaje_dimension('procesos'),
        'puntaje_regulaciones': evaluacion.calcular_puntaje_dimension('regulaciones'),
        'puntaje_equipamiento': evaluacion.calcular_puntaje_dimension('equipamiento'),
        'puntaje_integracion': evaluacion.calcular_puntaje_dimension('integracion'),
        'puntaje_organizacion': evaluacion.calcular_puntaje_dimension('organizacion')
    }
    
    # Devolver datos completos incluyendo resultados
    return jsonify({
        # Datos básicos
        'id': evaluacion.id,
        'empresa': evaluacion.empresa,
        'nit': evaluacion.nit,
        'departamento': evaluacion.departamento,
        'ciudad': evaluacion.ciudad,
        'cantidad_empleados': evaluacion.cantidad_empleados,
        'responsable': evaluacion.responsable,
        'rol': evaluacion.rol,
        'telefono_fijo': evaluacion.telefono_fijo,
        'celular': evaluacion.celular,
        'email': evaluacion.email,
        'sector': evaluacion.sector,
        'fecha': evaluacion.fecha.isoformat(),
        'estado': evaluacion.estado,
        'ultima_dimension': evaluacion.ultima_dimension,
        
        # Puntajes
        'puntajes': puntajes,
        
        # Respuestas por dimensión
        'procesos': procesos_values,
        'regulaciones': regulaciones_values,
        'equipamiento': equipamiento_values,
        'integracion': integracion_values,
        'organizacion': organizacion_values,
        
        # URL para ver resultados en la web
        'url_resultados': f"{os.getenv('BASE_URL', 'https://sistema-grd-crcsa.onrender.com')}/resultados/{evaluacion.id}"
    })

# Endpoint para obtener solo resultados y puntajes de una evaluación
@api.route('/evaluaciones/<int:id>/resultados', methods=['GET'])
@token_required
def get_evaluacion_resultados(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    
    # Calcular puntajes por dimensión
    puntajes = {
        'puntaje_total': evaluacion.calcular_puntaje_total(),
        'puntaje_procesos': evaluacion.calcular_puntaje_dimension('procesos'),
        'puntaje_regulaciones': evaluacion.calcular_puntaje_dimension('regulaciones'),
        'puntaje_equipamiento': evaluacion.calcular_puntaje_dimension('equipamiento'),
        'puntaje_integracion': evaluacion.calcular_puntaje_dimension('integracion'),
        'puntaje_organizacion': evaluacion.calcular_puntaje_dimension('organizacion')
    }
    
    return jsonify({
        'id': evaluacion.id,
        'empresa': evaluacion.empresa,
        'puntajes': puntajes,
        'fecha': evaluacion.fecha.isoformat(),
        'url_resultados': f"{os.getenv('BASE_URL', 'https://sistema-grd-crcsa.onrender.com')}/resultados/{evaluacion.id}"
    }) 