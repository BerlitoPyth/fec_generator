"""
Définition des données comptables utilisées par le générateur FEC
"""

from faker import Faker

# Initialiser le générateur de données fictives
fake = Faker('fr_FR')

class AccountingData:
    """
    Classe qui encapsule les données comptables (plan comptable, journaux, auxiliaires)
    """
    
    @staticmethod
    def get_plan_comptable():
        """Initialise un plan comptable français conforme (version ASCII)"""
        pc = {
            # Classe 1 - Comptes de capitaux
            "101000": "Capital social",
            "106100": "Reserve legale",
            "106800": "Autres reserves",
            "120000": "Resultat de l'exercice",
            "131800": "Autres subventions d'investissement",
            "151000": "Provisions pour risques",
            "164000": "Emprunts aupres des etablissements de credit",
            "165000": "Depots et cautionnements recus",
            "168800": "Interets courus sur emprunts",
            
            # Classe 2 - Comptes d'immobilisations
            "201000": "Frais d'etablissement",
            "203000": "Frais de recherche et developpement",
            "205000": "Logiciels",
            "207000": "Fonds commercial",
            "211000": "Terrains",
            "213100": "Constructions - Batiments",
            "213500": "Installations generales, agencements",
            "215400": "Materiel industriel",
            "218100": "Installations generales, agencements divers",
            "218200": "Materiel de transport",
            "218300": "Materiel de bureau et informatique",
            "218400": "Mobilier",
            "231000": "Immobilisations corporelles en cours",
            "280500": "Amort. logiciels",
            "281310": "Amort. batiments",
            "281350": "Amort. installations generales",
            "281540": "Amort. materiel industriel",
            "281810": "Amort. installations generales",
            "281820": "Amort. materiel de transport",
            "281830": "Amort. materiel de bureau",
            "281840": "Amort. mobilier",
            
            # Classe 3 - Comptes de stocks
            "311000": "Matieres premieres",
            "321000": "Matieres consommables",
            "350000": "Produits finis",
            "355000": "Produits finis (groupe)",
            "370000": "Marchandises",
            "371000": "Stock de marchandises",
            "397100": "Depreciation des stocks de marchandises",
            
            # Classe 4 - Comptes de tiers
            "401000": "Fournisseurs",
            "403000": "Fournisseurs - Effets a payer",
            "404000": "Fournisseurs d'immobilisations",
            "408100": "Fournisseurs - Factures non parvenues",
            "408400": "Fournisseurs d'immobilisations - Factures non parvenues",
            "409100": "Fournisseurs - Avances et acomptes verses",
            "411000": "Clients",
            "413000": "Clients - Effets a recevoir",
            "416000": "Clients douteux",
            "418100": "Clients - Factures a etablir",
            "419100": "Clients - Avances et acomptes recus",
            "421000": "Personnel - Remunerations dues",
            "425000": "Personnel - Avances et acomptes",
            "427000": "Personnel - Oppositions",
            "428200": "Personnel - Conges payes",
            "431000": "Securite sociale",
            "437000": "Autres organismes sociaux",
            "438200": "Charges sociales sur conges a payer",
            "441000": "Etat - Impot sur les benefices",
            "444000": "Etat - Impots sur les benefices",
            "445510": "TVA a decaisser",
            "445520": "TVA due intracommunautaire",
            "445620": "TVA deductible sur immobilisations",
            "445660": "TVA deductible sur ABS",
            "445670": "TVA collectee",
            "445710": "TVA collectee a payer",
            "445860": "TVA sur factures non parvenues",
            "445870": "TVA sur factures a etablir",
            "447100": "Autres impots, taxes et versements assimiles",
            "451000": "Groupe",
            "455000": "Associes - Comptes courants",
            "467000": "Autres comptes debiteurs ou crediteurs",
            "468600": "Charges a payer",
            "471000": "Compte d'attente",
            "486000": "Charges constatees d'avance",
            "487000": "Produits constates d'avance",
            "491000": "Depreciation des comptes clients",
            
            # Classe 5 - Comptes financiers
            "500000": "Valeurs mobilieres de placement",
            "508000": "Interets courus sur VMP",
            "511000": "Valeurs a l'encaissement",
            "512000": "Banque principale",
            "512100": "Banque secondaire",
            "514000": "Cheques postaux",
            "517000": "Autres organismes financiers",
            "518100": "Interets courus a payer",
            "518700": "Interets courus a recevoir",
            "530000": "Caisse",
            "580000": "Virements internes",
            "590000": "Depreciation des valeurs mobilieres de placement",
            
            # Classe 6 - Comptes de charges
            "601000": "Achats de matieres premieres",
            "602100": "Achats de matieres consommables",
            "602200": "Achats de fournitures consommables",
            "602260": "Achats d'emballages",
            "606100": "Electricite, gaz, eau",
            "606300": "Fournitures d'entretien et petit equipement",
            "606400": "Fournitures administratives",
            "606800": "Autres matieres et fournitures",
            "607000": "Achats de marchandises",
            "608500": "Frais accessoires d'achat",
            "611000": "Sous-traitance generale",
            "612000": "Redevances de credit-bail",
            "613200": "Locations immobilieres",
            "613500": "Locations mobilieres",
            "614000": "Charges locatives",
            "615200": "Entretien et reparations sur biens immobiliers",
            "615500": "Entretien et reparations sur biens mobiliers",
            "615600": "Maintenance",
            "616000": "Primes d'assurance",
            "618100": "Documentation generale",
            "618500": "Frais de colloques, seminaires, conferences",
            "621000": "Personnel exterieur a l'entreprise",
            "622600": "Honoraires",
            "622700": "Frais d'actes et de contentieux",
            "623000": "Publicite, publications, relations publiques",
            "623100": "Annonces et insertions",
            "623400": "Cadeaux a la clientele",
            "625100": "Voyages et deplacements",
            "625600": "Missions",
            "625700": "Receptions",
            "626000": "Frais postaux et de telecommunications",
            "627000": "Services bancaires et assimiles",
            "628100": "Concours divers (cotisations...)",
            "631000": "Impots, taxes et versements assimiles sur remunerations",
            "633000": "Impots, taxes et versements assimiles sur remunerations (autres organismes)",
            "635000": "Autres impots, taxes et versements assimiles",
            "641000": "Remunerations du personnel",
            "642000": "Remunerations des dirigeants",
            "645000": "Charges de securite sociale et de prevoyance",
            "647000": "Autres charges sociales",
            "648000": "Autres charges de personnel",
            "651000": "Redevances pour concessions, brevets, licences, etc.",
            "654000": "Pertes sur creances irrecouvrables",
            "658000": "Charges diverses de gestion courante",
            "661000": "Charges d'interets",
            "664000": "Pertes sur cessions de valeurs mobilieres de placement",
            "665000": "Escomptes accordes",
            "666000": "Pertes de change",
            "671000": "Charges exceptionnelles sur operations de gestion",
            "675000": "Valeurs comptables des elements d'actif cedes",
            "681110": "Dot. amort. sur immo. incorporelles",
            "681120": "Dot. amort. sur immo. corporelles",
            "681500": "Dot. provisions pour risques et charges d'exploitation",
            "681740": "Dot. provisions sur creances",
            "686500": "Dot. provisions pour risques et charges financiers",
            "687000": "Dot. amort. et provisions exceptionnels",
            "691000": "Participation des salaries aux resultats",
            "695000": "Impots sur les benefices",
            "698000": "Integration fiscale - Charges",
            
            # Classe 7 - Comptes de produits
            "701000": "Ventes de produits finis",
            "706000": "Prestations de services",
            "707000": "Ventes de marchandises",
            "708500": "Ports et frais accessoires factures",
            "709000": "Rabais, remises et ristournes accordes",
            "713000": "Variation des stocks",
            "720000": "Production immobilisee",
            "740000": "Subventions d'exploitation",
            "751000": "Redevances pour concessions, brevets, licences, etc.",
            "754000": "Ristournes percues des cooperatives",
            "758000": "Produits divers de gestion courante",
            "761000": "Produits de participations",
            "762000": "Produits des autres immobilisations financieres",
            "763000": "Revenus des autres creances",
            "764000": "Revenus des valeurs mobilieres de placement",
            "765000": "Escomptes obtenus",
            "766000": "Gains de change",
            "767000": "Produits nets sur cessions de valeurs mobilieres de placement",
            "771000": "Produits exceptionnels sur operations de gestion",
            "775000": "Produits des cessions d'elements d'actif",
            "777000": "Quote-part des subventions d'investissement viree au resultat",
            "781500": "Reprises sur provisions pour risques et charges d'exploitation",
            "781740": "Reprises sur provisions sur creances",
            "786500": "Reprises sur provisions pour risques et charges financiers",
            "791000": "Transferts de charges d'exploitation",
            "796000": "Transferts de charges financieres",
            "797000": "Transferts de charges exceptionnelles",
            "798000": "Integration fiscale - Produits"
        }
        return pc
    
    @staticmethod
    def get_journals():
        """Initialise les journaux comptables standard"""
        return {
            "AC": "Achats",
            "VE": "Ventes",
            "BQ": "Banque",
            "CA": "Caisse",
            "OD": "Operations diverses"
        }
    
    @staticmethod
    def get_auxiliaires():
        """Initialise les comptes auxiliaires (clients et fournisseurs)"""
        aux = {
            # Comptes auxiliaires fournisseurs
            "401": {
                "F00001": "DALKIA FRANCE",
                "F00002": "TELECOM SAS",
                "F00003": "FOURNITURES BUREAU DIRECT",
                "F00004": "PAPETERIE EXPRESS",
                "F00005": "BUREAU VERITAS",
                "F00006": "MAINTENANCE PRO",
                "F00007": "ASSURANCE GENERALI",
                "F00008": "TRANSPORT EXPRESS",
                "F00009": "NETTOYAGE SERVICE",
                "F00010": "ELECTRICITE DE FRANCE"
            },
            # Comptes auxiliaires clients
            "411": {
                "C00001": "CLIENT ALPHA",
                "C00002": "CLIENT BETA",
                "C00003": "CLIENT GAMMA",
                "C00004": "CLIENT DELTA",
                "C00005": "CLIENT EPSILON",
                "C00006": "CLIENT ZETA",
                "C00007": "CLIENT ETA",
                "C00008": "CLIENT THETA",
                "C00009": "CLIENT IOTA",
                "C00010": "CLIENT KAPPA"
            }
        }
        return aux
    
    @staticmethod
    def get_relevant_accounts(journal_code):
        """Retourne les comptes pertinents pour un journal donné"""
        # Récupération du plan comptable
        plan_comptable = AccountingData.get_plan_comptable()
        
        if journal_code == "AC":
            return [acc for acc in plan_comptable.keys() if acc.startswith(("60", "61", "62", "401"))]
        elif journal_code == "VE":
            return [acc for acc in plan_comptable.keys() if acc.startswith(("41", "70"))]
        elif journal_code == "BQ":
            return [acc for acc in plan_comptable.keys() if acc.startswith(("5", "40", "41", "6", "7"))]
        else:
            return list(plan_comptable.keys())
    
    @staticmethod
    def get_related_account(debit_account):
        """Retourne un compte cohérent avec le compte au débit"""
        # Récupération du plan comptable
        plan_comptable = AccountingData.get_plan_comptable()
        
        if debit_account.startswith("6"):  # Si débit sur charge
            return [acc for acc in plan_comptable.keys() if acc.startswith(("4", "5"))]
        elif debit_account.startswith("2"):  # Si débit sur immobilisation
            return [acc for acc in plan_comptable.keys() if acc.startswith(("404", "512"))]
        elif debit_account.startswith("401"):  # Si débit sur fournisseur
            return [acc for acc in plan_comptable.keys() if acc.startswith("5")]
        else:
            return [acc for acc in plan_comptable.keys() if not acc.startswith(debit_account[:3])]