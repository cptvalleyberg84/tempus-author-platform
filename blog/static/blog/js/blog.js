/**
 * Blog page functionality.
 * 
 * Implements lazy loading for blog card images beyond the first three cards
 * to improve initial page load performance.
 */

document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.blog-card:not(:nth-child(-n+3)) img');
    images.forEach(img => {
        img.setAttribute('loading', 'lazy');
    });
});