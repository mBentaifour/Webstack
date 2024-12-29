// Navigation.js
document.addEventListener('DOMContentLoaded', function() {
    // Gestion du menu mobile
    const navbarToggler = document.querySelector('.navbar-toggler');
    const navbarCollapse = document.querySelector('.navbar-collapse');

    if (navbarToggler && navbarCollapse) {
        navbarToggler.addEventListener('click', function() {
            navbarCollapse.classList.toggle('show');
        });
    }

    // Gestion de la barre de recherche
    const searchForm = document.querySelector('.search-form');
    if (searchForm) {
        searchForm.addEventListener('submit', function(e) {
            const searchInput = searchForm.querySelector('input[type="search"]');
            if (!searchInput.value.trim()) {
                e.preventDefault();
            }
        });
    }

    // Animation du menu actif
    const currentPath = window.location.pathname;
    document.querySelectorAll('.nav-link').forEach(link => {
        if (link.getAttribute('href') === currentPath) {
            link.classList.add('active');
        }
    });
});
