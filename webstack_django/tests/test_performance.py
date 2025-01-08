import unittest
import requests
import time
import statistics
import concurrent.futures
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

class TestPerformance(unittest.TestCase):
    """Tests de performance de l'API"""
    
    @classmethod
    def setUpClass(cls):
        """Configuration initiale pour tous les tests"""
        cls.BASE_URL = "http://localhost:8000/api"
        cls.PERFORMANCE_THRESHOLD = 1.0  # Seuil de performance en secondes
        
    def measure_response_time(self, url, method='get', data=None, iterations=5):
        """Mesure le temps de réponse moyen sur plusieurs itérations"""
        times = []
        for _ in range(iterations):
            start_time = time.time()
            if method.lower() == 'get':
                response = requests.get(url)
            elif method.lower() == 'post':
                response = requests.post(url, json=data)
            
            end_time = time.time()
            if response.status_code in [200, 201]:
                times.append(end_time - start_time)
            time.sleep(0.1)  # Petit délai entre les requêtes
            
        return {
            'min': min(times),
            'max': max(times),
            'avg': statistics.mean(times),
            'median': statistics.median(times)
        }
    
    def test_01_list_products_performance(self):
        """Test: Performance de la liste des produits"""
        url = f"{self.BASE_URL}/products/"
        metrics = self.measure_response_time(url)
        
        print(f"\nPerformance GET /products/:")
        print(f"Min: {metrics['min']:.3f}s")
        print(f"Max: {metrics['max']:.3f}s")
        print(f"Avg: {metrics['avg']:.3f}s")
        print(f"Median: {metrics['median']:.3f}s")
        
        self.assertLess(metrics['avg'], self.PERFORMANCE_THRESHOLD)
    
    def test_02_search_performance(self):
        """Test: Performance de la recherche"""
        url = f"{self.BASE_URL}/products/search/"
        data = {"search": "test"}
        metrics = self.measure_response_time(url, method='post', data=data)
        
        print(f"\nPerformance POST /products/search/:")
        print(f"Min: {metrics['min']:.3f}s")
        print(f"Max: {metrics['max']:.3f}s")
        print(f"Avg: {metrics['avg']:.3f}s")
        print(f"Median: {metrics['median']:.3f}s")
        
        self.assertLess(metrics['avg'], self.PERFORMANCE_THRESHOLD)
    
    def test_03_concurrent_requests(self):
        """Test: Performance sous charge concurrente"""
        url = f"{self.BASE_URL}/products/"
        num_concurrent = 10
        num_requests = 5
        
        def make_request():
            times = []
            for _ in range(num_requests):
                start_time = time.time()
                response = requests.get(url)
                end_time = time.time()
                if response.status_code == 200:
                    times.append(end_time - start_time)
                time.sleep(0.1)
            return times
        
        all_times = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = [executor.submit(make_request) for _ in range(num_concurrent)]
            for future in concurrent.futures.as_completed(futures):
                all_times.extend(future.result())
        
        metrics = {
            'min': min(all_times),
            'max': max(all_times),
            'avg': statistics.mean(all_times),
            'median': statistics.median(all_times)
        }
        
        print(f"\nPerformance sous charge concurrente ({num_concurrent} clients):")
        print(f"Min: {metrics['min']:.3f}s")
        print(f"Max: {metrics['max']:.3f}s")
        print(f"Avg: {metrics['avg']:.3f}s")
        print(f"Median: {metrics['median']:.3f}s")
        
        self.assertLess(metrics['avg'], self.PERFORMANCE_THRESHOLD * 2)
    
    def test_04_database_performance(self):
        """Test: Performance des opérations de base de données"""
        # Test de création rapide
        url = f"{self.BASE_URL}/products/"
        test_product = {
            "name": "Performance Test Product",
            "slug": "performance-test-product",
            "description": "Test product for performance testing",
            "price": 99.99,
            "stock": 100,
            "category_id": "29bf495e-eb1c-43b1-b753-80a937129628"
        }
        
        metrics = self.measure_response_time(url, method='post', data=test_product)
        
        print(f"\nPerformance création produit:")
        print(f"Min: {metrics['min']:.3f}s")
        print(f"Max: {metrics['max']:.3f}s")
        print(f"Avg: {metrics['avg']:.3f}s")
        print(f"Median: {metrics['median']:.3f}s")
        
        self.assertLess(metrics['avg'], self.PERFORMANCE_THRESHOLD)

if __name__ == '__main__':
    unittest.main(verbosity=2)
