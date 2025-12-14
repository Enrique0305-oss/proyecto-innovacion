import { API_URL } from '../utils/api';

export function AIAssistant(): string {
  return `
    <div class="ai-assistant-overlay" id="aiAssistantOverlay">
      <div class="ai-assistant-panel">
        <div class="ai-assistant-header">
          <div class="ai-assistant-title">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M12 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="currentColor"/>
            </svg>
            <div>
              <h3>AI Assistant</h3>
              <p class="ai-status">En línea</p>
            </div>
          </div>
          <button class="ai-close-btn" id="aiCloseBtn">
            <svg width="24" height="24" viewBox="0 0 24 24" fill="none">
              <path d="M18 6L6 18M6 6l12 12" stroke="currentColor" stroke-width="2" stroke-linecap="round"/>
            </svg>
          </button>
        </div>

        <div class="ai-assistant-body" id="aiChatBody">
          <div class="ai-message ai-message-bot">
            <div class="ai-message-avatar">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="currentColor"/>
              </svg>
            </div>
            <div class="ai-message-content">
              <div class="ai-message-text">
                ¡Hola! 👋 Soy tu asistente de IA. Puedo ayudarte a:<br><br>
                📊 Predecir riesgos de tareas<br>
                ⏱️ Estimar duraciones<br>
                👤 Recomendar personas<br>
                📈 Analizar desempeño<br>
                📋 Mostrar estadísticas<br><br>
                Escribe "ayuda" para ver ejemplos de comandos. ¿En qué puedo ayudarte?
              </div>
            </div>
          </div>
        </div>

        <div class="ai-assistant-footer">
          <div class="ai-input-wrapper">
            <input 
              type="text" 
              class="ai-input" 
              id="aiInput" 
              placeholder="Escribe tu pregunta..."
              autocomplete="off"
            />
            <button class="ai-send-btn" id="aiSendBtn">
              <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
                <path d="M2 10l16-8-8 16-2-8-6-0z" fill="currentColor"/>
              </svg>
            </button>
          </div>
        </div>
      </div>
    </div>
  `;
}

export function initAIAssistant() {
  let isOpen = false;

  function openAssistant() {
    const overlay = document.getElementById('aiAssistantOverlay');
    if (overlay) {
      overlay.classList.add('active');
      isOpen = true;
      
      // Enfocar el input
      setTimeout(() => {
        const input = document.getElementById('aiInput') as HTMLInputElement;
        if (input) input.focus();
      }, 100);
    }
  }

  function closeAssistant() {
    const overlay = document.getElementById('aiAssistantOverlay');
    if (overlay) {
      overlay.classList.remove('active');
      isOpen = false;
    }
  }

  function addMessage(text: string, isBot: boolean) {
    const chatBody = document.getElementById('aiChatBody');
    if (!chatBody) return;

    const messageDiv = document.createElement('div');
    messageDiv.className = `ai-message ${isBot ? 'ai-message-bot' : 'ai-message-user'}`;
    
    if (isBot) {
      messageDiv.innerHTML = `
        <div class="ai-message-avatar">
          <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
            <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="currentColor"/>
          </svg>
        </div>
        <div class="ai-message-content">
          <div class="ai-message-text">${text}</div>
        </div>
      `;
    } else {
      messageDiv.innerHTML = `
        <div class="ai-message-content">
          <div class="ai-message-text">${text}</div>
        </div>
      `;
    }

    chatBody.appendChild(messageDiv);
    chatBody.scrollTop = chatBody.scrollHeight;
  }

  function handleSendMessage() {
    const input = document.getElementById('aiInput') as HTMLInputElement;
    if (!input || !input.value.trim()) return;

    const userMessage = input.value.trim();
    addMessage(userMessage, false);
    input.value = '';

    // Mostrar indicador de "escribiendo..."
    const chatBody = document.getElementById('aiChatBody');
    const typingIndicator = document.createElement('div');
    typingIndicator.className = 'ai-message ai-message-bot typing-indicator';
    typingIndicator.id = 'typingIndicator';
    typingIndicator.innerHTML = `
      <div class="ai-message-avatar">
        <svg width="20" height="20" viewBox="0 0 20 20" fill="none">
          <path d="M10 2l2 6h6l-5 4 2 6-5-4-5 4 2-6-5-4h6l2-6z" fill="currentColor"/>
        </svg>
      </div>
      <div class="ai-message-content">
        <div class="ai-message-text">
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
          <span class="typing-dot"></span>
        </div>
      </div>
    `;
    chatBody?.appendChild(typingIndicator);
    if (chatBody) chatBody.scrollTop = chatBody.scrollHeight;

    // Llamar al backend real
    fetch(`${API_URL}/ml/chat`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${localStorage.getItem('access_token')}`
      },
      body: JSON.stringify({ message: userMessage })
    })
    .then(response => response.json())
    .then(data => {
      // Remover indicador de escribiendo
      const indicator = document.getElementById('typingIndicator');
      if (indicator) indicator.remove();

      // Mostrar respuesta del asistente
      const response = data.response || 'Lo siento, no pude procesar tu mensaje.';
      addMessage(response, true);
    })
    .catch(error => {
      console.error('Error en chat:', error);
      
      // Remover indicador de escribiendo
      const indicator = document.getElementById('typingIndicator');
      if (indicator) indicator.remove();

      // Respuesta de error
      addMessage('❌ Lo siento, ocurrió un error al procesar tu mensaje. Por favor, intenta de nuevo.', true);
    });
  }

  // Event listeners
  const aiButton = document.querySelector('.btn-ai-assistant');
  if (aiButton) {
    aiButton.addEventListener('click', openAssistant);
  }

  document.addEventListener('click', (e) => {
    const closeBtn = (e.target as Element).closest('#aiCloseBtn');
    if (closeBtn) {
      closeAssistant();
    }
  });

  // Cerrar al hacer click fuera del panel
  document.addEventListener('click', (e) => {
    const overlay = document.getElementById('aiAssistantOverlay');
    if (overlay && e.target === overlay) {
      closeAssistant();
    }
  });

  // Enviar mensaje
  document.addEventListener('click', (e) => {
    const sendBtn = (e.target as Element).closest('#aiSendBtn');
    if (sendBtn) {
      handleSendMessage();
    }
  });

  // Enviar con Enter
  document.addEventListener('keypress', (e) => {
    if (e.key === 'Enter') {
      const input = e.target as HTMLInputElement;
      if (input && input.id === 'aiInput') {
        handleSendMessage();
      }
    }
  });

  // Escape para cerrar
  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && isOpen) {
      closeAssistant();
    }
  });
}
