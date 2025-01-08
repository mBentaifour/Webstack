import unittest
import sys
import os
import logging
import django
from dotenv import load_dotenv

# Ajouter le répertoire parent au PYTHONPATH
parent_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, parent_dir)

# Configurer Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'webstack_django.settings')
django.setup()

# Charger les variables d'environnement
load_dotenv()

# Configuration du logging pour les tests
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def run_tests():
    """Exécute tous les tests et retourne True si tous les tests passent"""
    # Découverte automatique des tests
    loader = unittest.TestLoader()
    start_dir = os.path.dirname(os.path.abspath(__file__))
    suite = loader.discover(start_dir, pattern="test_*.py")

    # Configuration du runner
    runner = unittest.TextTestRunner(verbosity=2)
    
    print("\n=== Démarrage des tests ===\n")
    
    # Exécution des tests
    result = runner.run(suite)
    
    # Affichage du résumé
    print("\n=== Résumé des tests ===")
    print(f"Tests exécutés : {result.testsRun}")
    print(f"Tests réussis  : {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs        : {len(result.failures)}")
    print(f"Erreurs       : {len(result.errors)}")
    
    # Retourner True si tous les tests passent
    return len(result.failures) == 0 and len(result.errors) == 0

if __name__ == '__main__':
    # Ajouter le répertoire des tests au PYTHONPATH
    tests_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, tests_dir)
    
    success = run_tests()
    # Utiliser le code de retour approprié
    sys.exit(0 if success else 1)
