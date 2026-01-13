// Admin Panel für Hub-Buttons, Impressum und Datenschutz

let currentContent = window.siteContent || {};
let editingButtonIndex = -1;

// Login/Logout Funktionen
window.toggleLogin = function () {
    const modal = document.getElementById('login-modal');
    if (!modal) return;
    modal.classList.toggle('active');
    document.body.style.overflow = modal.classList.contains('active') ? 'hidden' : 'auto';
};

window.toggleEdit = function () {
    const modal = document.getElementById('edit-modal');
    if (!modal) return;
    modal.classList.toggle('active');
    document.body.style.overflow = modal.classList.contains('active') ? 'hidden' : 'auto';

    if (modal.classList.contains('active')) {
        loadContentToForm();
    }
};

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');

    errorDiv.classList.add('hidden');

    try {
        console.log('Versuche Login für:', username);
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ username, password })
        });

        const data = await response.json();
        console.log('Login Response:', data);

        if (response.ok && data.success) {
            window.isLoggedIn = true;
            updateUIForLogin();
            toggleLogin();
            // Lade aktuelle Inhalte
            await loadCurrentContent();
        } else {
            errorDiv.textContent = data.message || 'Login fehlgeschlagen (Falsche Daten?)';
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Login Error:', error);
        errorDiv.textContent = 'Verbindungsfehler: Der Server ist nicht erreichbar oder liefert keine gültige Antwort. (Details in der Konsole)';
        errorDiv.classList.remove('hidden');
    }
}

async function handleLogout() {
    try {
        const response = await fetch('/api/logout', { method: 'POST' });
        if (response.ok) {
            window.isLoggedIn = false;
            updateUIForLogout();
            location.reload(); // Reload um alles sauber zurückzusetzen
        }
    } catch (error) {
        console.error('Logout fehlgeschlagen:', error);
    }
}

function updateUIForLogin() {
    document.getElementById('btn-login').classList.add('hidden');
    document.getElementById('btn-edit').classList.remove('hidden');
    document.getElementById('btn-logout').classList.remove('hidden');
}

function updateUIForLogout() {
    document.getElementById('btn-login').classList.remove('hidden');
    document.getElementById('btn-edit').classList.add('hidden');
    document.getElementById('btn-logout').classList.add('hidden');
}

async function loadCurrentContent() {
    try {
        const response = await fetch('/api/content');
        const data = await response.json();
        currentContent = data;
        window.siteContent = data;
    } catch (error) {
        console.error('Fehler beim Laden:', error);
    }
}

function loadContentToForm() {
    // Basis-Informationen
    document.getElementById('edit-name').value = currentContent.name || '';
    document.getElementById('edit-email').value = currentContent.email || '';
    document.getElementById('edit-address').value = currentContent.address || '';
    document.getElementById('edit-subtitle-de').value = currentContent.subtitle_de || '';
    document.getElementById('edit-subtitle-en').value = currentContent.subtitle_en || '';
    document.getElementById('edit-status-de').value = currentContent.status_de || '';
    document.getElementById('edit-status-en').value = currentContent.status_en || '';
    document.getElementById('edit-age').value = currentContent.age || '';
    document.getElementById('edit-vibe').value = currentContent.vibe || '';
    document.getElementById('edit-location').value = currentContent.location || '';
    document.getElementById('edit-github').value = currentContent.github_url || '';
    document.getElementById('edit-instagram').value = currentContent.instagram_url || '';

    // Hub-Buttons laden
    renderHubButtonsEditor();

    // Impressum laden
    if (currentContent.impressum) {
        document.getElementById('edit-impressum-company').value = currentContent.impressum.company || '';
        document.getElementById('edit-impressum-address1').value = currentContent.impressum.address_line1 || '';
        document.getElementById('edit-impressum-address2').value = currentContent.impressum.address_line2 || '';
        document.getElementById('edit-impressum-country').value = currentContent.impressum.country || '';
        document.getElementById('edit-impressum-email').value = currentContent.impressum.email || '';
    }

    // Datenschutz laden
    if (currentContent.privacy) {
        document.getElementById('edit-privacy-intro-de').value = currentContent.privacy.intro_de || '';
        document.getElementById('edit-privacy-processing-de').value = currentContent.privacy.data_processing_de || '';
        document.getElementById('edit-privacy-logs-de').value = currentContent.privacy.server_logs_de || '';
    }
}

function renderHubButtonsEditor() {
    const container = document.getElementById('hub-buttons-editor');
    const buttons = currentContent.hub_buttons || [];

    container.innerHTML = buttons.map((btn, index) => `
        <div class="android-card p-4 bg-[var(--m3-surface)] mb-3">
            <div class="flex justify-between items-center">
                <div>
                    <strong>${btn.name_de}</strong>
                    <p class="text-sm opacity-60">${btn.url}</p>
                </div>
                <div class="flex gap-2">
                    <button onclick="editHubButton(${index})" class="px-3 py-1 bg-blue-500 text-white rounded">
                        Bearbeiten
                    </button>
                    <button onclick="deleteHubButton(${index})" class="px-3 py-1 bg-red-500 text-white rounded">
                        Löschen
                    </button>
                </div>
            </div>
        </div>
    `).join('') + `
        <button onclick="addNewHubButton()" class="w-full py-3 bg-green-500 text-white rounded-lg font-semibold">
            + Neuer Button
        </button>
    `;
}

function editHubButton(index) {
    editingButtonIndex = index;
    const btn = currentContent.hub_buttons[index];

    document.getElementById('hub-btn-name-de').value = btn.name_de;
    document.getElementById('hub-btn-desc-de').value = btn.desc_de;
    document.getElementById('hub-btn-url').value = btn.url;
    document.getElementById('hub-btn-icon').value = btn.icon;

    document.getElementById('hub-button-modal').classList.add('active');
}

function addNewHubButton() {
    editingButtonIndex = -1;
    document.getElementById('hub-btn-name-de').value = '';
    document.getElementById('hub-btn-desc-de').value = '';
    document.getElementById('hub-btn-url').value = '';
    document.getElementById('hub-btn-icon').value = 'study';

    document.getElementById('hub-button-modal').classList.add('active');
}

function saveHubButton() {
    const newButton = {
        id: document.getElementById('hub-btn-name-de').value.replace(/\s/g, ''),
        name_de: document.getElementById('hub-btn-name-de').value,
        name_en: document.getElementById('hub-btn-name-de').value,
        desc_de: document.getElementById('hub-btn-desc-de').value,
        desc_en: document.getElementById('hub-btn-desc-de').value,
        url: document.getElementById('hub-btn-url').value,
        icon: document.getElementById('hub-btn-icon').value
    };

    if (!currentContent.hub_buttons) {
        currentContent.hub_buttons = [];
    }

    if (editingButtonIndex >= 0) {
        currentContent.hub_buttons[editingButtonIndex] = newButton;
    } else {
        currentContent.hub_buttons.push(newButton);
    }

    document.getElementById('hub-button-modal').classList.remove('active');
    renderHubButtonsEditor();
}

function deleteHubButton(index) {
    if (confirm('Button wirklich löschen?')) {
        currentContent.hub_buttons.splice(index, 1);
        renderHubButtonsEditor();
    }
}

function cancelHubButtonEdit() {
    document.getElementById('hub-button-modal').classList.remove('active');
}

async function handleSaveContent(event) {
    event.preventDefault();
    const successDiv = document.getElementById('edit-success');
    const errorDiv = document.getElementById('edit-error');

    const updatedContent = {
        name: document.getElementById('edit-name').value,
        email: document.getElementById('edit-email').value,
        address: document.getElementById('edit-address').value,
        subtitle_de: document.getElementById('edit-subtitle-de').value,
        subtitle_en: document.getElementById('edit-subtitle-en').value,
        age: document.getElementById('edit-age').value,
        status_de: document.getElementById('edit-status-de').value,
        status_en: document.getElementById('edit-status-en').value,
        vibe: document.getElementById('edit-vibe').value,
        location: document.getElementById('edit-location').value,
        github_url: document.getElementById('edit-github').value,
        instagram_url: document.getElementById('edit-instagram').value,

        // Hub-Buttons
        hub_buttons: currentContent.hub_buttons || [],

        // Impressum
        impressum: {
            company: document.getElementById('edit-impressum-company').value,
            address_line1: document.getElementById('edit-impressum-address1').value,
            address_line2: document.getElementById('edit-impressum-address2').value,
            country: document.getElementById('edit-impressum-country').value,
            email: document.getElementById('edit-impressum-email').value,
            responsible: document.getElementById('edit-impressum-company').value
        },

        // Datenschutz
        privacy: {
            intro_de: document.getElementById('edit-privacy-intro-de').value,
            intro_en: currentContent.privacy?.intro_en || 'This website does not use cookies or tracking.',
            data_processing_de: document.getElementById('edit-privacy-processing-de').value,
            data_processing_en: currentContent.privacy?.data_processing_en || 'We do not process any personal data.',
            server_logs_de: document.getElementById('edit-privacy-logs-de').value,
            server_logs_en: currentContent.privacy?.server_logs_en || 'For technical reasons, temporary connection data is stored.'
        }
    };

    try {
        const response = await fetch('/api/content', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(updatedContent)
        });

        const data = await response.json();

        if (data.success) {
            currentContent = updatedContent;
            successDiv.textContent = 'Erfolgreich gespeichert!';
            successDiv.classList.remove('hidden');
            errorDiv.classList.add('hidden');
            setTimeout(() => {
                toggleEdit();
                successDiv.classList.add('hidden');
                location.reload();
            }, 1500);
        } else {
            errorDiv.textContent = data.error || 'Speichern fehlgeschlagen';
            errorDiv.classList.remove('hidden');
            successDiv.classList.add('hidden');
        }
    } catch (error) {
        errorDiv.textContent = 'Verbindungsfehler';
        errorDiv.classList.remove('hidden');
        successDiv.classList.add('hidden');
    }
}

function switchAdminTab(tabId) {
    // Buttons resetten
    document.querySelectorAll('.admin-tab-btn').forEach(btn => btn.classList.remove('active'));
    // Tab Inhalte verstecken
    document.querySelectorAll('.admin-tab-content').forEach(content => content.classList.add('hidden'));

    // Aktiven Tab/Button anzeigen
    document.getElementById(`tab-btn-${tabId}`).classList.add('active');
    document.getElementById(`admin-tab-${tabId}`).classList.remove('hidden');
}

// Init beim Laden
document.addEventListener('DOMContentLoaded', () => {
    if (window.isLoggedIn) {
        updateUIForLogin();
        loadCurrentContent();
    }
});
