from odoo import models, fields, api

class DossierJuridique(models.Model):
    _name = "dossier.juridique"
    _description = "Dossier Juridique"
    
    name = fields.Char(string="Nom du Dossier", required=True)
    description = fields.Text(string="Description")
    date_creation = fields.Date(string="Date de Création", default=fields.Date.today())
    
    statut = fields.Selection([
        ('en_cours', 'En Cours'),
        ('termine', 'Terminé'),
        ('rejete', 'Rejeté'),
    ], string="Statut", default='en_cours', required=True)
    
    # Utilisez une méthode au lieu d'une lambda dans le domaine
    def _get_avocat_domain(self):
        avocat_group = self.env.ref('cabinets_d\'avocats.group_avocat')
        return [('groups_id', 'in', [avocat_group.id])]
    
    def _get_client_domain(self):
        client_group = self.env.ref('cabinets_d\'avocats.group_client')
        return [('groups_id', 'in', [client_group.id])]
    
    avocat_id = fields.Many2one(
        "res.users",
        string="Avocat Responsable",
        domain=_get_avocat_domain,
        required=True
    )
    
    client_id = fields.Many2one(
        "res.users",
        string="Client Concerné",
        domain=_get_client_domain,
        required=True
    )
    
    def valider_dossier(self):
        """ Valider le dossier """
        self.write({'statut': 'termine'})
    
    def rejeter_dossier(self):
        """ Rejeter le dossier """
        self.write({'statut': 'rejete'})