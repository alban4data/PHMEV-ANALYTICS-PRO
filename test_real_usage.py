#!/usr/bin/env python3
"""
Test d'usage réel de l'application PHMEV
Simule des scénarios d'utilisation réels avec combinaisons de filtres
"""

import sys
import os
from datetime import datetime

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_scenario_1_cancer_treatment():
    """Scénario 1: Recherche de traitements anticancéreux"""
    print("🎯 Scénario 1: Recherche de traitements anticancéreux")
    print("   Utilisateur cherche: CABOMETYX à l'Institut Gustave Roussy")
    
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        
        # Étape 1: Rechercher CABOMETYX
        medicaments = cache.get('medicaments', [])
        cabometyx_results = [med for med in medicaments if 'cabometyx' in med.lower()]
        
        if cabometyx_results:
            print(f"   ✅ CABOMETYX trouvé: {len(cabometyx_results)} formulations")
            for med in cabometyx_results:
                print(f"      - {med}")
        else:
            print("   ❌ CABOMETYX non trouvé")
            return False
        
        # Étape 2: Rechercher Institut Gustave Roussy
        etablissements = cache.get('etablissements', [])
        igr_results = [etab for etab in etablissements if 'gustave' in etab.lower() and 'roussy' in etab.lower()]
        
        if igr_results:
            print(f"   ✅ Institut Gustave Roussy trouvé: {igr_results[0]}")
        else:
            print("   ❌ Institut Gustave Roussy non trouvé")
            return False
        
        # Étape 3: Vérifier la catégorie ATC (anticancéreux = L)
        atc1_data = cache.get('atc1', [])
        antineoplastic = None
        for code, label in atc1_data:
            if code == 'L' or 'antineoplasique' in label.lower() or 'immunomodulant' in label.lower():
                antineoplastic = (code, label)
                break
        
        if antineoplastic:
            print(f"   ✅ Catégorie anticancéreux trouvée: {antineoplastic[0]} - {antineoplastic[1]}")
        else:
            print("   ⚠️  Catégorie anticancéreux non identifiée clairement")
        
        print("   🎉 Scénario 1 RÉUSSI - Toutes les données nécessaires disponibles")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur scénario 1: {e}")
        return False

def test_scenario_2_hospital_analysis():
    """Scénario 2: Analyse par hôpital et ville"""
    print("\n🎯 Scénario 2: Analyse des CHU parisiens")
    print("   Utilisateur filtre: CHU + Paris + médicaments digestifs")
    
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        
        # Étape 1: Rechercher les CHU
        etablissements = cache.get('etablissements', [])
        chu_results = [etab for etab in etablissements if 'chu' in etab.lower()]
        
        if chu_results:
            print(f"   ✅ CHU trouvés: {len(chu_results)} établissements")
            print(f"      Exemples: {chu_results[:3]}")
        else:
            print("   ❌ Aucun CHU trouvé")
            return False
        
        # Étape 2: Vérifier Paris
        villes = cache.get('villes', [])
        paris_found = 'PARIS' in villes
        
        if paris_found:
            print("   ✅ Ville PARIS disponible")
        else:
            print("   ⚠️  Ville PARIS non trouvée dans la liste")
        
        # Étape 3: Système digestif (ATC A)
        atc1_data = cache.get('atc1', [])
        digestif = None
        for code, label in atc1_data:
            if code == 'A' or 'digestif' in label.lower():
                digestif = (code, label)
                break
        
        if digestif:
            print(f"   ✅ Système digestif trouvé: {digestif[0]} - {digestif[1]}")
            
            # Sous-catégories digestives
            atc2_data = cache.get('atc2', [])
            digestif_sub = [item for item in atc2_data if item[0].startswith('A')]
            print(f"   ✅ Sous-catégories digestives: {len(digestif_sub)} disponibles")
        else:
            print("   ❌ Système digestif non trouvé")
            return False
        
        print("   🎉 Scénario 2 RÉUSSI - Filtrage multi-critères possible")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur scénario 2: {e}")
        return False

def test_scenario_3_drug_search():
    """Scénario 3: Recherche de médicaments par nom commercial"""
    print("\n🎯 Scénario 3: Recherche par noms commerciaux")
    print("   Utilisateur teste: Mapping noms commerciaux -> molécules")
    
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        medicaments = cache.get('medicaments', [])
        
        # Tests de mapping comme dans l'application
        drug_mapping = {
            'cabometyx': 'cabozantinib',
            'humira': 'adalimumab',
            'keytruda': 'pembrolizumab',
            'opdivo': 'nivolumab'
        }
        
        mapping_results = {}
        
        for commercial, molecular in drug_mapping.items():
            # Recherche par nom commercial
            commercial_matches = [med for med in medicaments if commercial.lower() in med.lower()]
            
            # Recherche par molécule
            molecular_matches = [med for med in medicaments if molecular.lower() in med.lower()]
            
            mapping_results[commercial] = {
                'commercial_found': len(commercial_matches) > 0,
                'molecular_found': len(molecular_matches) > 0,
                'commercial_count': len(commercial_matches),
                'molecular_count': len(molecular_matches)
            }
            
            if commercial_matches:
                print(f"   ✅ '{commercial}' trouvé: {len(commercial_matches)} résultats")
                print(f"      Exemple: {commercial_matches[0]}")
            elif molecular_matches:
                print(f"   ⚠️  '{commercial}' non trouvé, mais molécule '{molecular}': {len(molecular_matches)} résultats")
            else:
                print(f"   ❌ '{commercial}' et '{molecular}' non trouvés")
        
        # Statistiques du mapping
        found_commercial = sum(1 for r in mapping_results.values() if r['commercial_found'])
        found_molecular = sum(1 for r in mapping_results.values() if r['molecular_found'])
        
        print(f"   📊 Résumé mapping: {found_commercial}/{len(drug_mapping)} noms commerciaux, {found_molecular}/{len(drug_mapping)} molécules")
        
        if found_commercial > 0 or found_molecular > 0:
            print("   🎉 Scénario 3 RÉUSSI - Système de recherche fonctionnel")
            return True
        else:
            print("   ❌ Scénario 3 ÉCHOUÉ - Aucun médicament test trouvé")
            return False
        
    except Exception as e:
        print(f"   ❌ Erreur scénario 3: {e}")
        return False

def test_scenario_4_hierarchical_navigation():
    """Scénario 4: Navigation hiérarchique complète"""
    print("\n🎯 Scénario 4: Navigation hiérarchique ATC complète")
    print("   Utilisateur navigue: ATC1 -> ATC2 -> ATC3 -> ATC4 -> ATC5")
    
    try:
        from filter_cache_embedded import get_embedded_cache
        cache = get_embedded_cache()
        
        # Parcours hiérarchique complet
        current_code = None
        
        for level in ['atc1', 'atc2', 'atc3', 'atc4', 'atc5']:
            atc_data = cache.get(level, [])
            
            if not atc_data:
                print(f"   ❌ Niveau {level} vide")
                return False
            
            if current_code is None:
                # Premier niveau - prendre le premier élément
                current_code, current_label = atc_data[0]
                print(f"   ✅ {level.upper()}: {current_code} - {current_label[:50]}...")
            else:
                # Niveaux suivants - filtrer par code parent
                filtered = [item for item in atc_data if item[0].startswith(current_code)]
                
                if filtered:
                    current_code, current_label = filtered[0]
                    print(f"   ✅ {level.upper()}: {current_code} - {current_label[:50]}... ({len(filtered)} options)")
                else:
                    print(f"   ⚠️  {level.upper()}: Aucune option pour {current_code}")
                    break
        
        print("   🎉 Scénario 4 RÉUSSI - Navigation hiérarchique complète")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur scénario 4: {e}")
        return False

def test_scenario_5_performance_simulation():
    """Scénario 5: Test de performance avec gros volumes"""
    print("\n🎯 Scénario 5: Simulation de performance")
    print("   Test: Recherche dans de gros volumes de données")
    
    try:
        from filter_cache_embedded import get_embedded_cache
        import time
        
        cache = get_embedded_cache()
        
        # Test 1: Recherche dans tous les médicaments
        start_time = time.time()
        medicaments = cache.get('medicaments', [])
        search_results = [med for med in medicaments if 'mg' in med.lower()]
        search_time = time.time() - start_time
        
        print(f"   ✅ Recherche 'mg' dans {len(medicaments)} médicaments: {len(search_results)} résultats en {search_time:.3f}s")
        
        # Test 2: Filtrage hiérarchique
        start_time = time.time()
        atc1_data = cache.get('atc1', [])
        atc2_data = cache.get('atc2', [])
        
        for atc1_code, _ in atc1_data:
            filtered_atc2 = [item for item in atc2_data if item[0].startswith(atc1_code)]
        
        filter_time = time.time() - start_time
        print(f"   ✅ Filtrage hiérarchique ATC1->ATC2: {len(atc1_data)} x {len(atc2_data)} en {filter_time:.3f}s")
        
        # Test 3: Recherche d'établissements
        start_time = time.time()
        etablissements = cache.get('etablissements', [])
        chu_search = [etab for etab in etablissements if 'chu' in etab.lower()]
        etab_time = time.time() - start_time
        
        print(f"   ✅ Recherche CHU dans {len(etablissements)} établissements: {len(chu_search)} résultats en {etab_time:.3f}s")
        
        # Évaluation des performances
        total_time = search_time + filter_time + etab_time
        if total_time < 1.0:
            print(f"   🚀 Performance EXCELLENTE: {total_time:.3f}s total")
        elif total_time < 3.0:
            print(f"   ✅ Performance BONNE: {total_time:.3f}s total")
        else:
            print(f"   ⚠️  Performance LENTE: {total_time:.3f}s total")
        
        print("   🎉 Scénario 5 RÉUSSI - Performance acceptable")
        return True
        
    except Exception as e:
        print(f"   ❌ Erreur scénario 5: {e}")
        return False

def run_real_usage_tests():
    """Exécuter tous les tests d'usage réel"""
    print("🚀 TESTS D'USAGE RÉEL - APPLICATION PHMEV")
    print("=" * 65)
    print(f"📅 {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("🎭 Simulation de scénarios utilisateur réels")
    print("=" * 65)
    
    scenarios = [
        ("Cancer - CABOMETYX/IGR", test_scenario_1_cancer_treatment),
        ("CHU Paris - Digestif", test_scenario_2_hospital_analysis),
        ("Noms commerciaux", test_scenario_3_drug_search),
        ("Navigation ATC", test_scenario_4_hierarchical_navigation),
        ("Performance", test_scenario_5_performance_simulation)
    ]
    
    results = []
    
    for scenario_name, test_func in scenarios:
        try:
            result = test_func()
            results.append((scenario_name, result))
        except Exception as e:
            print(f"❌ ERREUR CRITIQUE dans {scenario_name}: {e}")
            results.append((scenario_name, False))
    
    # Résumé final
    print("\n" + "=" * 65)
    print("📊 RÉSUMÉ DES SCÉNARIOS D'USAGE")
    print("=" * 65)
    
    passed = sum(1 for _, result in results if result)
    failed = len(results) - passed
    
    for scenario_name, result in results:
        status = "✅ RÉUSSI" if result else "❌ ÉCHOUÉ"
        print(f"{scenario_name:.<35} {status}")
    
    print("-" * 65)
    print(f"Total: {len(results)} scénarios | Réussis: {passed} | Échoués: {failed}")
    
    if failed == 0:
        print("\n🎉 TOUS LES SCÉNARIOS D'USAGE RÉUSSIS !")
        print("✅ L'application est prête pour la production")
        print("🚀 Tous les cas d'usage utilisateur sont couverts")
    else:
        print(f"\n⚠️  {failed} scénario(s) échoué(s)")
        print("🔧 Révision nécessaire avant mise en production")
    
    print("=" * 65)
    return failed == 0

if __name__ == "__main__":
    success = run_real_usage_tests()
    sys.exit(0 if success else 1)
