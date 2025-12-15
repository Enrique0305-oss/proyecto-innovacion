"""
Rutas de Reuniones
Endpoints para gestión de reuniones de proyectos
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from datetime import datetime
import json

from app.extensions import db
from app.models.web_user import WebUser
from app.models.meeting import Meeting

# Crear Blueprint
meetings_bp = Blueprint('meetings', __name__)


@meetings_bp.route('/', methods=['GET'])
@jwt_required()
def get_meetings():
    """
    Obtener lista de reuniones
    
    Query Params:
        - project_id: str (filtro por proyecto)
        - status: str (filtro por estado)
        - meeting_type: str (filtro por tipo)
    
    Returns:
        JSON con lista de reuniones
    """
    try:
        query = Meeting.query
        
        # Filtros
        project_id = request.args.get('project_id')
        if project_id:
            query = query.filter(Meeting.project_id == project_id)
        
        status = request.args.get('status')
        if status:
            query = query.filter(Meeting.status == status)
        
        meeting_type = request.args.get('meeting_type')
        if meeting_type:
            query = query.filter(Meeting.meeting_type == meeting_type)
        
        meetings = query.order_by(Meeting.meeting_date.desc()).all()
        
        return jsonify({
            'meetings': [meeting.to_dict() for meeting in meetings],
            'total': len(meetings)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener reuniones',
            'details': str(e)
        }), 500


@meetings_bp.route('/', methods=['POST'])
@jwt_required()
def create_meeting():
    """
    Crear una nueva reunión
    
    Body JSON:
        title: str (requerido)
        description: str
        project_id: str (requerido)
        meeting_date: str (formato YYYY-MM-DD)
        meeting_time: str (formato HH:MM)
        duration: int (minutos)
        meeting_type: str (presencial, virtual, hibrido)
        location: str
        status: str (programada, en_curso, completada, cancelada, reprogramada)
        participant_ids: list[int]
    
    Returns:
        JSON con la reunión creada
    """
    try:
        data = request.get_json()
        
        # Validar campos requeridos
        if not data.get('title') or not data.get('project_id'):
            return jsonify({
                'error': 'Campos requeridos: title, project_id'
            }), 400
        
        # Obtener usuario actual
        current_user_email = get_jwt_identity()
        current_user = WebUser.query.filter_by(email=current_user_email).first()
        
        # Convertir participant_ids a JSON string
        participant_ids = data.get('participant_ids', [])
        participant_ids_json = json.dumps(participant_ids) if participant_ids else None
        
        # Convertir fecha de string a date object
        meeting_date = None
        if data.get('meeting_date'):
            meeting_date = datetime.strptime(data.get('meeting_date'), '%Y-%m-%d').date()
        
        # Crear reunión
        meeting = Meeting(
            title=data.get('title'),
            description=data.get('description'),
            project_id=data.get('project_id'),
            meeting_date=meeting_date,
            meeting_time=data.get('meeting_time'),
            duration=data.get('duration', 60),
            meeting_type=data.get('meeting_type', 'virtual'),
            location=data.get('location'),
            status=data.get('status', 'programada'),
            participant_ids=participant_ids_json,
            created_by=current_user.id if current_user else None
        )
        
        db.session.add(meeting)
        db.session.commit()
        
        return jsonify({
            'message': 'Reunión creada exitosamente',
            'meeting': meeting.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear reunión',
            'details': str(e)
        }), 500


@meetings_bp.route('/<int:id>', methods=['GET'])
@jwt_required()
def get_meeting(id):
    """
    Obtener detalles de una reunión específica
    
    Path Params:
        id: ID de la reunión
    
    Returns:
        JSON con los detalles de la reunión
    """
    try:
        # Por ahora simulamos datos
        meeting = {
            'id': id,
            'title': 'Reunión de ejemplo',
            'status': 'programada'
        }
        
        return jsonify({
            'meeting': meeting
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener reunión',
            'details': str(e)
        }), 500


@meetings_bp.route('/<int:id>', methods=['PUT'])
@jwt_required()
def update_meeting(id):
    """
    Actualizar una reunión existente
    
    Path Params:
        id: ID de la reunión
    
    Body JSON:
        Campos a actualizar
    
    Returns:
        JSON con la reunión actualizada
    """
    try:
        data = request.get_json()
        
        # Por ahora solo retornamos éxito
        return jsonify({
            'message': 'Reunión actualizada exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al actualizar reunión',
            'details': str(e)
        }), 500


@meetings_bp.route('/<int:id>', methods=['DELETE'])
@jwt_required()
def delete_meeting(id):
    """
    Eliminar/cancelar una reunión
    
    Path Params:
        id: ID de la reunión
    
    Returns:
        JSON confirmando la eliminación
    """
    try:
        # Por ahora solo retornamos éxito
        return jsonify({
            'message': 'Reunión eliminada exitosamente'
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al eliminar reunión',
            'details': str(e)
        }), 500
