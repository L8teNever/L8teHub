// Login/Logout Funktionen
let currentContent = window.siteContent || {};

function toggleLogin() {
    const modal = document.getElementById('login-modal');
    modal.classList.toggle('active');
    document.body.style.overflow = modal.classList.contains('active') ? 'hidden' : 'auto';
}

function toggleEdit() {
    const modal = document.getElementById('edit-modal');
    modal.classList.toggle('active');
    document.body.style.overflow = modal.classList.contains('active') ? 'hidden' : 'auto';
    
    if (modal.classList.contains('active')) {
        loadContentToForm();
    }
}

async function handleLogin(event) {
    event.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    const errorDiv = document.getElementById('login-error');

    try {
        const response = await fetch('/api/login', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({username, password})
        });

        const data = await response.json();

        if (data.success) {
            window.isLoggedIn = true;
            updateUIForLogin();
            toggleLogin();
            errorDiv.classList.add('hidden');
        } else {
            errorDiv.textContent = data.message || 'Login fehlgeschlagen';
            errorDiv.classList.remove('hidden');
        }
    } catch (error) {
        errorDiv.textContent = 'Verbindungsfehler';
        errorDiv.classList.remove('hidden');
    }
}

async function handleLogout() {
    try {
        await fetch('/api/logout', {method: 'POST'});
        window.isLoggedIn = false;
        updateUIForLogout();
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

function loadContentToForm() {
    document.getElementById('edit-name').value = currentContent.name || '';
    document.getElementById('edit-subtitle-de').value = currentContent.subtitle_de || '';
    document.getElementById('edit-age').value = currentContent.age || '';
    document.getElementById('edit-status-de').value = currentContent.status_de || '';
    document.getElementById('edit-vibe').value = currentContent.vibe || '';
    document.getElementById('edit-location').value = currentContent.location || '';
    document.getElementById('edit-github').value = currentContent.github_url || '';
    document.getElementById('edit-instagram').value = currentContent.instagram_url || '';
}

async function handleSaveContent(event) {
    event.preventDefault();
    const successDiv = document.getElementById('edit-success');
    const errorDiv = document.getElementById('edit-error');

    const updatedContent = {
        name: document.getElementById('edit-name').value,
        subtitle_de: document.getElementById('edit-subtitle-de').value,
        subtitle_en: currentContent.subtitle_en || 'Digital Creator & Developer',
        subtitle_jp: currentContent.subtitle_jp || 'デジタルクリエイター＆開発者',
        age: document.getElementById('edit-age').value,
        status_de: document.getElementById('edit-status-de').value,
        status_en: currentContent.status_en || 'Student',
        vibe: document.getElementById('edit-vibe').value,
        location: document.getElementById('edit-location').value,
        github_url: document.getElementById('edit-github').value,
        instagram_url: document.getElementById('edit-instagram').value,
        email: currentContent.email || 'hello@l8tenever.com',
        address: currentContent.address || 'Musterstraße 123<br>12345 Berlin'
    };

    try {
        const response = await fetch('/api/content', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
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
                location.reload(); // Seite neu laden um Änderungen anzuzeigen
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

// Init Login-Status beim Laden
document.addEventListener('DOMContentLoaded', () => {
    if (window.isLoggedIn) {
        updateUIForLogin();
    }
});
