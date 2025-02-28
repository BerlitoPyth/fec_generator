# Guide de Migration vers l'Architecture Modulaire

Ce guide explique comment migrer du fichier monolithique `fec_generator_complet.py` vers la nouvelle architecture modulaire.

## Étapes de migration

### 1. Créer la structure de répertoires

Commencez par créer la structure de répertoires suivante :

```
fec_generator/
├── __init__.py
├── main.py
├── generator.py
├── models/
│   ├── __init__.py
│   ├── accounting_data.py
│   └── transaction.py
├── utils/
│   ├── __init__.py
│   ├── formatters.py
│   ├── validators.py
│   └── anomalies.py
└── exporters/
    ├── __init__.py
    ├── csv_exporter.py
    └── excel_exporter.py
```

### 2. Copier les fichiers

Copiez tous les fichiers créés dans leurs emplacements respectifs.

### 3. Installer les dépendances

Assurez-vous que toutes les dépendances sont installées :

```bash
pip install pandas numpy faker openpyxl
```

### 4. Tester l'installation

Pour vérifier que tout fonctionne correctement, vous pouvez exécuter un test simple :

```python
from fec_generator import FECGenerator

# Créer un générateur
generator = FECGenerator(transaction_count=10)

# Générer et exporter
generator.generate_transactions()
generator.export_to_csv("test_fec.csv")
```

## Principales modifications

### Séparation des responsabilités

- **Models** : Contient les structures de données et leur logique associée
- **Utils** : Fonctions utilitaires pour le formatage, la validation et les anomalies
- **Exporters** : Gestion des exports aux différents formats
- **Generator** : Classe principale qui orchestre les autres composants

### Changements d'API

La plupart des méthodes ont conservé la même signature, avec quelques ajustements :

- Les méthodes statiques ont été déplacées dans des classes dédiées
- Les importations doivent être mises à jour pour refléter la nouvelle structure
- L'usage en ligne de commande est maintenant géré par `main.py`

### Avantages de la nouvelle architecture

- **Maintenance plus facile** : Chaque composant a une responsabilité unique
- **Tests simplifiés** : Possibilité de tester chaque module individuellement
- **Réutilisation** : Les composants peuvent être réutilisés dans d'autres projets
- **Évolutivité** : Ajout de nouvelles fonctionnalités sans modifier le code existant

## Conseils pour les modifications futures

### Pour ajouter un nouveau format d'export

1. Créer un nouveau fichier dans le dossier `exporters/`
2. Ajouter l'import dans `exporters/__init__.py`
3. Ajouter une méthode à `FECGenerator` dans `generator.py`
4. Mettre à jour `main.py` pour supporter le nouveau format en ligne de commande

### Pour ajouter de nouveaux types d'anomalies

1. Modifier la fonction `inject_anomalies` dans `utils/anomalies.py`
2. Ajouter les nouvelles anomalies à la liste des types disponibles

### Pour étendre le plan comptable

Modifier la méthode `get_plan_comptable` dans `models/accounting_data.py`