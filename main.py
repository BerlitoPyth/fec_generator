import sys
import os
import argparse
from datetime import datetime

# Ajouter le répertoire parent au chemin Python
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import absolu
from generator import FECGenerator

def main():
    """
    Point d'entrée principal avec traitement des arguments en ligne de commande
    """
    # Définir les arguments de ligne de commande
    parser = argparse.ArgumentParser(description='Générateur de Fichier des Écritures Comptables (FEC)')
    
    # Arguments généraux
    parser.add_argument('--company', type=str, default="ENTREPRISE EXEMPLE SAS",
                        help='Nom de l\'entreprise')
    parser.add_argument('--siren', type=str, default="123456789",
                        help='Numéro SIREN')
    parser.add_argument('--start-date', type=str, default=f"{datetime.now().year}-01-01",
                        help='Date de début (format YYYY-MM-DD)')
    parser.add_argument('--end-date', type=str, default=f"{datetime.now().year}-12-31",
                        help='Date de fin (format YYYY-MM-DD)')
    parser.add_argument('--transactions', type=int, default=500,
                        help='Nombre de transactions à générer')
    parser.add_argument('--anomaly-rate', type=float, default=0.05,
                        help='Taux d\'anomalies à injecter (entre 0 et 1)')
    
    # Mode d'exportation
    parser.add_argument('--format', type=str, choices=['csv', 'excel', 'both'], default='csv',
                        help='Format d\'exportation (csv, excel ou both)')
    parser.add_argument('--output', type=str, default="FEC_GENERATED",
                        help='Nom de base du fichier de sortie (sans extension)')
    
    # Mode batch
    parser.add_argument('--batch', action='store_true',
                        help='Générer plusieurs fichiers FEC')
    parser.add_argument('--batch-count', type=int, default=5,
                        help='Nombre de fichiers à générer en mode batch')
    parser.add_argument('--output-dir', type=str, default="generated_fecs",
                        help='Répertoire de sortie pour le mode batch')
    
    # Analyser les arguments
    args = parser.parse_args()
    
    # Créer le générateur avec les paramètres
    generator = FECGenerator(
        company_name=args.company,
        siren=args.siren,
        start_date=args.start_date,
        end_date=args.end_date,
        transaction_count=args.transactions,
        anomaly_rate=args.anomaly_rate
    )
    
    # Mode batch: génération de multiples FEC
    if args.batch:
        if args.format == 'csv' or args.format == 'both':
            generated_csv = generator.generate_multiple_fecs(
                count=args.batch_count,
                base_filename=f"{args.output}_",
                output_dir=args.output_dir
            )
            print(f"Générés {len(generated_csv)} fichiers CSV dans {args.output_dir}")
            
        if args.format == 'excel' or args.format == 'both':
            generated_excel = generator.generate_multiple_fecs_excel(
                count=args.batch_count,
                base_filename=f"{args.output}_",
                output_dir=f"{args.output_dir}_excel"
            )
            print(f"Générés {len(generated_excel)} fichiers Excel dans {args.output_dir}_excel")
    
    # Mode normal: génération d'un seul FEC
    else:
        # Générer les transactions
        generator.generate_transactions()
        
        # Exporter selon le format choisi
        if args.format == 'csv' or args.format == 'both':
            csv_file = generator.export_to_csv(f"{args.output}.csv")
            print(f"FEC CSV généré: {csv_file}")
            
        if args.format == 'excel' or args.format == 'both':
            excel_file = generator.export_to_excel(f"{args.output}.xlsx")
            print(f"FEC Excel généré: {excel_file}")


if __name__ == "__main__":
    main()