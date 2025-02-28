"""
Fonctions de formatage pour le générateur FEC
"""

def format_decimal(value):
    """
    Formate un nombre décimal selon les normes FEC (virgule comme séparateur)
    
    Args:
        value (float): Valeur numérique à formater
        
    Returns:
        str: Valeur formatée avec virgule comme séparateur décimal
    """
    return f"{value:.2f}".replace(".", ",")


def format_fec_ecr_num(journal_code, ecr_id):
    """
    Formate le numéro d'écriture selon les normes FEC
    
    Args:
        journal_code (str): Code du journal
        ecr_id (int): Identifiant numérique de l'écriture
        
    Returns:
        str: Numéro d'écriture formaté
    """
    return f"{journal_code}{str(ecr_id).zfill(5)}"