-- Insérer des catégories de test
INSERT INTO categories (name, slug, description) VALUES
('Outillage à main', 'outillage-a-main', 'Tous les outils manuels pour vos travaux'),
('Électroportatif', 'electroportatif', 'Outils électriques pour professionnels et particuliers'),
('Quincaillerie', 'quincaillerie', 'Visserie, boulonnerie et accessoires');

-- Insérer des marques de test
INSERT INTO brands (name, slug, website) VALUES
('Bosch', 'bosch', 'https://www.bosch.fr'),
('Stanley', 'stanley', 'https://www.stanleytools.com'),
('Facom', 'facom', 'https://www.facom.fr');

-- Insérer des produits de test
WITH cat AS (SELECT id FROM categories WHERE slug = 'electroportatif'),
     br AS (SELECT id FROM brands WHERE slug = 'bosch')
INSERT INTO products (
    name,
    slug,
    category_id,
    brand_id,
    description,
    price,
    stock,
    image_url
)
SELECT 
    'Perceuse Bosch GSB 18V',
    'perceuse-bosch-gsb-18v',
    cat.id,
    br.id,
    'Perceuse à percussion 18V avec 2 batteries',
    199.99,
    10,
    'https://example.com/images/perceuse-bosch.jpg'
FROM cat, br;
