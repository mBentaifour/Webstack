import unittest
import sys
import os
import argparse
from dotenv import load_dotenv
import time

# Charger les variables d'environnement
load_dotenv()

def run_tests(test_type=None, verbose=True):
    """Exécuter les tests
    
    Args:
        test_type (str): Type de tests à exécuter ('api', 'auth', 'perf', 'valid', 'edge', ou None pour tous)
        verbose (bool): Si True, affiche les détails des tests
    """
    # Configuration du test loader
    loader = unittest.TestLoader()
    suite = unittest.TestSuite()
    
    # Répertoire des tests
    start_dir = os.path.join(os.path.dirname(__file__), 'tests')
    
    # Sélection des tests à exécuter
    if test_type == 'api':
        pattern = 'test_products_api.py'
    elif test_type == 'auth':
        pattern = 'test_auth.py'
    elif test_type == 'perf':
        pattern = 'test_performance.py'
    elif test_type == 'valid':
        pattern = 'test_validation.py'
    elif test_type == 'edge':
        pattern = 'test_edge_cases.py'
    else:
        pattern = 'test_*.py'
    
    # Découvrir et charger les tests
    suite = loader.discover(start_dir, pattern=pattern)
    
    # Configuration du runner
    verbosity = 2 if verbose else 1
    runner = unittest.TextTestRunner(verbosity=verbosity)
    
    # Exécuter les tests
    print(f"\nExécution des tests{f' ({test_type})' if test_type else ''}...")
    start_time = time.time()
    result = runner.run(suite)
    end_time = time.time()
    
    # Afficher le résumé
    print(f"\nRésumé des tests:")
    print(f"Temps total: {end_time - start_time:.2f} secondes")
    print(f"Tests exécutés: {result.testsRun}")
    print(f"Succès: {result.testsRun - len(result.failures) - len(result.errors)}")
    print(f"Échecs: {len(result.failures)}")
    print(f"Erreurs: {len(result.errors)}")
    
    return 0 if result.wasSuccessful() else 1

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Exécuter les tests du projet')
    parser.add_argument('--type', choices=['api', 'auth', 'perf', 'valid', 'edge'],
                      help='Type de tests à exécuter')
    parser.add_argument('--quiet', action='store_true',
                      help='Réduire la verbosité des tests')
    
    args = parser.parse_args()
    sys.exit(run_tests(args.type, not args.quiet))
