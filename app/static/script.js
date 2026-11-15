// ============================================================
// ACCESSIBILITY SETTINGS (Theme, Font Size, Language)
// ============================================================

const i18nTranslations = {
    en: {
        nav_home: "Home",
        nav_ask_ai: "Ask AI",
        nav_rights: "Rights",
        nav_documents: "Documents",
        nav_emergency: "Emergency",
        nav_sos: "SOS Shield",
        accessibility_settings: "Accessibility Settings",
        accessibility_subtitle: "Customize your viewing, language, and readability preferences.",
        language_label: "Language",
        theme_label: "Theme",
        theme_light: "Light",
        theme_dark: "Dark",
        theme_system: "System",
        font_size_label: "Font Size",
        font_small: "Small",
        font_medium: "Medium",
        font_large: "Large",
        font_xlarge: "XL",
        save_close: "Save & Close"
    },
    hi: {
        nav_home: "होम",
        nav_ask_ai: "एआई से पूछें",
        nav_rights: "अधिकार",
        nav_documents: "दस्तावेज़",
        nav_emergency: "आपातकाल",
        nav_sos: "एसओएस शील्ड",
        accessibility_settings: "एक्सेसिबिलिटी सेटिंग्स",
        accessibility_subtitle: "अपनी देखने, भाषा और पठनीयता प्राथमिकताओं को कस्टमाइज़ करें।",
        language_label: "भाषा",
        theme_label: "थीम",
        theme_light: "लाइट",
        theme_dark: "डार्क",
        theme_system: "सिस्टम",
        font_size_label: "फ़ॉन्ट साइज़",
        font_small: "छोटा",
        font_medium: "मध्यम",
        font_large: "बड़ा",
        font_xlarge: "अतिरिक्त बड़ा",
        save_close: "सहेजें और बंद करें"
    },
    mr: {
        nav_home: "मुखपृष्ठ",
        nav_ask_ai: "एआय विचारा",
        nav_rights: "हक्क",
        nav_documents: "कागदपत्रे",
        nav_emergency: "आणीबाणी",
        nav_sos: "एसओएस शील्ड",
        accessibility_settings: "अॅक्सेसिबिलिटी सेटिंग्ज",
        accessibility_subtitle: "तुमच्या पाहण्याच्या, भाषेच्या आणि वाचनीयतेच्या प्राधान्या सानुकूलित करा.",
        language_label: "भाषा",
        theme_label: "थीम",
        theme_light: "लाईट",
        theme_dark: "डार्क",
        theme_system: "सिस्टम",
        font_size_label: "फॉन्ट आकार",
        font_small: "लहान",
        font_medium: "मध्यम",
        font_large: "मोठे",
        font_xlarge: "अति मोठे",
        save_close: "सेव्ह करा आणि बंद करा"
    }
};

function openAccessibilityModal() {
    const modal = document.getElementById('accessibilityModal');
    if (modal) modal.classList.add('active');
}

function closeAccessibilityModal() {
    const modal = document.getElementById('accessibilityModal');
    if (modal) modal.classList.remove('active');
}

function setTheme(theme) {
    localStorage.setItem('lawaid_theme', theme);
    applyTheme(theme);
    updateActiveButtons('theme', theme);
    updateSiteLogo();
}

function applyTheme(theme) {
    const body = document.body;
    body.classList.remove('light-theme');

    if (theme === 'light') {
        body.classList.add('light-theme');
    } else if (theme === 'system') {
        const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
        if (!prefersDark) {
            body.classList.add('light-theme');
        }
    }
}

function updateSiteLogo() {
    const logo = document.getElementById('site-logo');
    if (!logo) return;

    const isLightTheme = document.body.classList.contains('light-theme');

    logo.src = isLightTheme
        ? logo.dataset.lightLogo
        : logo.dataset.darkLogo;
}

window.matchMedia('(prefers-color-scheme: dark)').addEventListener('change', () => {
    const savedTheme = localStorage.getItem('lawaid_theme');

    if (savedTheme === 'system') {
        applyTheme('system');
        updateSiteLogo();
    }
});

function setFontSize(size) {
    localStorage.setItem('lawaid_fontsize', size);
    applyFontSize(size);
    updateActiveButtons('fontsize', size);
}

function applyFontSize(size) {
    const htmlEl = document.documentElement;
    if (['small', 'medium', 'large', 'xlarge'].includes(size)) {
        htmlEl.setAttribute('data-font-size', size);
    } else {
        htmlEl.setAttribute('data-font-size', 'medium');
    }
}

function changeLanguage(lang) {
    localStorage.setItem('lawaid_lang', lang);
    applyLanguage(lang);
    const select = document.getElementById('langSelect');
    if (select) select.value = lang;
}

function applyLanguage(lang) {
    const translations = i18nTranslations[lang] || i18nTranslations['en'];
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (translations[key]) {
            el.textContent = translations[key];
        }
    });
}

function updateActiveButtons(type, val) {
    if (type === 'theme') {
        document.querySelectorAll('.theme-option-btn').forEach(btn => {
            if (btn.getAttribute('data-theme-val') === val) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    } else if (type === 'fontsize') {
        document.querySelectorAll('.fontsize-option-btn').forEach(btn => {
            if (btn.getAttribute('data-size-val') === val) {
                btn.classList.add('active');
            } else {
                btn.classList.remove('active');
            }
        });
    }
}

function initAccessibilitySettings() {
    const savedTheme = localStorage.getItem('lawaid_theme') || 'dark';
    const savedFontSize = localStorage.getItem('lawaid_fontsize') || 'medium';
    const savedLang = localStorage.getItem('lawaid_lang') || 'en';

    setTheme(savedTheme);
    setFontSize(savedFontSize);
    changeLanguage(savedLang);

    // Clean up legacy theme key if present
    if (localStorage.getItem('theme')) {
        localStorage.removeItem('theme');
    }
}

// Run on load and setup global event listeners (Outside click, Escape key)
document.addEventListener('DOMContentLoaded', () => {
    initAccessibilitySettings();

    // Close modal when clicking outside content overlay
    const modal = document.getElementById('accessibilityModal');
    if (modal) {
        modal.addEventListener('click', (e) => {
            if (e.target === modal) {
                closeAccessibilityModal();
            }
        });
    }

    // Close modal on Escape key
    window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            closeAccessibilityModal();
        }
    });
});
