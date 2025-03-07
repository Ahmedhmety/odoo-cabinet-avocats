{
    "name": "Cabinet d'Avocats",
    "version": "1.0",
    "depends": ["base"],
    "author": "Ahmed Hmety",
    "category": "Gestion Légale",
    "summary": "Gestion des dossiers juridiques, des clients et des avocats",
    "description": """Ce module permet aux cabinets d'avocats de gérer leurs dossiers, clients et paiements.""",
    "data": [
        "security/security.xml", 
        "security/ir.model.access.csv",
        "views/dossiers_views.xml",
        "views/users_views.xml",
    ],
    "application": True,
    "installable": True,

}
