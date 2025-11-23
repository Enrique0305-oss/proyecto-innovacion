"""
Modelos de base de datos
Exporta todos los modelos para facilitar su importación
"""
# Modelos nuevos para sb_production
from app.models.role import Role
from app.models.area import Area
from app.models.web_user import WebUser
from app.models.web_task import WebTask
from app.models.ml_models import MLModel, MLPrediction

# Modelos existentes
from app.models.user import User
from app.models.task import Task, TaskDependency, Assignee
from app.models.person import Person

__all__ = [
    # Nuevos modelos web
    'Role',
    'Area', 
    'WebUser',
    'WebTask',
    'MLModel',
    'MLPrediction',
    # Modelos existentes
    'User',
    'Task',
    'TaskDependency',
    'Assignee',
    'Person'
]
