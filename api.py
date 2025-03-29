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
        'estado': e.estado
    } for e in evaluaciones])

# Endpoint para obtener una evaluación específica
@api.route('/evaluaciones/<int:id>', methods=['GET'])
@token_required
def get_evaluacion(id):
    evaluacion = Evaluacion.query.get_or_404(id)
    return jsonify({
        'id': evaluacion.id,
        'empresa': evaluacion.empresa,
        'nit': evaluacion.nit,
        'departamento': evaluacion.departamento,
        'ciudad': evaluacion.ciudad,
        'cantidad_empleados': evaluacion.cantidad_empleados,
        'responsable': evaluacion.responsable,
        'email': evaluacion.email,
        'sector': evaluacion.sector,
        'fecha': evaluacion.fecha.isoformat(),
        'estado': evaluacion.estado
    }) 