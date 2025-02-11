/**
 * Back to Top button functionality.
 * 
 * Features:
 * - Shows button when user scrolls past 300px
 * - Hides button when user is near the top
 * - Smooth scrolling animation when clicked
 * - Uses Bootstrap classes for visibility toggling
 */

document.addEventListener('DOMContentLoaded', function() {
    const backToTopBtn = document.getElementById('back-to-top');
    
    // Show/hide button using Bootstrap classes
    window.addEventListener('scroll', function() {
        if (window.scrollY > 300) {
            backToTopBtn.classList.remove('d-none');
            backToTopBtn.classList.add('d-block');
        } else {
            backToTopBtn.classList.remove('d-block');
            backToTopBtn.classList.add('d-none');
        }
    });

    // Smooth scroll using Bootstrap's data-bs-scroll
    backToTopBtn.addEventListener('click', function(e) {
        e.preventDefault();
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
});