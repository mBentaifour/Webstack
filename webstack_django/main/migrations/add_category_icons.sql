-- Ajouter la colonne icon_class
ALTER TABLE categories ADD COLUMN IF NOT EXISTS icon_class text;

-- Mettre à jour les catégories existantes avec des icônes par défaut
UPDATE categories SET icon_class = 
    CASE 
        WHEN name ILIKE '%outillage%' THEN 'fas fa-tools'
        WHEN name ILIKE '%peinture%' THEN 'fas fa-paint-roller'
        WHEN name ILIKE '%jardin%' THEN 'fas fa-leaf'
        WHEN name ILIKE '%électricité%' THEN 'fas fa-bolt'
        WHEN name ILIKE '%plomberie%' THEN 'fas fa-faucet'
        WHEN name ILIKE '%quincaillerie%' THEN 'fas fa-screwdriver'
        WHEN name ILIKE '%bois%' THEN 'fas fa-tree'
        WHEN name ILIKE '%construction%' THEN 'fas fa-hard-hat'
        WHEN name ILIKE '%nettoyage%' THEN 'fas fa-broom'
        WHEN name ILIKE '%sécurité%' THEN 'fas fa-shield-alt'
        ELSE 'fas fa-box'
    END
WHERE icon_class IS NULL;
