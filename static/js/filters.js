// Gestion des filtres de produits
document.addEventListener('DOMContentLoaded', function() {
    // Initialisation du slider de prix
    const priceRange = document.getElementById('priceRange');
    if (priceRange) {
        noUiSlider.create(priceRange, {
            start: [0, 1000],
            connect: true,
            range: {
                'min': 0,
                'max': 1000
            }
        });

        // Mise à jour des valeurs affichées
        priceRange.noUiSlider.on('update', function(values, handle) {
            document.getElementById('minPrice').textContent = Math.round(values[0]) + '€';
            document.getElementById('maxPrice').textContent = Math.round(values[1]) + '€';
        });
    }

    // Gestion des filtres de catégories
    const categoryFilters = document.querySelectorAll('.category-filter');
    categoryFilters.forEach(filter => {
        filter.addEventListener('change', updateFilters);
    });

    // Gestion des filtres de marques
    const brandFilters = document.querySelectorAll('.brand-filter');
    brandFilters.forEach(filter => {
        filter.addEventListener('change', updateFilters);
    });
});

function updateFilters() {
    const selectedCategories = Array.from(document.querySelectorAll('.category-filter:checked'))
        .map(el => el.value);
    const selectedBrands = Array.from(document.querySelectorAll('.brand-filter:checked'))
        .map(el => el.value);
    const priceRange = document.getElementById('priceRange');
    const prices = priceRange ? priceRange.noUiSlider.get() : [0, 1000];

    // Construire l'URL avec les paramètres
    const params = new URLSearchParams();
    if (selectedCategories.length) params.append('categories', selectedCategories.join(','));
    if (selectedBrands.length) params.append('brands', selectedBrands.join(','));
    params.append('min_price', Math.round(prices[0]));
    params.append('max_price', Math.round(prices[1]));

    // Recharger la page avec les filtres
    window.location.href = `${window.location.pathname}?${params.toString()}`;
}
