import sys
import os
import argparse
from datetime import datetime

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import absolu
from generator import FECGenerator

def get_user_input():
    """
    Obtient les paramètres interactivement depuis le terminal
    """
    print("\n=== Générateur de Fichier des Écritures Comptables (FEC) ===\n")
    
    # Demander le format
    while True:
        format_choice = input("Choisissez le format de sortie (csv/excel/both) [csv]: ").strip().lower()
        if format_choice == "":
            format_choice = "csv"
        if format_choice in ["csv", "excel", "both"]:
            break
        print("Format non valide. Veuillez choisir 'csv', 'excel' ou 'both'.")
    
    # Demander le nombre de fichiers
    while True:
        try:
            files_input = input("Nombre de fichiers à générer [1]: ").strip()
            if files_input == "":
                files_count = 1
            else:
                files_count = int(files_input)
            if files_count > 0:
                break
            print("Veuillez entrer un nombre positif.")
        except ValueError:
            print("Veuillez entrer un nombre entier valide.")
    
    # Autres paramètres optionnels
    company_name = input("Nom de l'entreprise [ENTREPRISE EXEMPLE SAS]: ").strip()
    if company_name == "":
        company_name = "ENTREPRISE EXEMPLE SAS"
    
    transactions_input = input("Nombre de transactions [500]: ").strip()
    if transactions_input == "":
        transactions_count = 500
    else:
        try:
            transactions_count = int(transactions_input)
        except ValueError:
            print("Valeur non valide, utilisation de la valeur par défaut (500)")
            transactions_count = 500
    
    return {
        "format": format_choice,
        "files_count": files_count,
        "company_name": company_name,
        "transactions_count": transactions_count
    }

def main():
    """
    Point d'entrée principal avec interface interactive
    """
    # Obtenir les paramètres de l'utilisateur
    params = get_user_input()
    
    # Paramètres par défaut
    current_year = datetime.now().year
    start_date = f"{current_year}-01-01"
    end_date = f"{current_year}-12-31"
    siren = "123456789"
    anomaly_rate = 0.05
    output_base = "FEC_GENERATED"
    
    # Créer les dossiers de sortie
    csv_output_dir = "output_csv"
    excel_output_dir = "output_excel"
    os.makedirs(csv_output_dir, exist_ok=True)
    os.makedirs(excel_output_dir, exist_ok=True)
    
    # Créer le générateur
    generator = FECGenerator(
        company_name=params["company_name"],
        siren=siren,
        start_date=start_date,
        end_date=end_date,
        transaction_count=params["transactions_count"],
        anomaly_rate=anomaly_rate
    )
    
    # Mode multi-fichiers
    if params["files_count"] > 1:
        print(f"\nGénération de {params['files_count']} fichiers FEC...")
        
        # Générer les fichiers CSV
        if params["format"] in ["csv", "both"]:
            generated_csv = generator.generate_multiple_fecs(
                count=params["files_count"],
                base_filename=f"{output_base}_",
                output_dir=csv_output_dir
            )
            print(f"✓ Générés {len(generated_csv)} fichiers CSV dans '{csv_output_dir}'")
        
        # Générer les fichiers Excel
        if params["format"] in ["excel", "both"]:
            generated_excel = generator.generate_multiple_fecs_excel(
                count=params["files_count"],
                base_filename=f"{output_base}_",
                output_dir=excel_output_dir
            )
            print(f"✓ Générés {len(generated_excel)} fichiers Excel dans '{excel_output_dir}'")
    
    # Mode fichier unique
    else:
        print("\nGénération d'un fichier FEC...")
        generator.generate_transactions()
        
        # Générer le fichier CSV
        if params["format"] in ["csv", "both"]:
            csv_file = os.path.join(csv_output_dir, f"{output_base}.csv")
            generator.export_to_csv(csv_file)
            print(f"✓ FEC CSV généré: {csv_file}")
        
        # Générer le fichier Excel
        if params["format"] in ["excel", "both"]:
            excel_file = os.path.join(excel_output_dir, f"{output_base}.xlsx")
            generator.export_to_excel(excel_file)
            print(f"✓ FEC Excel généré: {excel_file}")
    
    print("\nGénération terminée avec succès!\n")

if __name__ == "__main__":
    main()