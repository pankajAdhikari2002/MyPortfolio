document.addEventListener('DOMContentLoaded', function() {
    // Get all sections
    const sections = document.querySelectorAll('section[id], header[id]');
    
    // Get all nav links
    const navLinks = document.querySelectorAll('.nav-link');
    
    // Function to update active state
    function updateActiveState() {
        let currentSection = '';
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.scrollY >= sectionTop - 150) {
                currentSection = section.getAttribute('id');
            }
        });
        
        // Remove active class from all links
        navLinks.forEach(link => {
            link.classList.remove('active');
        });
        
        // Add active class to current section's link
        if (currentSection) {
            document.querySelector(`.nav-link[href="#${currentSection}"]`).classList.add('active');
        }
    }
    
    // Update active state on scroll
    window.addEventListener('scroll', updateActiveState);
    
    // Update active state on page load
    updateActiveState();
}); 