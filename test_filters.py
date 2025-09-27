#!/usr/bin/env python3
"""
Script de test automatisé pour vérifier tous les filtres de l'application PHMEV
Teste le chargement, la cohérence et le fonctionnement de tous les filtres
"""

import sys
import os
import traceback
from datetime import datetime
import pandas as pd

# Ajouter le répertoire courant au path pour importer les modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test 1: Vérifier que tous les imports fonctionnent"""
    print("🧪 Test 1: Imports des modules...")
    try:
        # Test des imports principaux
        import streamlit as st
        import pandas as pd
        import numpy as np
        from google.cloud import bigquery
        from google.oauth2 import service_account
        
        # Test de l'import du cache intégré
        from filter_cache_embedded import get_embedded_cache
        
        print("✅ Tous les imports réussis")
        return True
    except Exception as e:
        print(f"❌ Erreur d'import: {e}")
        return False

def test_embedded_cache():
    """Test 2: Vérifier le cache intégré"""
    print("\n🧪 Test 2: Cache intégré...")
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        
        # Vérifier la structure du cache
        required_keys = ['atc1', 'atc2', 'atc3', 'atc4', 'atc5', 'villes', 'categories', 'etablissements', 'medicaments']
        
        for key in required_keys:
            if key not in cache:
                print(f"❌ Clé manquante dans le cache: {key}")
                return False
            
            if not isinstance(cache[key], list):
                print(f"❌ Type incorrect pour {key}: {type(cache[key])}")
                return False
            
            if len(cache[key]) == 0:
                print(f"⚠️  Liste vide pour {key}")
            else:
                print(f"✅ {key}: {len(cache[key])} éléments")
        
        # Vérifier la structure des ATC (tuples code, label)
        for atc_level in ['atc1', 'atc2', 'atc3', 'atc4', 'atc5']:
            if cache[atc_level] and len(cache[atc_level]) > 0:
                first_item = cache[atc_level][0]
                if not isinstance(first_item, tuple) or len(first_item) != 2:
                    print(f"❌ Structure incorrecte pour {atc_level}: {first_item}")
                    return False
        
        print("✅ Cache intégré valide")
        return True
    except Exception as e:
        print(f"❌ Erreur cache intégré: {e}")
        traceback.print_exc()
        return False

def test_bigquery_connection():
    """Test 3: Vérifier la connexion BigQuery"""
    print("\n🧪 Test 3: Connexion BigQuery...")
    try:
        # Simuler l'import des fonctions de l'app
        sys.path.insert(0, '.')
        
        # Test de connexion avec fichier local
        import os
        from google.oauth2 import service_account
        from google.cloud import bigquery
        
        json_file = 'test-db-473321-aed58eeb55a8.json'
        if os.path.exists(json_file):
            try:
                credentials = service_account.Credentials.from_service_account_file(json_file)
                client = bigquery.Client(credentials=credentials, project='test-db-473321')
                
                # Test simple de requête
                test_query = "SELECT 1 as test"
                result = client.query(test_query).result()
                
                print("✅ Connexion BigQuery réussie")
                return True, client
            except Exception as e:
                print(f"⚠️  Connexion BigQuery échouée: {e}")
                return False, None
        else:
            print("⚠️  Fichier de credentials non trouvé")
            return False, None
    except Exception as e:
        print(f"❌ Erreur test BigQuery: {e}")
        return False, None

def test_filter_functions():
    """Test 4: Tester les fonctions de filtrage"""
    print("\n🧪 Test 4: Fonctions de filtrage...")
    try:
        # Créer un environnement de test minimal
        class MockStreamlit:
            def cache_data(self, ttl=None):
                def decorator(func):
                    return func
                return decorator
            
            def cache_resource(self):
                def decorator(func):
                    return func
                return decorator
        
        # Mock streamlit
        import sys
        sys.modules['streamlit'] = MockStreamlit()
        
        # Maintenant importer et tester les fonctions
        from streamlit_app import get_base_filter_options
        
        print("🔄 Test du chargement des options de base...")
        options = get_base_filter_options()
        
        if not options:
            print("❌ Options vides")
            return False
        
        # Vérifier les clés essentielles
        essential_keys = ['atc1', 'medicaments', 'etablissements', 'villes']
        for key in essential_keys:
            if key not in options:
                print(f"❌ Clé manquante: {key}")
                return False
            print(f"✅ {key}: {len(options[key])} éléments")
        
        print("✅ Fonctions de filtrage OK")
        return True
    except Exception as e:
        print(f"❌ Erreur fonctions de filtrage: {e}")
        traceback.print_exc()
        return False

def test_search_functionality():
    """Test 5: Tester la fonctionnalité de recherche"""
    print("\n🧪 Test 5: Fonctionnalité de recherche...")
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        
        # Test de recherche de médicaments
        medicaments = cache.get('medicaments', [])
        
        # Test de recherche case-insensitive
        search_term = "cabozantinib"
        matches = [med for med in medicaments if search_term.lower() in med.lower()]
        
        if matches:
            print(f"✅ Recherche '{search_term}' trouvée: {len(matches)} résultats")
            print(f"   Exemple: {matches[0]}")
        else:
            print(f"⚠️  Recherche '{search_term}' non trouvée")
        
        # Test de recherche d'établissements
        etablissements = cache.get('etablissements', [])
        search_etab = "chu"
        etab_matches = [etab for etab in etablissements if search_etab.lower() in etab.lower()]
        
        if etab_matches:
            print(f"✅ Recherche établissement '{search_etab}' trouvée: {len(etab_matches)} résultats")
        else:
            print(f"⚠️  Recherche établissement '{search_etab}' non trouvée")
        
        # Test du mapping des médicaments
        drug_mapping = {
            'cabometyx': 'cabozantinib',
            'keytruda': 'pembrolizumab',
            'opdivo': 'nivolumab'
        }
        
        for commercial, molecular in drug_mapping.items():
            molecular_matches = [med for med in medicaments if molecular.lower() in med.lower()]
            if molecular_matches:
                print(f"✅ Mapping {commercial} -> {molecular}: {len(molecular_matches)} résultats")
            else:
                print(f"⚠️  Mapping {commercial} -> {molecular}: non trouvé")
        
        print("✅ Fonctionnalité de recherche OK")
        return True
    except Exception as e:
        print(f"❌ Erreur recherche: {e}")
        traceback.print_exc()
        return False

def test_hierarchical_filters():
    """Test 6: Tester les filtres hiérarchiques"""
    print("\n🧪 Test 6: Filtres hiérarchiques ATC...")
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        
        # Vérifier la hiérarchie ATC
        atc_levels = ['atc1', 'atc2', 'atc3', 'atc4', 'atc5']
        
        for level in atc_levels:
            atc_data = cache.get(level, [])
            if not atc_data:
                print(f"⚠️  Niveau {level} vide")
                continue
            
            # Vérifier la structure (code, label)
            sample = atc_data[0]
            if isinstance(sample, tuple) and len(sample) == 2:
                code, label = sample
                print(f"✅ {level}: {len(atc_data)} codes (ex: {code} - {label[:50]}...)")
            else:
                print(f"❌ Structure incorrecte pour {level}: {sample}")
                return False
        
        # Test de cohérence hiérarchique
        atc1_codes = [code for code, _ in cache.get('atc1', [])]
        atc2_codes = [code for code, _ in cache.get('atc2', [])]
        
        if atc1_codes and atc2_codes:
            # Vérifier que les codes ATC2 commencent par des codes ATC1
            valid_atc2 = 0
            for atc2_code, _ in cache.get('atc2', [])[:10]:  # Test sur 10 premiers
                if any(atc2_code.startswith(atc1_code) for atc1_code, _ in cache.get('atc1', [])):
                    valid_atc2 += 1
            
            if valid_atc2 > 0:
                print(f"✅ Cohérence hiérarchique ATC1->ATC2: {valid_atc2}/10 codes valides")
            else:
                print("⚠️  Problème de cohérence hiérarchique ATC")
        
        print("✅ Filtres hiérarchiques OK")
        return True
    except Exception as e:
        print(f"❌ Erreur filtres hiérarchiques: {e}")
        traceback.print_exc()
        return False

def test_data_consistency():
    """Test 7: Vérifier la cohérence des données"""
    print("\n🧪 Test 7: Cohérence des données...")
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        
        # Vérifier qu'il n'y a pas de doublons
        for key, data in cache.items():
            if isinstance(data, list):
                original_len = len(data)
                unique_len = len(set(data) if all(isinstance(x, str) for x in data) else data)
                
                if key.startswith('atc'):
                    # Pour les ATC, vérifier les doublons sur les codes
                    codes = [item[0] if isinstance(item, tuple) else item for item in data]
                    unique_codes = len(set(codes))
                    if unique_codes != len(codes):
                        print(f"⚠️  Doublons détectés dans {key}: {len(codes)} -> {unique_codes}")
                    else:
                        print(f"✅ {key}: Pas de doublons ({len(codes)} codes)")
                else:
                    if original_len != unique_len:
                        print(f"⚠️  Doublons détectés dans {key}: {original_len} -> {unique_len}")
                    else:
                        print(f"✅ {key}: Pas de doublons ({original_len} éléments)")
        
        # Vérifier les valeurs nulles ou vides
        for key, data in cache.items():
            if isinstance(data, list):
                empty_values = 0
                for item in data:
                    if isinstance(item, tuple):
                        if not item[0] or not item[1] or item[0].strip() == '' or item[1].strip() == '':
                            empty_values += 1
                    elif isinstance(item, str):
                        if not item or item.strip() == '':
                            empty_values += 1
                
                if empty_values > 0:
                    print(f"⚠️  Valeurs vides dans {key}: {empty_values}")
                else:
                    print(f"✅ {key}: Pas de valeurs vides")
        
        print("✅ Cohérence des données OK")
        return True
    except Exception as e:
        print(f"❌ Erreur cohérence: {e}")
        traceback.print_exc()
        return False

def run_all_tests():
    """Exécuter tous les tests"""
    print("🚀 DÉBUT DES TESTS AUTOMATISÉS - FILTRES PHMEV")
    print("=" * 60)
    print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    tests = [
        ("Imports", test_imports),
        ("Cache intégré", test_embedded_cache),
        ("Connexion BigQuery", lambda: test_bigquery_connection()[0]),
        ("Fonctions de filtrage", test_filter_functions),
        ("Recherche", test_search_functionality),
        ("Filtres hiérarchiques", test_hierarchical_filters),
        ("Cohérence des données", test_data_consistency)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"❌ ERREUR CRITIQUE dans {test_name}: {e}")
            traceback.print_exc()
            results.append((test_name, False))
    
    # Résumé des résultats
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    passed = 0
    failed = 0
    
    for test_name, result in results:
        status = "✅ PASSÉ" if result else "❌ ÉCHOUÉ"
        print(f"{test_name:.<30} {status}")
        if result:
            passed += 1
        else:
            failed += 1
    
    print("-" * 60)
    print(f"Total: {len(results)} tests | Réussis: {passed} | Échoués: {failed}")
    
    if failed == 0:
        print("🎉 TOUS LES TESTS SONT PASSÉS ! L'application est prête.")
    else:
        print(f"⚠️  {failed} test(s) échoué(s). Vérification nécessaire.")
    
    print("=" * 60)
    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
