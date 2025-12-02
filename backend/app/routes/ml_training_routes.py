"""
Rutas para Entrenamiento y Configuración de Modelos ML
Endpoints para la interfaz de Configuración IA
"""
from flask import Blueprint, request, jsonify, send_file
from flask_jwt_extended import jwt_required, get_jwt_identity
import os
import json
from app.ml.model_trainer import ModelTrainer
from app.models.web_user import WebUser
from app.models.role import Role

# Crear Blueprint
ml_training_bp = Blueprint('ml_training', __name__)

# Instancia del trainer
trainer = ModelTrainer()


def require_admin():
    """Decorator para verificar que el usuario es super_admin"""
    current_user_email = get_jwt_identity()
    user = WebUser.query.filter_by(email=current_user_email).first()
    
    if not user:
        return jsonify({'error': 'Usuario no encontrado'}), 404
    
    role = Role.query.get(user.role_id)
    if not role or role.name != 'super_admin':
        return jsonify({
            'error': 'Acceso denegado',
            'message': 'Solo Super Administradores pueden acceder a esta función'
        }), 403
    
    return None


@ml_training_bp.route('/model/info', methods=['GET'])
@jwt_required()
def get_model_info():
    """
    Obtener información del modelo actual de riesgo
    
    GET /api/ml/model/info
    
    Returns:
        JSON con información del modelo (fecha, accuracy, features, etc.)
    """
    try:
        info = trainer.get_model_info()
        return jsonify(info), 200
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener información del modelo',
            'details': str(e)
        }), 500


@ml_training_bp.route('/model/train', methods=['POST'])
@jwt_required()
def train_model():
    """
    Entrenar/Reentrenar el modelo de riesgo
    
    POST /api/ml/model/train
    
    Body JSON (opcional):
        - use_optuna: bool (default: true) - Optimizar hiperparámetros
        - n_trials: int (default: 50) - Número de trials de Optuna
        - data_limit: int (default: null) - Límite de datos (null = todos)
    
    Returns:
        JSON con resultados del entrenamiento
    """
    # Verificar permisos de admin
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    try:
        data = request.get_json() or {}
        
        use_optuna = data.get('use_optuna', True)
        n_trials = data.get('n_trials', 50)
        data_limit = data.get('data_limit', None)
        
        print(f"\n🚀 Iniciando entrenamiento del modelo...")
        print(f"   - Optimización Optuna: {use_optuna}")
        print(f"   - Trials: {n_trials}")
        print(f"   - Límite de datos: {data_limit or 'Todos'}")
        
        # Entrenar modelo
        result = trainer.train_risk_model(
            data=None,
            use_optuna=use_optuna,
            n_trials=n_trials
        )
        
        if result['success']:
            return jsonify({
                'success': True,
                'message': 'Modelo entrenado exitosamente',
                'accuracy': result['accuracy'],
                'timestamp': result['timestamp'],
                'metrics': result['metrics']
            }), 200
        else:
            return jsonify({
                'success': False,
                'error': result['error']
            }), 500
            
    except Exception as e:
        import traceback
        return jsonify({
            'error': 'Error al entrenar modelo',
            'details': str(e),
            'trace': traceback.format_exc()
        }), 500


@ml_training_bp.route('/model/metrics', methods=['GET'])
@jwt_required()
def get_model_metrics():
    """
    Obtener métricas del modelo actual
    
    GET /api/ml/model/metrics
    
    Returns:
        JSON con métricas detalladas (classification_report, feature_importance)
    """
    try:
        metrics_path = os.path.join(trainer.risk_model_path, 'metrics')
        
        if not os.path.exists(metrics_path):
            return jsonify({
                'error': 'No hay métricas disponibles',
                'message': 'Entrena el modelo primero'
            }), 404
        
        # Leer classification report
        report_file = os.path.join(metrics_path, 'classification_report.csv')
        importance_file = os.path.join(metrics_path, 'feature_importance.csv')
        
        metrics = {}
        
        if os.path.exists(report_file):
            import pandas as pd
            df_report = pd.read_csv(report_file)
            metrics['classification_report'] = df_report.to_dict('records')
        
        if os.path.exists(importance_file):
            import pandas as pd
            df_importance = pd.read_csv(importance_file)
            # Top 20 features más importantes
            metrics['feature_importance'] = df_importance.head(20).to_dict('records')
        
        return jsonify(metrics), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener métricas',
            'details': str(e)
        }), 500


@ml_training_bp.route('/model/metrics/image/<metric_type>', methods=['GET'])
@jwt_required()
def get_metric_image(metric_type):
    """
    Obtener imágenes de métricas (confusion_matrix, feature_importance)
    
    GET /api/ml/model/metrics/image/<metric_type>
    
    Params:
        - metric_type: 'confusion_matrix' o 'feature_importance'
    
    Returns:
        Imagen PNG
    """
    try:
        metrics_path = os.path.join(trainer.risk_model_path, 'metrics')
        
        valid_types = ['confusion_matrix', 'feature_importance']
        if metric_type not in valid_types:
            return jsonify({
                'error': 'Tipo de métrica inválido',
                'valid_types': valid_types
            }), 400
        
        image_file = os.path.join(metrics_path, f'{metric_type}.png')
        
        if not os.path.exists(image_file):
            return jsonify({
                'error': 'Imagen no encontrada',
                'message': f'No existe {metric_type}.png'
            }), 404
        
        return send_file(image_file, mimetype='image/png')
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener imagen',
            'details': str(e)
        }), 500


@ml_training_bp.route('/model/config', methods=['GET'])
@jwt_required()
def get_model_config():
    """
    Obtener configuración completa del modelo
    
    GET /api/ml/model/config
    
    Returns:
        JSON con model_config.json completo
    """
    try:
        config_file = os.path.join(trainer.risk_model_path, 'model_config.json')
        
        if not os.path.exists(config_file):
            return jsonify({
                'error': 'Configuración no encontrada',
                'message': 'El modelo aún no ha sido entrenado'
            }), 404
        
        with open(config_file, 'r', encoding='utf-8') as f:
            config = json.load(f)
        
        return jsonify(config), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al leer configuración',
            'details': str(e)
        }), 500


@ml_training_bp.route('/training/status', methods=['GET'])
@jwt_required()
def get_training_status():
    """
    Verificar el estado del sistema de entrenamiento
    
    GET /api/ml/training/status
    
    Returns:
        JSON con estado del sistema
    """
    try:
        # Verificar dependencias
        dependencies = {
            'catboost': False,
            'optuna': False,
            'sklearn': False,
            'pandas': False
        }
        
        try:
            import catboost
            dependencies['catboost'] = True
        except:
            pass
        
        try:
            import optuna
            dependencies['optuna'] = True
        except:
            pass
        
        try:
            import sklearn
            dependencies['sklearn'] = True
        except:
            pass
        
        try:
            import pandas
            dependencies['pandas'] = True
        except:
            pass
        
        all_ready = all(dependencies.values())
        
        # Verificar si existe modelo
        model_info = trainer.get_model_info()
        
        return jsonify({
            'status': 'ready' if all_ready else 'dependencies_missing',
            'dependencies': dependencies,
            'model': model_info,
            'paths': {
                'models': trainer.models_path,
                'risk_model': trainer.risk_model_path
            }
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al verificar estado',
            'details': str(e)
        }), 500


@ml_training_bp.route('/data/preview', methods=['GET'])
@jwt_required()
def preview_training_data():
    """
    Vista previa de datos de entrenamiento disponibles
    
    GET /api/ml/data/preview?limit=10
    
    Query params:
        - limit: int (default: 10) - Número de registros a mostrar
    
    Returns:
        JSON con muestra de datos y estadísticas
    """
    # Verificar permisos de admin
    admin_check = require_admin()
    if admin_check:
        return admin_check
    
    try:
        limit = request.args.get('limit', 10, type=int)
        
        # Extraer datos de la BD
        data = trainer.get_training_data_from_db('task', limit=limit)
        
        # Estadísticas básicas
        stats = {
            'total_records': len(data),
            'columns': list(data.columns),
            'null_counts': data.isnull().sum().to_dict(),
            'data_types': data.dtypes.astype(str).to_dict()
        }
        
        # Muestra de datos (primeros registros)
        sample = data.head(limit).to_dict('records')
        
        return jsonify({
            'statistics': stats,
            'sample': sample
        }), 200
        
    except Exception as e:
        return jsonify({
            'error': 'Error al obtener datos',
            'details': str(e)
        }), 500
