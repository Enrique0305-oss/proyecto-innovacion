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
                ¡Hola! Soy tu asistente de IA. Puedo ayudarte a analizar predicciones, resumir insights y recomendar acciones. ¿En qué puedo ayudarte hoy?
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

    // Simular respuesta del bot
    setTimeout(() => {
      const responses = [
        'Basándome en los datos actuales, puedo observar que la eficiencia general está en 85%, lo cual es un buen indicador. ¿Te gustaría profundizar en algún área específica?',
        'He detectado 3 cuellos de botella que requieren atención. El proceso de aprobación parece ser el punto crítico. ¿Quieres que analice las causas?',
        'Las predicciones de los 24 modelos activos muestran una precisión del 95%. Te recomiendo priorizar las tareas en el área de Operaciones para mejorar la eficiencia en un 15%.',
        'Según el análisis, Luis García tiene el perfil ideal para 5 tareas prioritarias. ¿Deseas ver el detalle de la recomendación?',
        'El tiempo promedio ha disminuido un 12% respecto al mes anterior, lo cual es excelente. ¿Necesitas un reporte detallado de esta métrica?'
      ];
      
      const randomResponse = responses[Math.floor(Math.random() * responses.length)];
      addMessage(randomResponse, true);
    }, 1000);
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
