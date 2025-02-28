"""
Modèle représentant une transaction comptable pour le générateur FEC
"""

import random
from datetime import datetime, timedelta
import string
from faker import Faker

# Initialiser le générateur de données fictives
fake = Faker('fr_FR')

class Transaction:
    """
    Classe représentant une transaction comptable dans le FEC
    """
    
    @staticmethod
    def generate_transaction_date(start_date, end_date):
        """Génère une date aléatoire dans la période (jours ouvrés)"""
        delta = (end_date - start_date).days
        random_days = random.randint(0, delta)
        transaction_date = start_date + timedelta(days=random_days)
        
        # Si weekend, ajuster au vendredi précédent
        if transaction_date.weekday() >= 5:  # 5=samedi, 6=dimanche
            transaction_date -= timedelta(days=transaction_date.weekday() - 4)  # revenir au vendredi
            
        return transaction_date
    
    @staticmethod
    def generate_valid_date(transaction_date, end_date):
        """Génère une date de validation postérieure à la date de transaction"""
        max_days = min(7, (end_date - transaction_date).days)
        if max_days <= 0:
            return transaction_date.strftime("%Y%m%d")
        days_after = random.randint(0, max_days)
        valid_date = transaction_date + timedelta(days=days_after)
        return valid_date.strftime("%Y%m%d")
    
    @staticmethod
    def generate_realistic_amount(account):
        """Génère un montant réaliste basé sur le type de compte"""
        account_prefix = account[:1]
        
        # Montants plus élevés pour certains comptes
        if account in ["401000", "411000", "512000"]:
            return round(random.uniform(100, 10000), 2)
        
        # Achats et ventes
        elif account_prefix in ["6", "7"]:
            return round(random.uniform(10, 2000), 2)
        
        # Immobilisations
        elif account_prefix == "2":
            return round(random.uniform(500, 20000), 2)
        
        # Valeur par défaut
        else:
            return round(random.uniform(10, 1000), 2)
    
    @staticmethod
    def generate_transaction_label(account, journal):
        """Génère un libellé réaliste pour une transaction (sans accents)"""
        if journal == "AC":
            suppliers = ["DALKIA FRANCE", "TELECOM SAS", "FOURNITURES BUREAU", "PAPETERIE EXPRESS", "ELECTRICITE DE FRANCE"]
            return f"FACT {fake.date_this_year().strftime('%y%m%d')} {random.choice(suppliers)}"
        
        elif journal == "VE":
            clients = ["CLIENT ALPHA", "CLIENT BETA", "CLIENT GAMMA", "CLIENT DELTA", "CLIENT EPSILON"]
            return f"FACT CLIENT {random.choice(clients)} {fake.random_number(digits=6)}"
        
        elif journal == "BQ":
            if account.startswith("6"):
                return f"CB {fake.date_this_year().strftime('%d/%m')} FOURNISSEUR"
            elif account.startswith("5"):
                return f"VIREMENT {fake.date_this_year().strftime('%d/%m')} REF {fake.random_number(digits=8)}"
            else:
                return f"OPERATION BANCAIRE {fake.date_this_year().strftime('%d/%m')}"
        
        elif journal == "OD":
            return f"ECRITURE DE REGULARISATION {fake.date_this_year().strftime('%m/%Y')}"
        
        else:
            return f"OPERATION DIVERSE {fake.date_this_year().strftime('%d/%m/%Y')}"
    
    @staticmethod
    def generate_piece_reference(journal, transaction_date):
        """Génère une référence de pièce comptable"""
        month = transaction_date.strftime("%m")
        return f"{journal}{month}{random.randint(1000, 9999)}"
    
    @staticmethod
    def get_lettering_info(account, end_date):
        """Génère des informations de lettrage pour certains comptes"""
        if account.startswith(("401", "411")):
            # 20% de chance d'avoir un lettrage
            if random.random() < 0.2:
                letter = random.choice(string.ascii_uppercase)
                num = random.randint(1, 9)
                lettering = f"{letter}{num}"
                # Date de lettrage
                date_lettering = (end_date - timedelta(days=random.randint(0, 30))).strftime("%Y%m%d")
                return lettering, date_lettering
        
        return "", ""