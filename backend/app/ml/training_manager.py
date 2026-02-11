"""
Training Manager - Gestión de reentrenamiento de modelos ML
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from pathlib import Path
from sqlalchemy import text
from app.extensions import db
from app.models.ml_models import MLModel, MLDataset, MLTrainingJob


class TrainingManager:
    """Gestiona extracción de datos, entrenamiento y versionado de modelos"""
    
    def __init__(self):
        self.models_dir = Path(__file__).parent / 'models'
        self.datasets_dir = Path(__file__).parent / 'datasets'
        self.datasets_dir.mkdir(exist_ok=True)
    
    
    def get_available_data_stats(self):
        """Obtiene estadísticas de datos disponibles para reentrenamiento"""
        stats = {}
        
        # Tareas completadas con horas reales
        query_tasks = text("""
            SELECT 
                COUNT(*) as total,
                COUNT(CASE WHEN actual_hours IS NOT NULL THEN 1 END) as with_actual_hours,
                MIN(created_at) as oldest_date,
                MAX(created_at) as newest_date
            FROM web_tasks
        """)
        result = db.session.execute(query_tasks).fetchone()
        
        stats['tasks'] = {
            'total': result[0],
            'with_actual_hours': result[1],
            'oldest_date': result[2].isoformat() if result[2] else None,
            'newest_date': result[3].isoformat() if result[3] else None,
        }
        
        # Usuarios
        query_users = text("SELECT COUNT(*) FROM web_users WHERE status='activo'")
        stats['users'] = db.session.execute(query_users).scalar()
        
        # Dependencias
        query_deps = text("SELECT COUNT(*) FROM web_task_dependencies")
        stats['dependencies'] = db.session.execute(query_deps).scalar()
        
        # Predicciones guardadas
        query_preds = text("SELECT COUNT(*) FROM ml_predictions")
        stats['predictions'] = db.session.execute(query_preds).scalar()
        
        return stats
    
    
    def extract_dataset_for_model(self, model_type, date_from=None, date_to=None):
        """
        Extrae dataset de web_tasks para un tipo de modelo específico
        
        Args:
            model_type: 'risk', 'duration', 'recommendation', 'simulation'
            date_from: Fecha inicio (opcional)
            date_to: Fecha fin (opcional)
            
        Returns:
            pandas.DataFrame con el dataset
        """
        print(f" Extrayendo dataset para modelo '{model_type}'...")
        
        if model_type == 'risk':
            return self._extract_risk_dataset(date_from, date_to)
        elif model_type == 'duration':
            return self._extract_duration_dataset(date_from, date_to)
        elif model_type == 'recommendation':
            return self._extract_recommendation_dataset(date_from, date_to)
        elif model_type == 'simulation':
            return self._extract_simulation_dataset(date_from, date_to)
        else:
            raise ValueError(f"Tipo de modelo no soportado: {model_type}")
    
    
    def _extract_risk_dataset(self, date_from, date_to):
        """Dataset para clasificador de riesgo"""
        query = text("""
            SELECT 
                wt.id,
                wt.title,
                wt.area,
                wt.priority,
                wt.complexity_score,
                wt.estimated_hours,
                wt.actual_hours,
                wt.status,
                DATEDIFF(wt.deadline, wt.start_date) as days_allocated,
                DATEDIFF(wt.completed_at, wt.start_date) as days_taken,
                wu.experience_years,
                wu.performance_index,
                wu.current_load,
                -- Target: riesgo alto si se retrasó >20% o status=retrasada
                CASE 
                    WHEN wt.status = 'retrasada' THEN 1
                    WHEN wt.actual_hours > wt.estimated_hours * 1.2 THEN 1
                    ELSE 0
                END as high_risk
            FROM web_tasks wt
            LEFT JOIN web_users wu ON wt.assigned_to = wu.email
            WHERE wt.actual_hours IS NOT NULL
                AND wt.estimated_hours > 0
        """)
        
        if date_from:
            query = text(str(query) + f" AND wt.created_at >= '{date_from}'")
        if date_to:
            query = text(str(query) + f" AND wt.created_at <= '{date_to}'")
        
        df = pd.read_sql(query, db.session.bind)
        print(f"    {len(df)} registros extraídos para Risk Model")
        return df
    
    
    def _extract_duration_dataset(self, date_from, date_to):
        """Dataset para predictor de duración"""
        query = text("""
            SELECT 
                wt.id,
                wt.title,
                wt.area,
                wt.priority,
                wt.complexity_score,
                wt.estimated_hours,
                wt.actual_hours,  -- Target
                wu.experience_years,
                wu.performance_index,
                wu.tasks_completed,
                wu.current_load,
                (SELECT COUNT(*) FROM web_task_dependencies WHERE successor_task_id = wt.id) as dependencies_count
            FROM web_tasks wt
            LEFT JOIN web_users wu ON wt.assigned_to = wu.email
            WHERE wt.actual_hours IS NOT NULL
                AND wt.actual_hours > 0
                AND wt.status = 'completada'
        """)
        
        if date_from:
            query = text(str(query) + f" AND wt.created_at >= '{date_from}'")
        if date_to:
            query = text(str(query) + f" AND wt.created_at <= '{date_to}'")
        
        df = pd.read_sql(query, db.session.bind)
        print(f"    {len(df)} registros extraídos para Duration Model")
        return df
    
    
    def _extract_recommendation_dataset(self, date_from, date_to):
        """Dataset para recomendador persona-tarea"""
        query = text("""
            SELECT 
                wt.id as task_id,
                wt.area as task_area,
                wt.priority,
                wt.complexity_score,
                wt.estimated_hours,
                wu.email as assigned_person,
                wu.area as person_area,
                wu.experience_years,
                wu.skills,
                wu.performance_index,
                -- Success: completada a tiempo
                CASE 
                    WHEN wt.status = 'completada' AND wt.actual_hours <= wt.estimated_hours * 1.1 THEN 1
                    ELSE 0
                END as success
            FROM web_tasks wt
            INNER JOIN web_users wu ON wt.assigned_to = wu.email
            WHERE wt.actual_hours IS NOT NULL
                AND wt.status IN ('completada', 'retrasada')
        """)
        
        if date_from:
            query = text(str(query) + f" AND wt.created_at >= '{date_from}'")
        if date_to:
            query = text(str(query) + f" AND wt.created_at <= '{date_to}'")
        
        df = pd.read_sql(query, db.session.bind)
        print(f"    {len(df)} registros extraídos para Recommendation Model")
        return df
    
    
    def _extract_simulation_dataset(self, date_from, date_to):
        """Dataset para simulación de procesos (bottleneck)"""
        query = text("""
            SELECT 
                wt.id,
                wt.project_id,
                wt.title,
                wt.area,
                wt.priority,
                wt.complexity_score,
                wt.estimated_hours,
                wt.actual_hours,
                wt.status,
                wt.start_date,
                wt.completed_at,
                -- Delay ratio
                CASE 
                    WHEN wt.estimated_hours > 0 THEN wt.actual_hours / wt.estimated_hours
                    ELSE 0
                END as delay_ratio,
                -- Bottleneck si delay > 1.2
                CASE 
                    WHEN wt.actual_hours > wt.estimated_hours * 1.2 THEN 1
                    ELSE 0
                END as is_bottleneck
            FROM web_tasks wt
            WHERE wt.actual_hours IS NOT NULL
                AND wt.estimated_hours > 0
        """)
        
        if date_from:
            query = text(str(query) + f" AND wt.created_at >= '{date_from}'")
        if date_to:
            query = text(str(query) + f" AND wt.created_at <= '{date_to}'")
        
        df = pd.read_sql(query, db.session.bind)
        print(f"    {len(df)} registros extraídos para Simulation/Bottleneck Model")
        return df
    
    
    def save_dataset(self, df, model_type, uploaded_by=None):
        """
        Guarda dataset en disco y registra en bd
        
        Returns:
            MLDataset object
        """
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        filename = f"{model_type}_dataset_{timestamp}.csv"
        filepath = self.datasets_dir / filename
        
        # Guardar CSV
        df.to_csv(filepath, index=False)
        file_size = filepath.stat().st_size
        
        # Registrar en BD
        dataset = MLDataset(
            filename=filename,
            original_name=filename,
            file_path=str(filepath),
            file_type='csv',
            file_size_bytes=file_size,
            record_count=len(df),
            columns_count=len(df.columns),
            columns_info={'columns': list(df.columns), 'dtypes': df.dtypes.astype(str).to_dict()},
            data_preview=df.head(5).to_dict('records'),
            status='processed',
            uploaded_by=uploaded_by,
            processed_at=datetime.now()
        )
        
        db.session.add(dataset)
        db.session.commit()
        
        print(f" Dataset guardado: {filename} ({file_size} bytes)")
        return dataset
    
    
    def compare_models(self, old_metrics, new_metrics):
        """
        Compara métricas de dos modelos
        
        Returns:
            dict con comparación y decisión
        """
        # Métricas principales a comparar
        comparison = {
            'old': old_metrics,
            'new': new_metrics,
            'improvements': {},
            'should_replace': False,
            'reason': ''
        }
        
        # Comparar accuracy/precision
        old_acc = old_metrics.get('accuracy') or old_metrics.get('precision', 0)
        new_acc = new_metrics.get('accuracy') or new_metrics.get('precision', 0)
        
        improvement = ((new_acc - old_acc) / old_acc * 100) if old_acc > 0 else 0
        
        comparison['improvements']['accuracy'] = {
            'old': old_acc,
            'new': new_acc,
            'delta': new_acc - old_acc,
            'delta_percent': improvement
        }
        
        # Decisión: reemplazar si mejora >2%
        MIN_IMPROVEMENT = 2.0  # 2%
        
        if improvement >= MIN_IMPROVEMENT:
            comparison['should_replace'] = True
            comparison['reason'] = f"Mejora significativa: +{improvement:.2f}%"
        elif improvement > 0:
            comparison['should_replace'] = False
            comparison['reason'] = f"Mejora insuficiente: +{improvement:.2f}% (mínimo {MIN_IMPROVEMENT}%)"
        else:
            comparison['should_replace'] = False
            comparison['reason'] = f"Modelo nuevo es peor: {improvement:.2f}%"
        
        return comparison
    
    
    def activate_model(self, job_id, replace_current=True):
        """
        Activa un modelo entrenado
        
        Args:
            job_id: ID del training job
            replace_current: Si True, desactiva el modelo anterior
        """
        job = MLTrainingJob.query.get(job_id)
        if not job or job.status != 'completed':
            raise ValueError("Job no encontrado o no completado")
        
        if not job.output_model_path:
            raise ValueError("No hay modelo entrenado")
        
        # Obtener modelo original
        model = MLModel.query.get(job.model_id)
        if not model:
            raise ValueError("Modelo no encontrado")
        
        # Backup del modelo anterior
        if replace_current and model.model_path:
            old_path = Path(model.model_path)
            if old_path.exists():
                backup_name = old_path.stem + '_backup_' + datetime.now().strftime('%Y%m%d_%H%M%S') + old_path.suffix
                backup_path = old_path.parent / backup_name
                old_path.rename(backup_path)
                print(f" Backup creado: {backup_path}")
        
        # Activar nuevo modelo
        model.model_path = job.output_model_path
        model.status = 'activo'
        model.last_trained = job.completed_at
        model.samples_count = job.config.get('samples_count', 0) if job.config else 0
        
        # Actualizar métricas
        if job.metrics:
            model.precision = job.metrics.get('accuracy') or job.metrics.get('precision')
            model.recall_score = job.metrics.get('recall')
            model.f1_score = job.metrics.get('f1_score')
            model.mae = job.metrics.get('mae')
            model.rmse = job.metrics.get('rmse')
            model.r2_score = job.metrics.get('r2_score')
            model.metrics = job.metrics
        
        # Incrementar versión
        if model.version:
            try:
                version_num = float(model.version.replace('v', ''))
                model.version = f"v{version_num + 0.1:.1f}"
            except:
                model.version = 'v2.0'
        
        db.session.commit()
        print(f" Modelo activado: {model.name} {model.version}")
        
        return model


# Instancia global
training_manager = TrainingManager()
