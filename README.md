# FEC Generator

Générateur de Fichier des Écritures Comptables (FEC) pour l'audit, les tests et la formation.

## Description

Ce projet propose un générateur de données comptables au format FEC (Fichier des Écritures Comptables) conforme aux normes françaises. Il permet de créer des jeux de données fictifs mais réalistes pour diverses utilisations :

- Formation à l'analyse de données comptables
- Tests de logiciels d'audit
- Développement d'algorithmes de détection d'anomalies
- Démonstrations de solutions comptables et financières

## Caractéristiques

- Génération de transactions équilibrées avec débit et crédit
- Plan comptable français standard inclus
- Support des comptes auxiliaires (clients, fournisseurs)
- Exportation au format CSV (conforme FEC) et Excel
- Injection contrôlée d'anomalies pour les tests d'audit
- Paramétrage flexible (période, nombre de transactions, taux d'anomalies)
- Mode batch pour générer plusieurs fichiers avec des caractéristiques différentes

## Installation

### Via pip

```bash
pip install fec-generator
```

### Depuis les sources

```bash
git clone https://github.com/votre-compte/fec-generator.git
cd fec-generator
pip install -e .
```

## Utilisation

### En ligne de commande

```bash
# Génération de base
fec-generator --company "MA SOCIETE SAS" --siren "123456789" --transactions 1000

# Contrôler la période
fec-generator --start-date "2023-01-01" --end-date "2023-12-31"

# Exporter en Excel
fec-generator --format excel --output "MON_FEC_2023"

# Génération en lot (plusieurs fichiers)
fec-generator --batch --batch-count 10 --output-dir "mes_fecs" --anomaly-rate 0.1
```

### En tant que bibliothèque Python

```python
from fec_generator import FECGenerator

# Créer un générateur
generator = FECGenerator(
    company_name="MA SOCIETE SAS",
    siren="123456789",
    start_date="2023-01-01",
    end_date="2023-12-31",
    transaction_count=1000,
    anomaly_rate=0.05
)

# Générer les transactions
transactions = generator.generate_transactions()

# Exporter au format CSV
generator.export_to_csv("mon_fec_2023.csv")

# Exporter au format Excel
generator.export_to_excel("mon_fec_2023.xlsx")

# Générer plusieurs fichiers
generator.generate_multiple_fecs(count=5, output_dir="mes_fecs")
```

## Structure du projet

```
fec_generator/
│
├── __init__.py                # Initialisation du package
├── main.py                    # Point d'entrée principal
├── generator.py               # Classe principale FECGenerator
├── models/
│   ├── __init__.py            # Initialisation du sous-package
│   ├── accounting_data.py     # Définition des données comptables 
│   └── transaction.py         # Modèle de transaction
├── utils/
│   ├── __init__.py            # Initialisation du sous-package
│   ├── formatters.py          # Fonctions de formatage (dates, montants)
│   ├── validators.py          # Validation des données FEC
│   └── anomalies.py           # Génération d'anomalies
└── exporters/
    ├── __init__.py            # Initialisation du sous-package
    ├── csv_exporter.py        # Export au format CSV
    └── excel_exporter.py      # Export au format Excel
```

## Licence

Ce projet est sous licence MIT. Voir le fichier LICENSE pour plus de détails.

## Contribution

Les contributions sont les bienvenues ! N'hésitez pas à ouvrir une issue ou une pull request.