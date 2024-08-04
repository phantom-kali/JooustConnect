function setTheme(theme) {
    if (theme === 'dark') {
        document.body.classList.add('dark-theme');
    } else {
        document.body.classList.remove('dark-theme');
    }
    localStorage.setItem('theme', theme);
}

function applyTheme(theme) {
    if (theme === 'system') {
        if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
            setTheme('dark');
        } else {
            setTheme('light');
        }
    } else {
        setTheme(theme);
    }
}

document.addEventListener('DOMContentLoaded', function () {
    // Apply theme on page load
    const savedTheme = localStorage.getItem('theme') || 'system';
    applyTheme(savedTheme);

    // Listen for changes in color scheme preference
    window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', e => {
        if (savedTheme === 'system') {
            applyTheme('system');
        }
    });
});