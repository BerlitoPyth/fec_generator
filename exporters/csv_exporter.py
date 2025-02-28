"""
Fonctions d'exportation CSV pour le générateur FEC
"""

import os
import csv
import random
from datetime import datetime
from faker import Faker

from ..utils.formatters import format_decimal, format_fec_ecr_num
from ..utils.validators import validate_fec, fix_unbalanced_entries
from ..generator import FECGenerator

# Initialiser le générateur de données fictives
fake = Faker('fr_FR')

def export_to_csv(transactions, filename="FEC_EXAMPLE.csv"):
    """
    Exporte les transactions au format FEC (CSV) sans problèmes d'encodage
    
    Args:
        transactions (list): Liste des transactions
        filename (str, optional): Nom du fichier CSV à générer. Par défaut à "FEC_EXAMPLE.csv".
    
    Returns:
        str: Chemin du fichier généré
    """
    # Les colonnes du FEC dans l'ordre requis
    fec_columns = [
        "JournalCode", "JournalLib", "EcritureNum", "EcritureDate",
        "CompteNum", "CompteLib", "CompAuxNum", "CompAuxLib",
        "PieceRef", "PieceDate", "EcritureLib", "Debit", "Credit",
        "EcritureLet", "DateLet", "ValidDate", "Montantdevise", "Idevise"
    ]
    
    # Préparation des données pour export
    export_data = []
    for t in transactions:
        row = {
            "JournalCode": t['journal_code'],
            "JournalLib": t['journal_lib'],
            "EcritureNum": format_fec_ecr_num(t['journal_code'], t['ecr_id']),
            "EcritureDate": t['ecr_date'],
            "CompteNum": t['account'],
            "CompteLib": t['account_lib'],
            "CompAuxNum": t['comp_aux'],
            "CompAuxLib": t['comp_aux_lib'],
            "PieceRef": t['piece_ref'],
            "PieceDate": t['piece_date'],
            "EcritureLib": t['label'],
            "Debit": format_decimal(t['debit']),
            "Credit": format_decimal(t['credit']),
            "EcritureLet": t['lettering'],
            "DateLet": t['date_lettering'],
            "ValidDate": t['valid_date'],
            "Montantdevise": "",
            "Idevise": ""
        }
        export_data.append(row)
    
    # Validation et correction du FEC
    is_valid, errors = validate_fec(export_data)
    if not is_valid:
        print("Correction automatique des écritures non équilibrées...")
        export_data = fix_unbalanced_entries(export_data)
        
        # Vérification après correction
        is_valid, errors = validate_fec(export_data)
        if not is_valid:
            print("ATTENTION: Le FEC contient toujours des erreurs après correction")
        else:
            print("Corrections appliquées avec succès")
    
    # Création du répertoire de sortie si nécessaire
    os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else '.', exist_ok=True)
    
    # Écriture du fichier CSV avec le format FEC (séparateur |)
    # Utilisation explicite de l'encodage ASCII pour éviter tout problème
    with open(filename, 'w', newline='', encoding='ascii') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fec_columns, delimiter='|')
        writer.writeheader()
        writer.writerows(export_data)
        
    print(f"FEC exporté avec succès: {filename}")
    print(f"Nombre de transactions: {len(export_data)}")
    
    return filename


def generate_multiple_fecs(count=5, base_filename="FEC_ENTREPRISE_", output_dir="generated_fecs"):
    """
    Génère plusieurs FEC avec des caractéristiques différentes
    
    Args:
        count (int, optional): Nombre de fichiers à générer. Par défaut à 5.
        base_filename (str, optional): Préfixe du nom de fichier. Par défaut à "FEC_ENTREPRISE_".
        output_dir (str, optional): Répertoire de sortie. Par défaut à "generated_fecs".
    
    Returns:
        list: Liste des informations sur les fichiers générés
    """
    # Création du répertoire de sortie
    os.makedirs(output_dir, exist_ok=True)
    
    generated_files = []
    
    for i in range(1, count + 1):
        # Varier les paramètres pour chaque FEC
        company_name = f"ENTREPRISE_{i} SAS"
        siren = fake.numerify("#########")
        
        # Différentes périodes comptables
        year = 2023
        start_date = f"{year}-01-01"
        end_date = f"{year}-12-31"
        
        # Varier le nombre de transactions et le taux d'anomalies
        transaction_count = random.randint(300, 1000)
        anomaly_rate = random.uniform(0.03, 0.15)
        
        # Créer un nouveau générateur avec ces paramètres
        generator = FECGenerator(
            company_name=company_name,
            siren=siren,
            start_date=start_date,
            end_date=end_date,
            transaction_count=transaction_count,
            anomaly_rate=anomaly_rate
        )
        
        # Générer et exporter le FEC
        filename = os.path.join(output_dir, f"{base_filename}{i}_{year}.csv")
        generator.generate_transactions()
        generator.export_to_csv(filename)
        
        generated_files.append({
            "filename": filename,
            "company": company_name,
            "transaction_count": transaction_count,
            "anomaly_rate": anomaly_rate,
            "anomaly_count": int(transaction_count * anomaly_rate)
        })
        
        print(f"Généré FEC {i}/{count}: {filename}")
    
    return generated_files