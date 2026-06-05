// Modal Content Data for LawAid X Sanvidhan
const modalData = {
    // ========================================
    // HOW IT WORKS SECTION (4 modals)
    // ========================================
    'how-it-works-1': {
        icon: 'chatbubble-ellipses-outline',
        title: 'Ask Your Legal Question',
        description: 'Our AI-powered chat interface makes it easy to get legal help in plain language. Simply type your question as you would ask a friend - no legal jargon required.',
        keyPoints: [
            'Ask questions in Hindi or English',
            'Get instant responses 24/7',
            'No registration required for basic queries',
            'Privacy-focused - your questions are confidential',
            'Follow-up questions to clarify your situation'
        ],
        cta: {
            text: 'Try Legal Chat',
            link: '/chat-ui',
            icon: 'chatbubbles-outline'
        }
    },

    'how-it-works-2': {
        icon: 'analytics-outline',
        title: 'AI Analyzes Indian Law',
        description: 'Our advanced AI system, powered by Google Gemini, processes your question against a comprehensive database of Indian constitutional law, statutes, and legal precedents.',
        keyPoints: [
            'Searches through the Indian Constitution',
            'References relevant IPC sections and amendments',
            'Considers Supreme Court judgments',
            'Analyzes state-specific laws when applicable',
            'Cross-references multiple legal sources for accuracy'
        ],
        cta: null
    },

    'how-it-works-3': {
        icon: 'bulb-outline',
        title: 'Get Clear Answers',
        description: 'Receive easy-to-understand explanations of your legal rights and options. We break down complex legal concepts into simple, actionable information.',
        keyPoints: [
            'Plain language explanations (no legal jargon)',
            'Step-by-step guidance for your situation',
            'References to specific articles and sections',
            'Practical next steps you can take',
            'Links to relevant government resources'
        ],
        cta: null
    },

    'how-it-works-4': {
        icon: 'shield-checkmark-outline',
        title: 'Take Immediate Action',
        description: 'Beyond answers, we provide tools to help you act on your rights. Generate legal documents, activate emergency alerts, or find immediate guidance for urgent situations.',
        keyPoints: [
            'Generate FIR complaints and legal notices',
            'Create RTI (Right to Information) requests',
            'Activate SOS Shield for emergencies',
            'Access RightNow! for immediate legal situations',
            'Download documents in PDF format'
        ],
        cta: {
            text: 'Explore Emergency Tools',
            link: '/sos-shield',
            icon: 'flash-outline'
        }
    },

    // ========================================
    // WHY CHOOSE US SECTION (3 modals)
    // ========================================
    'why-choose-india': {
        icon: 'flag-outline',
        title: 'Built for India',
        description: 'Unlike generic legal platforms, LawAid X Sanvidhan is specifically designed for the Indian legal system. We understand the unique challenges Indian citizens face when seeking legal help.',
        keyPoints: [
            'Complete Indian Constitution explainer',
            'IPC, CrPC, and major Indian statutes',
            'State-specific laws and regulations',
            'Understanding of Indian legal procedures',
            'Culturally relevant examples and scenarios',
            'Support for regional legal variations'
        ],
        cta: {
            text: 'Explore Constitution',
            link: '/constitution',
            icon: 'book-outline'
        }
    },

    'why-choose-ai': {
        icon: 'hardware-chip-outline',
        title: 'Powered by Advanced AI',
        description: 'We leverage Google Gemini, one of the world\'s most advanced AI systems, to provide accurate and contextual legal information. Our AI is specifically trained on Indian legal texts.',
        keyPoints: [
            'Google Gemini AI technology',
            'Trained on Indian legal corpus',
            'Natural language understanding',
            'Context-aware responses',
            'Continuous learning and updates',
            'Fast response times (typically under 5 seconds)'
        ],
        cta: null
    },

    'why-choose-simple': {
        icon: 'happy-outline',
        title: 'Simple Language Promise',
        description: 'Legal language can be intimidating and confusing. We\'re committed to explaining your rights in clear, simple terms that anyone can understand - because justice should be accessible to all.',
        keyPoints: [
            'No complex legal terminology',
            'Explanations in everyday language',
            'Visual aids and examples when helpful',
            'Bilingual support (English & Hindi)',
            'Definitions for unavoidable legal terms',
            'Focus on practical understanding'
        ],
        cta: null
    },

    // ========================================
    // LEGAL TOPICS SECTION (9 modals)
    // ========================================
    'topic-fundamental-rights': {
        icon: 'hammer-outline',
        title: 'Fundamental Rights',
        description: 'Learn about your constitutional rights guaranteed by the Indian Constitution - the foundation of Indian democracy.',
        keyPoints: [
            'Right to Equality (Articles 14-18)',
            'Right to Freedom (Articles 19-22)',
            'Right against Exploitation (Articles 23-24)',
            'Right to Freedom of Religion (Articles 25-28)',
            'Cultural and Educational Rights (Articles 29-30)',
            'Right to Constitutional Remedies (Article 32)'
        ],
        cta: {
            text: 'Learn More',
            link: '/constitution',
            icon: 'book-outline'
        }
    },

    'topic-consumer-rights': {
        icon: 'cart-outline',
        title: 'Consumer Rights',
        description: 'Understand your rights as a consumer under the Consumer Protection Act, 2019. Get help with defective products, unfair practices, and service issues.',
        keyPoints: [
            'Right to safety and quality products',
            'Right to be informed about products/services',
            'Right to choose and fair competition',
            'Right to be heard and file complaints',
            'Right to seek redressal and compensation',
            'Protection against unfair trade practices'
        ],
        cta: {
            text: 'File Consumer Complaint',
            link: '/chat-ui',
            icon: 'document-text-outline'
        }
    },

    'topic-cyber-crime': {
        icon: 'laptop-outline',
        title: 'Cyber Crime Protection',
        description: 'Stay safe online and know your rights under the IT Act, 2000. Learn how to report cyber crimes and protect yourself from digital threats.',
        keyPoints: [
            'Identity theft and phishing protection',
            'Online harassment and cyberbullying',
            'Hacking and unauthorized access',
            'Data privacy violations',
            'How to report cyber crimes to authorities',
            'Digital evidence preservation'
        ],
        cta: {
            text: 'Report Cyber Crime',
            link: '/chat-ui',
            icon: 'shield-outline'
        }
    },

    'topic-women-child': {
        icon: 'people-circle-outline',
        title: 'Women & Child Safety',
        description: 'Comprehensive legal protection for women and children under various Indian laws including POCSO, Domestic Violence Act, and more.',
        keyPoints: [
            'Protection from domestic violence',
            'Sexual harassment laws (workplace & public)',
            'POCSO Act for child protection',
            'Dowry prohibition and related crimes',
            'Women\'s property and inheritance rights',
            'Emergency helplines and support services'
        ],
        cta: {
            text: 'Emergency SOS',
            link: '/sos-shield',
            icon: 'flash-outline'
        }
    },

    'topic-fir-police': {
        icon: 'document-attach-outline',
        title: 'FIR & Police Procedures',
        description: 'Know your rights when dealing with police. Learn how to file an FIR, what to expect during investigations, and your legal protections.',
        keyPoints: [
            'How to file an FIR (First Information Report)',
            'Your rights during police questioning',
            'Arrest procedures and bail rights',
            'Zero FIR and when to use it',
            'Complaint against police misconduct',
            'Legal aid and representation rights'
        ],
        cta: {
            text: 'Generate FIR Draft',
            link: '/chat-ui',
            icon: 'create-outline'
        }
    },

    'topic-digital-fraud': {
        icon: 'card-outline',
        title: 'Digital Fraud Prevention',
        description: 'Protect yourself from online scams, UPI fraud, and digital payment frauds. Learn immediate steps to take if you\'ve been defrauded.',
        keyPoints: [
            'UPI and payment app fraud prevention',
            'Credit/debit card safety measures',
            'Identifying phishing and scam calls',
            'Reporting fraud to banks and cyber cell',
            'Freezing accounts and blocking transactions',
            'Recovery process and legal remedies'
        ],
        cta: {
            text: 'Report Fraud Now',
            link: '/chat-ui',
            icon: 'warning-outline'
        }
    },

    'topic-legal-awareness': {
        icon: 'bulb-outline',
        title: 'Legal Awareness',
        description: 'Build your understanding of basic legal concepts, court systems, and how to access justice in India.',
        keyPoints: [
            'Understanding the Indian court system',
            'How to read and understand legal documents',
            'Legal aid and free legal services',
            'Limitation periods for filing cases',
            'Alternative dispute resolution (mediation, arbitration)',
            'Your rights in civil and criminal matters'
        ],
        cta: {
            text: 'Start Learning',
            link: '/constitution',
            icon: 'school-outline'
        }
    },

    'topic-traffic-rules': {
        icon: 'car-outline',
        title: 'Traffic Rules & Motor Vehicles',
        description: 'Know your rights and responsibilities under the Motor Vehicles Act. Handle traffic violations, accidents, and insurance claims.',
        keyPoints: [
            'Traffic violation penalties and fines',
            'License suspension and revocation',
            'Accident procedures and reporting',
            'Insurance claims and compensation',
            'Hit-and-run cases',
            'Challenging traffic challans'
        ],
        cta: {
            text: 'Get Traffic Help',
            link: '/chat-ui',
            icon: 'help-circle-outline'
        }
    },

    'topic-employment': {
        icon: 'briefcase-outline',
        title: 'Employment Law',
        description: 'Understand your workplace rights under Indian labor laws. Get help with wrongful termination, salary disputes, and workplace harassment.',
        keyPoints: [
            'Employment contracts and terms',
            'Minimum wages and salary rights',
            'Wrongful termination and layoffs',
            'Workplace harassment (sexual & general)',
            'Provident Fund (PF) and gratuity rights',
            'Labor court procedures and remedies'
        ],
        cta: {
            text: 'Workplace Issue Help',
            link: '/chat-ui',
            icon: 'chatbubbles-outline'
        }
    },

    // ========================================
    // WHO IS THIS FOR SECTION (3 modals)
    // ========================================
    'audience-students': {
        icon: 'school-outline',
        title: 'For Students',
        description: 'Whether you\'re studying civics, law, or just want to be an informed citizen, LawAid X Sanvidhan is your companion for understanding Indian constitutional values.',
        keyPoints: [
            'Learn constitutional basics for exams',
            'Understand fundamental rights and duties',
            'Research projects and assignments',
            'Prepare for competitive exams (UPSC, etc.)',
            'Develop civic awareness and responsibility',
            'Free educational resource'
        ],
        cta: {
            text: 'Explore Constitution',
            link: '/constitution',
            icon: 'book-outline'
        }
    },

    'audience-citizens': {
        icon: 'business-outline',
        title: 'For Citizens',
        description: 'Every Indian deserves to know their rights. Whether you\'re facing a legal issue or just want to be informed, we\'re here to help you navigate the legal system.',
        keyPoints: [
            'Quick answers to everyday legal questions',
            'Generate legal documents (complaints, notices)',
            'Emergency legal assistance (SOS Shield)',
            'Consumer rights and protection',
            'Property and family law guidance',
            'No lawyer fees for basic information'
        ],
        cta: {
            text: 'Ask Legal Question',
            link: '/chat-ui',
            icon: 'chatbubbles-outline'
        }
    },

    'audience-ngos': {
        icon: 'people-outline',
        title: 'For NGOs & Social Workers',
        description: 'Empower the communities you serve with legal knowledge. Use our platform to educate, assist, and advocate for those who need legal help the most.',
        keyPoints: [
            'Legal education resource for communities',
            'Help beneficiaries understand their rights',
            'Generate legal documents for those in need',
            'Research legal provisions for advocacy',
            'Free tool for grassroots organizations',
            'Multilingual support for diverse communities'
        ],
        cta: {
            text: 'Start Helping Others',
            link: '/chat-ui',
            icon: 'heart-outline'
        }
    }
};

// Modal Functions
function openModal(modalId) {
    const overlay = document.getElementById('modal-overlay');
    const modalBody = document.getElementById('modal-body');

    const data = modalData[modalId];
    if (!data) {
        console.error('Modal data not found for:', modalId);
        return;
    }

    // Build modal content
    let content = `
    <h2>
      <ion-icon name="${data.icon}"></ion-icon>
      ${data.title}
    </h2>
    <p>${data.description}</p>
  `;

    if (data.keyPoints && data.keyPoints.length > 0) {
        content += '<ul>';
        data.keyPoints.forEach(point => {
            content += `<li>${point}</li>`;
        });
        content += '</ul>';
    }

    if (data.cta) {
        content += `
      <a href="${data.cta.link}" class="modal-cta">
        <ion-icon name="${data.cta.icon}"></ion-icon>
        ${data.cta.text}
      </a>
    `;
    }

    modalBody.innerHTML = content;
    overlay.classList.add('active');

    // Prevent body scroll when modal is open
    document.body.style.overflow = 'hidden';
}

function closeModal() {
    const overlay = document.getElementById('modal-overlay');
    overlay.classList.remove('active');

    // Restore body scroll
    document.body.style.overflow = '';
}

// Event Listeners
document.addEventListener('DOMContentLoaded', function () {
    const overlay = document.getElementById('modal-overlay');

    // Close on overlay click (outside modal content)
    overlay.addEventListener('click', function (e) {
        if (e.target === overlay) {
            closeModal();
        }
    });

    // Close on ESC key
    document.addEventListener('keydown', function (e) {
        if (e.key === 'Escape' && overlay.classList.contains('active')) {
            closeModal();
        }
    });
});
