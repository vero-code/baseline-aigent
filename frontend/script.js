const chatForm = document.getElementById('chat-form');
const messageInput = document.getElementById('message-input');
const messagesContainer = document.getElementById('messages-container');
const sendButton = document.getElementById('send-button');

const API_URL = 'http://127.0.0.1:8000/api/ask';

// Add new message to chat
function addMessage(sender, text) {
    const messageElement = document.createElement('div');
    messageElement.classList.add('message', `${sender}-message`);

    if (sender === 'ai') {
        // Use marked to render Markdown
        messageElement.innerHTML = marked.parse(text);
    } else {
        const p = document.createElement('p');
        p.textContent = text;
        messageElement.appendChild(p);
    }

    messagesContainer.appendChild(messageElement);
    // Scroll down to see the latest message
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Display loading indicator
function showLoadingIndicator() {
    const loadingElement = document.createElement('div');
    loadingElement.classList.add('message', 'ai-message', 'loading-indicator');
    loadingElement.innerHTML = `
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
    `;
    messagesContainer.appendChild(loadingElement);
    messagesContainer.scrollTop = messagesContainer.scrollHeight;
}

// Remove loading indicator
function hideLoadingIndicator() {
    const loadingElement = document.querySelector('.loading-indicator');
    if (loadingElement) {
        loadingElement.remove();
    }
}

// Form submission handler
chatForm.addEventListener('submit', async (event) => {
    event.preventDefault();

    const userMessage = messageInput.value.trim();
    if (!userMessage) return;

    addMessage('user', userMessage);
    messageInput.value = '';
    
    showLoadingIndicator();

    try {
        const response = await fetch(API_URL, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ query: userMessage }),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        hideLoadingIndicator();
        
        addMessage('ai', data.response);
    } catch (error) {
        console.error('Error fetching AI response:', error);
        hideLoadingIndicator();
        addMessage('ai', 'Sorry, an error occurred.');
    }
});