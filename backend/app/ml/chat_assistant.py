"""
Asistente de Chat Inteligente
Procesa mensajes en lenguaje natural y ejecuta predicciones ML
"""
import re
from typing import Dict, Any, Optional
from app.ml.risk_model import predict_risk
from app.ml.duration_model import predict_duration
from app.ml.recommender_model import recommend_person
from app.ml.attrition_model import predict_attrition
from app.extensions import db
from app.models.web_user import WebUser
from app.models.web_task import WebTask


class ChatAssistant:
    """Asistente conversacional que usa los modelos ML del sistema"""
    
    def __init__(self):
        self.intents = {
            'riesgo': ['riesgo', 'risk', 'peligro', 'predic'],
            'duracion': ['duración', 'tiempo', 'cuánto', 'demora', 'tarda'],
            'recomendar': ['recomendar', 'recomendación', 'recomend', 'quién', 'quien', 'mejor persona', 'asignar', 'para'],
            'desempeño': ['desempeño', 'desempeño', 'performance', 'rendimiento', 'análisis', 'analiza', 'colaborador', 'usuario'],
            'renuncia': ['renuncia', 'attrition', 'resignación', 'dejar'],
            'estadisticas': ['estadísticas', 'estadisticas', 'stats', 'métricas', 'resumen', 'dashboard'],
            'ayuda': ['ayuda', 'help', 'qué puedes hacer', 'comandos']
        }
    
    def detect_intent(self, message: str) -> str:
        """Detecta la intención del mensaje del usuario"""
        message = message.lower()
        
        for intent, keywords in self.intents.items():
            if any(keyword in message for keyword in keywords):
                return intent
        
        return 'unknown'
    
    def extract_complexity(self, message: str) -> str:
        """Extrae la complejidad de la tarea del mensaje"""
        message = message.lower()
        if 'baja' in message or 'fácil' in message or 'simple' in message:
            return 'Baja'
        elif 'alta' in message or 'difícil' in message or 'compleja' in message or 'complicada' in message:
            return 'Alta'
        else:
            return 'Media'
    
    def extract_priority(self, message: str) -> str:
        """Extrae la prioridad del mensaje"""
        message = message.lower()
        if 'crítica' in message or 'urgente' in message:
            return 'Crítica'
        elif 'alta' in message and 'prioridad' in message:
            return 'Alta'
        elif 'baja' in message and 'prioridad' in message:
            return 'Baja'
        else:
            return 'Media'
    
    def extract_area(self, message: str) -> str:
        """Extrae el área del mensaje"""
        message = message.lower()
        areas = {
            'ti': 'TI',
            'tecnología': 'Tecnología',
            'marketing': 'Marketing',
            'operaciones': 'Operaciones',
            'rrhh': 'RRHH',
            'ventas': 'Ventas',
            'comercial': 'Comercial',
            'finanzas': 'Finanzas'
        }
        
        for key, value in areas.items():
            if key in message:
                return value
        
        return 'TI'  # Default
    
    def extract_number(self, message: str) -> Optional[int]:
        """Extrae un número del mensaje"""
        numbers = re.findall(r'\d+', message)
        return int(numbers[0]) if numbers else None
    
    def handle_risk_prediction(self, message: str) -> str:
        """Maneja predicción de riesgo"""
        try:
            task_data = {
                'complexity_level': self.extract_complexity(message),
                'priority': self.extract_priority(message),
                'area': self.extract_area(message),
                'task_type': 'Desarrollo',  # Default
                'duration_est': self.extract_number(message) or 10,
                'assignees_count': 1,
                'dependencies': 0
            }
            
            result = predict_risk(task_data)
            
            risk_emoji = {
                'bajo_riesgo': '✅',
                'alto_riesgo': '⚠️'
            }
            
            emoji = risk_emoji.get(result['risk_level'].lower(), '📊')
            
            response = f"{emoji} **Predicción de Riesgo**\n\n"
            response += f"Nivel de riesgo: **{result['risk_level'].upper()}**\n"
            response += f"Confianza: {result['probability']*100:.1f}%\n\n"
            
            if result.get('risk_factors'):
                response += "**Factores identificados:**\n"
                for factor in result['risk_factors'][:3]:
                    response += f"• {factor}\n"
            
            if result.get('recommendations'):
                response += f"\n💡 **Recomendación:** {result['recommendations'][0]}"
            
            return response
            
        except Exception as e:
            return f"❌ Error al predecir riesgo: {str(e)}"
    
    def handle_duration_prediction(self, message: str) -> str:
        """Maneja predicción de duración"""
        try:
            days = self.extract_number(message) or 10
            
            task_data = {
                'complexity_level': self.extract_complexity(message),
                'duration_est_days': days
            }
            
            result = predict_duration(task_data)
            
            predicted = result.get('duration_days', result.get('duration', days))
            diff = predicted - days
            
            response = f"⏱️ **Predicción de Duración**\n\n"
            response += f"Estimación inicial: {days} días\n"
            response += f"Predicción IA: **{predicted:.1f} días**\n"
            response += f"Diferencia: {'+' if diff > 0 else ''}{diff:.1f} días ({(diff/days*100):.1f}%)\n\n"
            
            if result.get('confidence_interval'):
                ci = result['confidence_interval']
                response += f"📊 Rango esperado: {ci.get('min', predicted*0.8):.1f} - {ci.get('max', predicted*1.2):.1f} días"
            
            return response
            
        except Exception as e:
            return f"❌ Error al predecir duración: {str(e)}"
    
    def handle_recommendation(self, message: str) -> str:
        """Maneja recomendación de persona"""
        try:
            task_data = {
                'complexity_level': self.extract_complexity(message),
                'priority': self.extract_priority(message),
                'area': self.extract_area(message),
                'task_type': 'Desarrollo',
                'duration_est': self.extract_number(message) or 10
            }
            
            result = recommend_person(task_data)
            
            if not result.get('recommendations'):
                return "📋 No encontré personas disponibles para esta tarea."
            
            top_person = result['recommendations'][0]
            
            response = f"👤 **Recomendación de Asignación**\n\n"
            response += f"**Mejor opción:** {top_person['name']}\n"
            response += f"Score: {top_person['score']*100:.1f}%\n"
            response += f"Experiencia: {top_person.get('experience_years', 'N/A')} años\n"
            response += f"Performance: {top_person.get('performance_index', 'N/A')}%\n\n"
            
            if top_person.get('reason'):
                response += f"💡 **¿Por qué?** {top_person['reason']}"
            
            if len(result['recommendations']) > 1:
                response += f"\n\n📌 Otras opciones: {', '.join([p['name'] for p in result['recommendations'][1:3]])}"
            
            return response
            
        except Exception as e:
            return f"❌ Error al recomendar: {str(e)}"
    
    def handle_performance_analysis(self, message: str) -> str:
        """Maneja análisis de desempeño"""
        try:
            # Buscar persona por nombre en el mensaje
            users = WebUser.query.filter(WebUser.status == 'active').all()
            
            person = None
            for user in users:
                if user.full_name.lower() in message.lower():
                    person = user
                    break
            
            if not person:
                # Si no encuentra por nombre, tomar el primero como ejemplo
                if users:
                    person = users[0]
                    message_prefix = f"(No especificaste un nombre, mostrando ejemplo con {person.full_name})\n\n"
                else:
                    return "❌ No hay usuarios activos en el sistema."
            else:
                message_prefix = ""
            
            result = predict_attrition({'person_id': person.person_id})
            
            response = message_prefix + f"📊 **Análisis de Desempeño: {person.full_name}**\n\n"
            response += f"Performance: {person.performance_index:.1f}%\n"
            response += f"Experiencia: {person.experience_years} años\n"
            response += f"Tareas completadas: {person.tasks_completed}\n"
            
            # Manejar diferentes formatos de respuesta
            if isinstance(result, dict):
                risk_level = result.get('attrition_risk', result.get('risk_level', 'N/A'))
                probability = result.get('attrition_probability', result.get('probability', 0))
                response += f"Riesgo de renuncia: **{risk_level.upper()}** ({probability*100:.1f}%)\n\n"
                
                if result.get('recommendations'):
                    response += f"💡 **Recomendación:** {result['recommendations'][0]}"
                elif result.get('factors'):
                    factors = result['factors']
                    if factors:
                        response += f"💡 **Factor principal:** {factors[0].get('factor', 'N/A')}"
            else:
                response += f"Riesgo de renuncia: N/A\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error al analizar desempeño: {str(e)}"
    
    def handle_statistics(self) -> str:
        """Retorna estadísticas generales del sistema"""
        try:
            total_tasks = WebTask.query.count()
            completed = WebTask.query.filter_by(status='completed').count()
            in_progress = WebTask.query.filter_by(status='in_progress').count()
            total_users = WebUser.query.filter_by(status='active').count()
            
            completion_rate = (completed / total_tasks * 100) if total_tasks > 0 else 0
            
            response = f"📊 **Estadísticas del Sistema**\n\n"
            response += f"📋 Total de tareas: {total_tasks}\n"
            response += f"✅ Completadas: {completed} ({completion_rate:.1f}%)\n"
            response += f"🔄 En progreso: {in_progress}\n"
            response += f"👥 Usuarios activos: {total_users}\n"
            
            return response
            
        except Exception as e:
            return f"❌ Error al obtener estadísticas: {str(e)}"
    
    def handle_help(self) -> str:
        """Retorna ayuda sobre qué puede hacer el asistente"""
        return """🤖 **Asistente IA - Comandos Disponibles**

Puedo ayudarte con:

📊 **Predicción de Riesgo**
"Predice el riesgo de una tarea de alta complejidad en TI"

⏱️ **Duración de Tareas**
"¿Cuánto tiempo tomará una tarea media de 10 días?"

👤 **Recomendación de Personas**
"¿Quién es mejor para una tarea de desarrollo?"

📈 **Análisis de Desempeño**
"Analiza el desempeño de [nombre]"

📊 **Estadísticas**
"Muestra las estadísticas del sistema"

Escribe tu pregunta naturalmente y yo la procesaré. 😊"""
    
    def process_message(self, message: str) -> str:
        """Procesa el mensaje y retorna una respuesta"""
        if not message or not message.strip():
            return "Por favor, escribe una pregunta o comando."
        
        intent = self.detect_intent(message)
        
        if intent == 'riesgo':
            return self.handle_risk_prediction(message)
        elif intent == 'duracion':
            return self.handle_duration_prediction(message)
        elif intent == 'recomendar':
            return self.handle_recommendation(message)
        elif intent == 'desempeño':
            return self.handle_performance_analysis(message)
        elif intent == 'renuncia':
            return self.handle_performance_analysis(message)  # Usa el mismo handler
        elif intent == 'estadisticas':
            return self.handle_statistics()
        elif intent == 'ayuda':
            return self.handle_help()
        else:
            return """🤔 No entendí tu pregunta. Puedo ayudarte con:

• Predicción de riesgo de tareas
• Estimación de duración
• Recomendación de personas
• Análisis de desempeño
• Estadísticas del sistema

Escribe "ayuda" para ver ejemplos."""


# Instancia global del asistente
assistant = ChatAssistant()
