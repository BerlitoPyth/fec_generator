"""
Fonctions de génération d'anomalies pour le FEC
"""

import random
from datetime import timedelta

def inject_anomalies(transactions, anomaly_rate=0.05):
    """
    Injecte des anomalies dans les transactions pour l'IA prédictive
    
    Args:
        transactions (list): Liste des transactions
        anomaly_rate (float, optional): Taux d'anomalies à injecter. Par défaut à 0.05.
    
    Returns:
        list: Transactions avec anomalies injectées
    """
    anomaly_count = int(len(transactions) * anomaly_rate)
    anomaly_indices = random.sample(range(len(transactions)), anomaly_count)
    
    for idx in anomaly_indices:
        anomaly_type = random.choice([
            "round_amount", 
            "unusual_date", 
            "duplicate_ref", 
            "unusual_account_usage",
            "threshold_amount",
            "weekend_transaction"
        ])
        
        if anomaly_type == "round_amount":
            # Montants ronds suspects
            transactions[idx]['debit'] = round(transactions[idx]['debit'])
            transactions[idx]['credit'] = round(transactions[idx]['credit'])
        
        elif anomaly_type == "unusual_date":
            # Transaction en dehors des heures de bureau
            hour = random.randint(20, 23)
            transactions[idx]['transaction_date'] = transactions[idx]['transaction_date'].replace(hour=hour)
        
        elif anomaly_type == "duplicate_ref":
            # Référence de pièce dupliquée
            if idx > 0:
                transactions[idx]['piece_ref'] = transactions[idx-1]['piece_ref']
        
        elif anomaly_type == "unusual_account_usage":
            # Utilisation inhabituelle d'un compte
            if transactions[idx]['account'].startswith("5"):
                unusual_accounts = ["471000", "486000"]
                transactions[idx]['account'] = random.choice(unusual_accounts)
                # Mise à jour du libellé du compte
                plan_comptable = {
                    "471000": "Compte d'attente",
                    "486000": "Charges constatees d'avance"
                }
                transactions[idx]['account_lib'] = plan_comptable[transactions[idx]['account']]
        
        elif anomaly_type == "threshold_amount":
            # Montant juste sous un seuil d'autorisation (par exemple, 999€ au lieu de 1000€)
            thresholds = [1000, 5000, 10000]
            chosen_threshold = random.choice(thresholds)
            if transactions[idx]['debit'] > 0:
                transactions[idx]['debit'] = chosen_threshold - random.uniform(0.01, 1)
            else:
                transactions[idx]['credit'] = chosen_threshold - random.uniform(0.01, 1)
        
        elif anomaly_type == "weekend_transaction":
            # Transaction un weekend
            # Trouver un samedi ou dimanche proche
            current_date = transactions[idx]['transaction_date']
            days_to_add = (5 - current_date.weekday()) % 7  # Pour atteindre samedi
            if days_to_add == 0:
                days_to_add = 1  # Pour dimanche si on est déjà samedi
            transactions[idx]['transaction_date'] = current_date + timedelta(days=days_to_add)
            transactions[idx]['ecr_date'] = transactions[idx]['transaction_date'].strftime("%Y%m%d")
            
    return transactions