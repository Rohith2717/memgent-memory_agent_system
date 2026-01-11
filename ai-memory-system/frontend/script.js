const API_URL = "http://127.0.0.1:8000";

const chatLog = document.getElementById('chat-log');
const userInput = document.getElementById('user-input');
const sendBtn = document.getElementById('send-btn');
const taskIdInput = document.getElementById('task-id');

const historyList = document.getElementById('history-list');

// Auto resize textarea
function autoResize(textarea) {
    textarea.style.height = 'auto';
    textarea.style.height = textarea.scrollHeight + 'px';
}

async function loadHistory() {
    try {
        const response = await fetch(`${API_URL}/memory/history`);
        const data = await response.json();

        historyList.innerHTML = '';
        data.history.forEach(item => {
            const div = document.createElement('div');
            div.className = `history-item ${item.id === taskIdInput.value ? 'active' : ''}`;
            div.innerHTML = `
                <i data-lucide="message-square"></i>
                <span>${item.id}</span>
            `;
            div.onclick = () => loadSession(item.id);
            historyList.appendChild(div);
        });
        lucide.createIcons();
    } catch (e) {
        console.error("Failed to load history", e);
    }
}

async function loadSession(id) {
    taskIdInput.value = id;
    localStorage.setItem('lastTaskId', id);
    chatLog.innerHTML = '';

    try {
        const res = await fetch(`${API_URL}/memory/session/${id}`);
        const data = await res.json();

        if (data.messages && data.messages.length > 0) {
            data.messages.forEach(msg => {
                const text = msg.content;
                // Parse "User intent: ... \nAssistant response: ..."
                // We use a simple split or regex. 
                // Note: This relies on the specific format in MemoryService.
                const parts = text.split('\nAssistant response: ');
                if (parts.length === 2) {
                    const userText = parts[0].replace('User intent: ', '').trim();
                    const botText = parts[1].trim();
                    appendMessage('user', userText);
                    appendMessage('system', botText);
                } else {
                    // Fallback
                    appendMessage('system', text);
                }
            });
        } else {
            chatLog.innerHTML = `
                <div class="message system">
                    <div class="avatar"><i data-lucide="bot"></i></div>
                    <div class="content">
                        <p>Switched to session <b>${id}</b>. No history found.</p>
                    </div>
                </div>
            `;
        }
    } catch (e) {
        console.error("Error loading session:", e);
        chatLog.innerHTML = `<div class="message system"><p>Error loading history.</p></div>`;
    }

    lucide.createIcons();
    loadHistory(); // refresh active state
}

// Generate new random Task ID
function generateNewTask() {
    const id = 'task-' + Math.random().toString(36).substr(2, 6);
    loadSession(id);
}

// Add message to DOM
function appendMessage(role, text) {
    const msgDiv = document.createElement('div');
    msgDiv.className = `message ${role}`;

    const icon = role === 'user' ? 'user' : 'bot';

    // Simple mock markdown parsing
    // Bold
    let formatted = text.replace(/\*\*(.*?)\*\*/g, '<b>$1</b>');
    // Code
    formatted = formatted.replace(/`(.*?)`/g, '<code>$1</code>');
    // Newlines
    formatted = formatted.replace(/\n/g, '<br>');

    msgDiv.innerHTML = `
        <div class="avatar"><i data-lucide="${icon}"></i></div>
        <div class="content">
            <p>${formatted}</p>
        </div>
    `;

    chatLog.appendChild(msgDiv);
    lucide.createIcons();
    chatLog.scrollTop = chatLog.scrollHeight;
}

async function sendMessage() {
    const text = userInput.value.trim();
    if (!text) return;

    const taskId = taskIdInput.value;

    // UI updates
    appendMessage('user', text);
    userInput.value = '';
    userInput.style.height = 'auto';

    // Show typing indicator (mock)
    const typingDiv = document.createElement('div');
    typingDiv.className = 'message system typing';
    typingDiv.innerHTML = `
        <div class="avatar"><i data-lucide="bot"></i></div>
        <div class="content"><p>Thinking...</p></div>
    `;
    chatLog.appendChild(typingDiv);
    lucide.createIcons();
    chatLog.scrollTop = chatLog.scrollHeight;

    try {
        const response = await fetch(`${API_URL}/chat`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                task_id: taskId,
                message: text
            })
        });

        const data = await response.json();

        // Remove typing
        chatLog.removeChild(typingDiv);

        if (data.response) {
            appendMessage('system', data.response);
        } else {
            appendMessage('system', 'Error: No response from agent.');
        }

        loadHistory(); // Refresh sidebar in case this was a new task

    } catch (error) {
        chatLog.removeChild(typingDiv);
        appendMessage('system', `Error: ${error.message}. Is the backend running?`);
    }
}

// Event Listeners
sendBtn.addEventListener('click', sendMessage);

userInput.addEventListener('keydown', (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
        e.preventDefault();
        sendMessage();
    }
});

// Init
const lastId = localStorage.getItem('lastTaskId');
if (lastId) {
    loadSession(lastId);
} else {
    generateNewTask();
}
// loadHistory is called inside loadSession, but strictly we need to call it if loadSession logic fails or to init sidebar if we didn't call loadSession?
// Actually loadSession calls loadHistory at the end.
// But if we generateNewTask, it also calls loadSession.
// So we are covered. 
lucide.createIcons();
