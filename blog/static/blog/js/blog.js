document.addEventListener('DOMContentLoaded', function() {
    const images = document.querySelectorAll('.blog-card:not(:nth-child(-n+3)) img');
    images.forEach(img => {
        img.setAttribute('loading', 'lazy');
    });
});