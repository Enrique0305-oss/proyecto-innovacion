"""
Sistema de Reentrenamiento de Modelos ML
Permite entrenar/reentrenar modelos desde la interfaz de Configuración IA
"""
import os
import json
import joblib
import pandas as pd
import numpy as np
from datetime import datetime
from flask import current_app
from sqlalchemy import text
from app.extensions import db


class ModelTrainer:
    """Clase para gestionar el entrenamiento de modelos"""
    
    def __init__(self):
        self.models_path = os.path.join(
            os.path.dirname(os.path.dirname(os.path.dirname(__file__))),
            'ml', 'models'
        )
        self.risk_model_path = os.path.join(self.models_path, 'risk')
        self.training_script_path = os.path.join(self.models_path, 'training')
    
    def get_training_data_from_db(self, table_name='task', limit=None):
        """
        Extraer datos de entrenamiento desde la base de datos
        
        Args:
            table_name: Nombre de la tabla (task por defecto)
            limit: Límite de registros (None = todos)
        
        Returns:
            pandas.DataFrame con los datos
        """
        try:
            query = f"SELECT * FROM {table_name}"
            if limit:
                query += f" LIMIT {limit}"
            
            df = pd.read_sql(query, db.engine)
            print(f"✓ Datos extraídos: {len(df)} registros de '{table_name}'")
            return df
            
        except Exception as e:
            print(f"✗ Error al extraer datos: {str(e)}")
            raise
    
    def train_risk_model(self, data=None, use_optuna=True, n_trials=50):
        """
        Entrenar modelo de clasificación de riesgo con CatBoost
        
        Args:
            data: DataFrame con datos (si None, extrae de BD)
            use_optuna: Si usar optimización de hiperparámetros
            n_trials: Número de trials para Optuna
        
        Returns:
            dict con resultados del entrenamiento
        """
        try:
            # Importar dependencias necesarias
            from catboost import CatBoostClassifier, Pool
            from sklearn.model_selection import train_test_split
            from sklearn.preprocessing import StandardScaler, LabelEncoder
            from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
            import optuna
            
            print("\n" + "="*70)
            print(" ENTRENAMIENTO DE MODELO DE RIESGO - CATBOOST MULTICLASS")
            print("="*70)
            
            # 1. Cargar datos
            if data is None:
                print("\n Extrayendo datos de la base de datos...")
                data = self.get_training_data_from_db('task')
            
            # 2. Preparar features y target
            print("\n🔧 Preparando features...")
            X, y, feature_names, preprocessor = self._prepare_risk_features(data)
            
            # 3. Split train/test
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=0.2, random_state=42, stratify=y
            )
            
            print(f"   Train: {len(X_train)} | Test: {len(X_test)}")
            print(f"   Clases: {np.unique(y)}")
            
            # 4. Optimización con Optuna (opcional)
            best_params = {}
            if use_optuna:
                print(f"\n Optimizando hiperparámetros con Optuna ({n_trials} trials)...")
                best_params = self._optimize_catboost(X_train, y_train, n_trials)
                print(f"   Mejores parámetros encontrados: {best_params}")
            
            # 5. Entrenar modelo final
            print("\n Entrenando modelo final...")
            model = CatBoostClassifier(
                **best_params,
                random_state=42,
                verbose=False
            )
            
            model.fit(X_train, y_train, eval_set=(X_test, y_test), verbose=100)
            
            # 6. Evaluar modelo
            print("\n Evaluando modelo...")
            y_pred = model.predict(X_test)
            
            accuracy = accuracy_score(y_test, y_pred)
            report = classification_report(y_test, y_pred, output_dict=True)
            conf_matrix = confusion_matrix(y_test, y_pred)
            
            print(f"   Accuracy: {accuracy:.4f}")
            
            # 7. Guardar modelo y artefactos
            print("\n Guardando modelo y artefactos...")
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            # Crear carpeta si no existe
            os.makedirs(self.risk_model_path, exist_ok=True)
            os.makedirs(os.path.join(self.risk_model_path, 'metrics'), exist_ok=True)
            
            # Guardar modelo
            model_file = os.path.join(self.risk_model_path, 'model_catboost_multiclass.pkl')
            joblib.dump(model, model_file)
            print(f"   ✓ Modelo guardado: {model_file}")
            
            # Guardar preprocessor
            preprocessor_file = os.path.join(self.risk_model_path, 'preprocessor.pkl')
            joblib.dump(preprocessor, preprocessor_file)
            print(f"   ✓ Preprocessor guardado: {preprocessor_file}")
            
            # Guardar configuración
            config = {
                'model_type': 'CatBoostClassifier',
                'features': feature_names,
                'n_features': len(feature_names),
                'classes': list(np.unique(y)),
                'n_classes': len(np.unique(y)),
                'training_date': timestamp,
                'accuracy': float(accuracy),
                'best_params': best_params,
                'train_size': len(X_train),
                'test_size': len(X_test)
            }
            
            config_file = os.path.join(self.risk_model_path, 'model_config.json')
            with open(config_file, 'w', encoding='utf-8') as f:
                json.dump(config, f, indent=2)
            print(f"   ✓ Configuración guardada: {config_file}")
            
            # Guardar métricas
            metrics_file = os.path.join(self.risk_model_path, 'metrics', 'classification_report.csv')
            pd.DataFrame(report).transpose().to_csv(metrics_file)
            print(f"   ✓ Métricas guardadas: {metrics_file}")
            
            # Guardar importancia de features
            feature_importance = pd.DataFrame({
                'feature': feature_names,
                'importance': model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            importance_file = os.path.join(self.risk_model_path, 'metrics', 'feature_importance.csv')
            feature_importance.to_csv(importance_file, index=False)
            print(f"   ✓ Feature importance guardada: {importance_file}")
            
            # 8. Guardar estudio de Optuna
            if use_optuna and hasattr(self, '_last_study'):
                study_file = os.path.join(self.risk_model_path, 'optuna_study.json')
                study_data = {
                    'best_params': best_params,
                    'best_value': self._last_study.best_value,
                    'n_trials': len(self._last_study.trials),
                    'timestamp': timestamp
                }
                with open(study_file, 'w') as f:
                    json.dump(study_data, f, indent=2)
                print(f"   ✓ Estudio Optuna guardado: {study_file}")
            
            print("\n" + "="*70)
            print(" ENTRENAMIENTO COMPLETADO EXITOSAMENTE")
            print("="*70 + "\n")
            
            return {
                'success': True,
                'accuracy': float(accuracy),
                'model_path': model_file,
                'config_path': config_file,
                'timestamp': timestamp,
                'metrics': {
                    'accuracy': float(accuracy),
                    'classification_report': report,
                    'confusion_matrix': conf_matrix.tolist()
                }
            }
            
        except Exception as e:
            print(f"\n✗ Error en entrenamiento: {str(e)}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'error': str(e)
            }
    
    def _prepare_risk_features(self, data):
        """
        Preparar features para el modelo de riesgo
        
        Returns:
            X, y, feature_names, preprocessor
        """
        from sklearn.preprocessing import StandardScaler, LabelEncoder
        
        # Definir features que usarás (ajusta según tus columnas)
        # IMPORTANTE: Usa las mismas 32 features de tu modelo original
        categorical_features = [
            'complexity_level', 'priority', 'area_name', 'task_type',
            'status', 'assigned_to'
        ]
        
        numerical_features = [
            'duration_est', 'assignees_count', 'dependencies_count',
            'completion_percentage', 'days_elapsed'
        ]
        
        # Target: nivel de riesgo (debes tener esta columna en tu tabla)
        # Si no existe, puedes calcularla con reglas heurísticas
        if 'risk_level' not in data.columns:
            data['risk_level'] = self._calculate_risk_heuristic(data)
        
        # Eliminar filas con valores nulos en target
        data = data.dropna(subset=['risk_level'])
        
        # Preparar features categóricas
        label_encoders = {}
        for col in categorical_features:
            if col in data.columns:
                le = LabelEncoder()
                data[f'{col}_encoded'] = le.fit_transform(data[col].fillna('unknown'))
                label_encoders[col] = le
        
        # Seleccionar features finales
        feature_columns = [f'{col}_encoded' for col in categorical_features if col in data.columns]
        feature_columns += [col for col in numerical_features if col in data.columns]
        
        # Rellenar NaN en features numéricas
        for col in numerical_features:
            if col in data.columns:
                data[col] = data[col].fillna(0)
        
        X = data[feature_columns].values
        y = data['risk_level'].values
        
        # Normalizar features numéricas
        scaler = StandardScaler()
        X = scaler.fit_transform(X)
        
        # Guardar preprocessor
        preprocessor = {
            'scaler': scaler,
            'label_encoders': label_encoders,
            'feature_columns': feature_columns,
            'categorical_features': categorical_features,
            'numerical_features': numerical_features
        }
        
        return X, y, feature_columns, preprocessor
    
    def _calculate_risk_heuristic(self, data):
        """
        Calcular risk_level con reglas heurísticas si no existe
        """
        risk_levels = []
        for _, row in data.iterrows():
            score = 0
            
            # Complejidad
            if 'complexity_level' in row and 'alta' in str(row['complexity_level']).lower():
                score += 3
            
            # Prioridad
            if 'priority' in row and ('alta' in str(row['priority']).lower() or 'crítica' in str(row['priority']).lower()):
                score += 2
            
            # Duración
            if 'duration_est' in row and row['duration_est'] > 30:
                score += 2
            
            # Determinar nivel
            if score >= 5:
                risk_levels.append('alto')
            elif score >= 3:
                risk_levels.append('medio')
            else:
                risk_levels.append('bajo')
        
        return risk_levels
    
    def _optimize_catboost(self, X_train, y_train, n_trials=50):
        """
        Optimizar hiperparámetros con Optuna
        """
        import optuna
        from catboost import CatBoostClassifier
        from sklearn.model_selection import cross_val_score
        
        def objective(trial):
            params = {
                'iterations': trial.suggest_int('iterations', 100, 1000),
                'depth': trial.suggest_int('depth', 4, 10),
                'learning_rate': trial.suggest_float('learning_rate', 0.01, 0.3),
                'l2_leaf_reg': trial.suggest_float('l2_leaf_reg', 1, 10),
                'border_count': trial.suggest_int('border_count', 32, 255),
                'random_state': 42,
                'verbose': False
            }
            
            model = CatBoostClassifier(**params)
            score = cross_val_score(model, X_train, y_train, cv=3, scoring='accuracy', n_jobs=-1)
            return score.mean()
        
        study = optuna.create_study(direction='maximize')
        study.optimize(objective, n_trials=n_trials, show_progress_bar=True)
        
        self._last_study = study
        return study.best_params
    
    def get_model_info(self):
        """
        Obtener información del modelo actual
        """
        config_file = os.path.join(self.risk_model_path, 'model_config.json')
        
        if not os.path.exists(config_file):
            return {
                'status': 'no_model',
                'message': 'No hay modelo entrenado'
            }
        
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            return {
                'status': 'ready',
                'model_type': config.get('model_type'),
                'accuracy': config.get('accuracy'),
                'training_date': config.get('training_date'),
                'n_features': config.get('n_features'),
                'classes': config.get('classes')
            }
        except:
            return {
                'status': 'error',
                'message': 'Error al leer configuración del modelo'
            }
