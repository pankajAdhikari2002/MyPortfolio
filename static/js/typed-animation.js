function initTyped() {
    try {
        const typed = new Typed('.typed-text', {
            strings: ['Web Developer', 'Cybersecurity Enthusiast', 'Python Fanatic', 'Crypto Follower'],
            typeSpeed: 40,
            backSpeed: 25,
            backDelay: 1500,
            startDelay: 500,
            loop: true,
            showCursor: true,
            cursorChar: '|',
            autoInsertCss: true,
            fadeOut: true,
            fadeOutClass: 'typed-fade-out',
            fadeOutDelay: 500,
            onStringTyped: function(arrayPos, self) {
                // Add a small pause between strings
                setTimeout(() => {
                    self.stopNum = 0;
                }, 100);
            }
        });
    } catch (error) {
        console.error('Error initializing Typed.js:', error);
    }
}

// Try multiple ways to ensure the script runs
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initTyped);
} else {
    initTyped();
} 