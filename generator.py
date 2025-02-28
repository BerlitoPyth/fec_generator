"""
Classe principale du générateur FEC
"""

import random
from datetime import datetime, timedelta

from models.accounting_data import AccountingData
from models.transaction import Transaction
from utils.anomalies import inject_anomalies
from utils.formatters import format_decimal, format_fec_ecr_num
from utils.validators import validate_fec, fix_unbalanced_entries, fix_unbalanced_entries_excel


class FECGenerator:
    """
    Générateur de Fichier des Écritures Comptables (FEC)
    Permet de créer des données comptables fictives pour l'audit et les tests
    """
    
    def __init__(self, 
                 company_name="ENTREPRISE EXEMPLE SAS", 
                 siren="123456789", 
                 start_date="2024-01-01", 
                 end_date="2024-12-31",
                 journal_count=5,
                 transaction_count=500,
                 anomaly_rate=0.05):
        """
        Initialise le générateur FEC
        
        Args:
            company_name (str, optional): Nom de l'entreprise. Par défaut à "ENTREPRISE EXEMPLE SAS".
            siren (str, optional): Numéro SIREN. Par défaut à "123456789".
            start_date (str, optional): Date de début de période. Par défaut à "2024-01-01".
            end_date (str, optional): Date de fin de période. Par défaut à "2024-12-31".
            journal_count (int, optional): Nombre de journaux. Par défaut à 5.
            transaction_count (int, optional): Nombre de transactions à générer. Par défaut à 500.
            anomaly_rate (float, optional): Taux d'anomalies à injecter. Par défaut à 0.05.
        """
        
        self.company_name = company_name
        self.siren = siren
        self.start_date = datetime.strptime(start_date, "%Y-%m-%d")
        self.end_date = datetime.strptime(end_date, "%Y-%m-%d")
        self.journal_count = journal_count
        self.transaction_count = transaction_count
        self.anomaly_rate = anomaly_rate
        
        # Initialiser les structures
        self.plan_comptable = AccountingData.get_plan_comptable()
        self.journals = AccountingData.get_journals()
        self.transactions = []
        
        # Comptabilité auxiliaire
        self.auxiliaires = AccountingData.get_auxiliaires()
        
        # Compteurs
        self.current_ecr_id = 1
    
    def _get_auxiliary_account(self, account):
        """
        Retourne un compte auxiliaire approprié si applicable
        
        Args:
            account (str): Numéro de compte comptable
            
        Returns:
            tuple: (code_auxiliaire, libellé_auxiliaire)
        """
        account_prefix = account[:3]
        
        if account_prefix in self.auxiliaires:
            aux_keys = list(self.auxiliaires[account_prefix].keys())
            aux_code = random.choice(aux_keys)
            aux_lib = self.auxiliaires[account_prefix][aux_code]
            return aux_code, aux_lib
        
        return "", ""
    
    def generate_transactions(self):
        """
        Génère l'ensemble des transactions pour la période
        
        Returns:
            list: Transactions générées
        """
        transactions = []
        
        # Identifiants d'écriture par journal pour assurer la continuité
        journal_ecr_id = {journal: 1 for journal in self.journals.keys()}
        
        # Générer les transactions
        for _ in range(self.transaction_count):
            journal_code = random.choice(list(self.journals.keys()))
            transaction_date = Transaction.generate_transaction_date(self.start_date, self.end_date)
            
            # Identifier les comptes pertinents selon le journal
            relevant_accounts = AccountingData.get_relevant_accounts(journal_code)
            
            # Sélectionner un compte au débit et un au crédit
            debit_account = random.choice(relevant_accounts)
            
            # Logique pour un crédit cohérent avec le débit
            credit_accounts = AccountingData.get_related_account(debit_account)
            
            if not credit_accounts:
                credit_accounts = [acc for acc in relevant_accounts if acc != debit_account]
            
            credit_account = random.choice(credit_accounts)
            
            # Montant
            amount = Transaction.generate_realistic_amount(debit_account)
            
            # Référence de pièce
            piece_ref = Transaction.generate_piece_reference(journal_code, transaction_date)
            
            # Créer les lignes d'écriture
            ecr_id = journal_ecr_id[journal_code]
            
            # Date de validation
            valid_date = Transaction.generate_valid_date(transaction_date, self.end_date)
            
            # Ligne au débit
            debit_label = Transaction.generate_transaction_label(debit_account, journal_code)
            
            # Comptes auxiliaires
            debit_aux_num, debit_aux_lib = self._get_auxiliary_account(debit_account)
            
            # Lettrage
            debit_lettering, debit_date_lettering = Transaction.get_lettering_info(debit_account, self.end_date)
            
            transactions.append({
                'journal_code': journal_code,
                'journal_lib': self.journals[journal_code],
                'ecr_id': ecr_id,
                'ecr_date': transaction_date.strftime("%Y%m%d"),
                'transaction_date': transaction_date,
                'piece_ref': piece_ref,
                'piece_date': transaction_date.strftime("%Y%m%d"),
                'account': debit_account,
                'account_lib': self.plan_comptable[debit_account],
                'comp_aux': debit_aux_num,
                'comp_aux_lib': debit_aux_lib,
                'label': debit_label,
                'debit': amount,
                'credit': 0.00,
                'lettering': debit_lettering,
                'date_lettering': debit_date_lettering,
                'valid_date': valid_date
            })
            
            # Ligne au crédit
            credit_label = debit_label  # Même libellé pour l'équilibre
            
            # Comptes auxiliaires
            credit_aux_num, credit_aux_lib = self._get_auxiliary_account(credit_account)
            
            # Lettrage
            credit_lettering, credit_date_lettering = Transaction.get_lettering_info(credit_account, self.end_date)
            
            transactions.append({
                'journal_code': journal_code,
                'journal_lib': self.journals[journal_code],
                'ecr_id': ecr_id,
                'ecr_date': transaction_date.strftime("%Y%m%d"),
                'transaction_date': transaction_date,
                'piece_ref': piece_ref,
                'piece_date': transaction_date.strftime("%Y%m%d"),
                'account': credit_account,
                'account_lib': self.plan_comptable[credit_account],
                'comp_aux': credit_aux_num,
                'comp_aux_lib': credit_aux_lib,
                'label': credit_label,
                'debit': 0.00,
                'credit': amount,
                'lettering': credit_lettering,
                'date_lettering': credit_date_lettering,
                'valid_date': valid_date
            })
            
            # Incrémenter le compteur d'écriture pour ce journal
            journal_ecr_id[journal_code] += 1
        
        # Injecter des anomalies
        transactions = inject_anomalies(transactions, self.anomaly_rate)
        
        # Trier par journal et numéro d'écriture
        transactions.sort(key=lambda x: (x['journal_code'], x['ecr_id']))
        
        self.transactions = transactions
        return transactions
    
    def export_to_csv(self, filename="FEC_EXAMPLE.csv"):
        """
        Exporte les transactions au format FEC (CSV)
        
        Args:
            filename (str, optional): Nom du fichier CSV à générer. Par défaut à "FEC_EXAMPLE.csv".
            
        Returns:
            str: Chemin du fichier généré
        """
        from exporters.csv_exporter import export_to_csv
        
        if not self.transactions:
            self.generate_transactions()
            
        return export_to_csv(self.transactions, filename)
    
    def export_to_excel(self, filename="FEC_EXAMPLE.xlsx"):
        """
        Exporte les transactions au format Excel (.xlsx)
        
        Args:
            filename (str, optional): Nom du fichier Excel à générer. Par défaut à "FEC_EXAMPLE.xlsx".
            
        Returns:
            str: Chemin du fichier généré
        """
        from exporters.excel_exporter import export_to_excel
        
        if not self.transactions:
            self.generate_transactions()
            
        return export_to_excel(self.transactions, filename)
    
    def generate_multiple_fecs(self, count=5, base_filename="FEC_ENTREPRISE_", output_dir="generated_fecs"):
        """
        Génère plusieurs FEC avec des caractéristiques différentes
        
        Args:
            count (int, optional): Nombre de fichiers à générer. Par défaut à 5.
            base_filename (str, optional): Préfixe du nom de fichier. Par défaut à "FEC_ENTREPRISE_".
            output_dir (str, optional): Répertoire de sortie. Par défaut à "generated_fecs".
            
        Returns:
            list: Liste des informations sur les fichiers générés
        """
        from .exporters.csv_exporter import generate_multiple_fecs
        return generate_multiple_fecs(count, base_filename, output_dir)
    
    def generate_multiple_fecs_excel(self, count=5, base_filename="FEC_ENTREPRISE_", output_dir="generated_fecs_excel"):
        """
        Génère plusieurs FEC au format Excel avec des caractéristiques différentes
        
        Args:
            count (int, optional): Nombre de fichiers à générer. Par défaut à 5.
            base_filename (str, optional): Préfixe du nom de fichier. Par défaut à "FEC_ENTREPRISE_".
            output_dir (str, optional): Répertoire de sortie. Par défaut à "generated_fecs_excel".
            
        Returns:
            list: Liste des informations sur les fichiers générés
        """
        from .exporters.excel_exporter import generate_multiple_fecs_excel
        return generate_multiple_fecs_excel(count, base_filename, output_dir)