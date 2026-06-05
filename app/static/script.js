// Theme Management
function initTheme() {
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;

    console.log('Initializing theme. Saved theme:', savedTheme);
    if (savedTheme === 'light') {
        document.body.classList.add('light-theme');
    } else if (savedTheme === 'dark') {
        document.body.classList.remove('light-theme');
    } else if (prefersDark) {
        document.body.classList.remove('light-theme');
    } else {
        // Default to dark for this app as requested
        document.body.classList.remove('light-theme');
    }
    updateThemeIcon();
}

function toggleTheme() {
    console.log('Toggling theme...');
    document.body.classList.toggle('light-theme');
    const isLight = document.body.classList.contains('light-theme');
    console.log('Is light theme now:', isLight);
    localStorage.setItem('theme', isLight ? 'light' : 'dark');
    updateThemeIcon();
}

function updateThemeIcon() {
    const themeBtn = document.getElementById('theme-toggle-btn');
    if (themeBtn) {
        const isLight = document.body.classList.contains('light-theme');
        themeBtn.innerHTML = isLight ? '<ion-icon name="moon-outline"></ion-icon>' : '<ion-icon name="sunny-outline"></ion-icon>';
        themeBtn.setAttribute('title', isLight ? 'Switch to Dark Mode' : 'Switch to Light Mode');
    }
}

// Initialize on load
document.addEventListener('DOMContentLoaded', () => {
    initTheme();

    const themeBtn = document.getElementById('theme-toggle-btn');
    if (themeBtn) {
        themeBtn.addEventListener('click', toggleTheme);
    }
});
