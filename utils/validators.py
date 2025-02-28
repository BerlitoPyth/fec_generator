"""
Fonctions de validation pour le générateur FEC
"""

def validate_fec(export_data):
    """
    Vérifie la validité du FEC généré (équilibre des écritures)
    
    Args:
        export_data (list): Liste des lignes d'écritures au format FEC
        
    Returns:
        tuple: (bool, list) - Validité et liste des erreurs
    """
    errors = []
    
    # Vérifier l'équilibre des écritures
    ecr_balances = {}
    for row in export_data:
        ecr_key = (row["JournalCode"], row["EcritureNum"])
        if ecr_key not in ecr_balances:
            ecr_balances[ecr_key] = 0
        
        # Convertir les montants de texte à nombres
        debit = float(row["Debit"].replace(",", "."))
        credit = float(row["Credit"].replace(",", "."))
        
        ecr_balances[ecr_key] += debit - credit
    
    # Vérifier l'équilibre (avec tolérance pour les erreurs d'arrondi)
    for ecr_key, balance in ecr_balances.items():
        if abs(balance) > 0.01:
            errors.append(f"Écriture {ecr_key} non équilibrée: {balance}")
    
    return (len(errors) == 0), errors


def fix_unbalanced_entries(export_data):
    """
    Corrige les écritures non équilibrées dans un FEC (format CSV)
    
    Args:
        export_data (list): Liste des lignes d'écritures au format FEC
        
    Returns:
        list: Liste des lignes d'écritures corrigées
    """
    # Regrouper les lignes par écriture
    entries = {}
    for row in export_data:
        key = (row["JournalCode"], row["EcritureNum"])
        if key not in entries:
            entries[key] = []
        entries[key].append(row)
    
    # Vérifier et corriger l'équilibre de chaque écriture
    for key, rows in entries.items():
        total_debit = sum(float(row["Debit"].replace(",", ".")) for row in rows)
        total_credit = sum(float(row["Credit"].replace(",", ".")) for row in rows)
        
        difference = total_debit - total_credit
        
        if abs(difference) > 0.01:  # Si déséquilibre significatif
            # Trouver la ligne avec le montant le plus élevé pour ajuster
            if difference > 0:  # Trop de débit
                # Trouver la ligne de débit la plus élevée
                target_rows = [r for r in rows if float(r["Debit"].replace(",", ".")) > 0]
                if target_rows:
                    target_row = max(target_rows, key=lambda r: float(r["Debit"].replace(",", ".")))
                    new_amount = float(target_row["Debit"].replace(",", ".")) - difference
                    target_row["Debit"] = f"{new_amount:.2f}".replace(".", ",")
            else:  # Trop de crédit
                # Trouver la ligne de crédit la plus élevée
                target_rows = [r for r in rows if float(r["Credit"].replace(",", ".")) > 0]
                if target_rows:
                    target_row = max(target_rows, key=lambda r: float(r["Credit"].replace(",", ".")))
                    new_amount = float(target_row["Credit"].replace(",", ".")) + difference
                    target_row["Credit"] = f"{new_amount:.2f}".replace(".", ",")
    
    return export_data


def fix_unbalanced_entries_excel(export_data):
    """
    Corrige les écritures non équilibrées pour l'export Excel (valeurs numériques)
    
    Args:
        export_data (list): Liste des lignes d'écritures au format Excel
        
    Returns:
        list: Liste des lignes d'écritures corrigées
    """
    # Regrouper les lignes par écriture
    entries = {}
    for row in export_data:
        key = (row["JournalCode"], row["EcritureNum"])
        if key not in entries:
            entries[key] = []
        entries[key].append(row)
    
    # Vérifier et corriger l'équilibre de chaque écriture
    for key, rows in entries.items():
        total_debit = sum(row["Debit"] for row in rows)
        total_credit = sum(row["Credit"] for row in rows)
        
        difference = total_debit - total_credit
        
        if abs(difference) > 0.01:  # Si déséquilibre significatif
            # Trouver la ligne avec le montant le plus élevé pour ajuster
            if difference > 0:  # Trop de débit
                target_rows = [r for r in rows if r["Debit"] > 0]
                if target_rows:
                    target_row = max(target_rows, key=lambda r: r["Debit"])
                    target_row["Debit"] = target_row["Debit"] - difference
            else:  # Trop de crédit
                target_rows = [r for r in rows if r["Credit"] > 0]
                if target_rows:
                    target_row = max(target_rows, key=lambda r: r["Credit"])
                    target_row["Credit"] = target_row["Credit"] + difference
    
    return export_data