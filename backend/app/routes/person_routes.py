"""
Rutas de Personas
Endpoints para gestión de personas/empleados
"""
from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity

from app.extensions import db
from app.models.person import Person
from app.models.web_user import WebUser

# Crear Blueprint
persons_bp = Blueprint('persons', __name__)


@persons_bp.route('/', methods=['GET'])
@jwt_required()
def get_persons():
    """
    Obtener lista de personas
    
    Query Params:
        - area: str (filtro por área)
        - position: str (filtro por cargo)
        - status: str (filtro por estado)
    
    Returns:
        JSON con lista de personas
    """
    try:
        query = Person.query
        
        # Filtros
        area = request.args.get('area')
        if area:
            query = query.filter(Person.area == area)
        
        position = request.args.get('position')
        if position:
            query = query.filter(Person.role == position)
        
        status = request.args.get('status')
        if status:
            if status == 'active':
                query = query.filter(Person.resigned == False)
            elif status == 'inactive':
                query = query.filter(Person.resigned == True)
        
        # Ordenar por ID (nombre no existe)
        query = query.order_by(Person.person_id)
        
        persons = query.all()
        
        return jsonify({
            'persons': [person.to_dict() for person in persons],
            'total': len(persons)
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener personas',
            'details': str(e)
        }), 500


@persons_bp.route('/<person_id>', methods=['GET'])
@jwt_required()
def get_person(person_id):
    """
    Obtener una persona específica por ID
    
    Path Params:
        person_id: ID de la persona
    
    Returns:
        JSON con los detalles de la persona
    """
    try:
        person = Person.query.get(person_id)
        
        if not person:
            return jsonify({'error': 'Persona no encontrada'}), 404
        
        return jsonify({
            'person': person.to_dict()
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener persona',
            'details': str(e)
        }), 500


@persons_bp.route('/', methods=['POST'])
@jwt_required()
def create_person():
    """
    Crear una nueva persona
    
    Body JSON:
        - person_id: str (requerido, único)
        - name: str (requerido)
        - email: str
        - position: str
        - area: str
        - hire_date: date
        - salary: float
        - skills: str
        - performance_score: int (0-100)
    
    Returns:
        JSON con la persona creada
    """
    try:
        user_id = get_jwt_identity()
        user = WebUser.query.get(user_id)
        
        # Verificar permisos
        if not user.can('users.create'):
            return jsonify({'error': 'Acceso denegado - permisos insuficientes'}), 403
        
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'No se enviaron datos'}), 400
        
        person_id = data.get('person_id')
        name = data.get('name')
        
        if not person_id or not name:
            return jsonify({
                'error': 'Campos requeridos faltantes',
                'required': ['person_id', 'name']
            }), 400
        
        # Verificar que no exista
        if Person.query.get(person_id):
            return jsonify({'error': 'Ya existe una persona con ese ID'}), 409
        
        # Crear persona
        new_person = Person(
            person_id=person_id,
            name=name,
            email=data.get('email'),
            position=data.get('position'),
            area=data.get('area'),
            hire_date=data.get('hire_date'),
            salary=data.get('salary'),
            skills=data.get('skills'),
            performance_score=data.get('performance_score'),
            status='active'
        )
        
        db.session.add(new_person)
        db.session.commit()
        
        return jsonify({
            'message': 'Persona creada exitosamente',
            'person': new_person.to_dict()
        }), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al crear persona',
            'details': str(e)
        }), 500


@persons_bp.route('/<person_id>', methods=['PUT'])
@jwt_required()
def update_person(person_id):
    """
    Actualizar una persona existente
    
    Path Params:
        person_id: ID de la persona
    
    Body JSON:
        Campos a actualizar (todos opcionales)
    
    Returns:
        JSON con la persona actualizada
    """
    try:
        user_id = get_jwt_identity()
        user = WebUser.query.get(user_id)
        
        # Verificar permisos
        if not user.can('users.edit'):
            return jsonify({'error': 'Acceso denegado - permisos insuficientes'}), 403
        
        person = Person.query.get(person_id)
        
        if not person:
            return jsonify({'error': 'Persona no encontrada'}), 404
        
        data = request.get_json()
        
        # Actualizar campos
        if 'name' in data:
            person.name = data['name']
        if 'email' in data:
            person.email = data['email']
        if 'position' in data:
            person.position = data['position']
        if 'area' in data:
            person.area = data['area']
        if 'hire_date' in data:
            person.hire_date = data['hire_date']
        if 'salary' in data:
            person.salary = data['salary']
        if 'skills' in data:
            person.skills = data['skills']
        if 'performance_score' in data:
            person.performance_score = data['performance_score']
        if 'status' in data:
            person.status = data['status']
        
        db.session.commit()
        
        return jsonify({
            'message': 'Persona actualizada exitosamente',
            'person': person.to_dict()
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al actualizar persona',
            'details': str(e)
        }), 500


@persons_bp.route('/<person_id>', methods=['DELETE'])
@jwt_required()
def delete_person(person_id):
    """
    Eliminar/desactivar una persona
    
    Path Params:
        person_id: ID de la persona
    
    Returns:
        JSON con mensaje de confirmación
    """
    try:
        user_id = get_jwt_identity()
        user = WebUser.query.get(user_id)
        
        # Verificar permisos
        if not user.can('users.delete'):
            return jsonify({'error': 'Acceso denegado'}), 403
        
        person = Person.query.get(person_id)
        
        if not person:
            return jsonify({'error': 'Persona no encontrada'}), 404
        
        # En lugar de eliminar, desactivar
        person.status = 'inactive'
        db.session.commit()
        
        return jsonify({
            'message': 'Persona desactivada exitosamente'
        }), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Error al desactivar persona',
            'details': str(e)
        }), 500


@persons_bp.route('/stats', methods=['GET'])
@jwt_required()
def get_person_stats():
    """
    Obtener estadísticas de personas
    
    Returns:
        JSON con estadísticas
    """
    try:
        total = Person.query.count()
        active = Person.query.filter(Person.status == 'active').count()
        
        # Contar por área
        areas = db.session.query(
            Person.area,
            db.func.count(Person.person_id)
        ).group_by(Person.area).all()
        
        # Contar por posición
        positions = db.session.query(
            Person.position,
            db.func.count(Person.person_id)
        ).group_by(Person.position).all()
        
        return jsonify({
            'total_persons': total,
            'active_persons': active,
            'persons_by_area': [{'area': a[0] or 'Sin área', 'count': a[1]} for a in areas],
            'persons_by_position': [{'position': p[0] or 'Sin cargo', 'count': p[1]} for p in positions]
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener estadísticas',
            'details': str(e)
        }), 500
