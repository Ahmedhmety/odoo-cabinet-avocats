from odoo import models, fields, api
from datetime import timedelta

class DossierJuridique(models.Model):
    _name = "dossier.juridique"
    _description = "Dossier Juridique"
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Ajouter la fonctionnalité de messagerie
    
    name = fields.Char(string="Nom du Dossier", required=True, tracking=True)
    description = fields.Text(string="Description", tracking=True)
    date_creation = fields.Date(string="Date de Création", default=fields.Date.today(), tracking=True)
    
    # Nouveaux champs
    titre = fields.Char(string="Titre de l'affaire", tracking=True)
    date_echeance = fields.Date(string="Date d'échéance", tracking=True)
    date_cloture = fields.Date(string="Date de clôture", readonly=True, tracking=True)
    
    statut = fields.Selection([
        ('en_cours', 'En Cours'),
        ('termine', 'Terminé'),
        ('rejete', 'Rejeté'),
    ], string="Statut", default='en_cours', required=True, tracking=True)
    
    etape = fields.Selection([
        ('reception', 'Réception'),
        ('analyse', 'Analyse'),
        ('preparation', 'Préparation'),
        ('procedure', 'Procédure'),
        ('jugement', 'Jugement'),
        ('post_jugement', 'Post-Jugement'),
        ('archivage', 'Archivage')
    ], string="Étape", default='reception', tracking=True)
    
    type_affaire = fields.Selection([
        ('civil', 'Civil'),
        ('penal', 'Pénal'),
        ('commercial', 'Commercial'),
        ('social', 'Social'),
        ('administratif', 'Administratif'),
        ('famille', 'Droit de la famille'),
        ('immobilier', 'Immobilier'),
        ('autre', 'Autre')
    ], string="Type d'affaire", tracking=True)
    
    priorite = fields.Selection([
        ('0', 'Normale'),
        ('1', 'Basse'),
        ('2', 'Moyenne'),
        ('3', 'Haute'),
        ('4', 'Très haute')
    ], string="Priorité", default='0', tracking=True)
    
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
        required=True,
        tracking=True
    )
    
    client_id = fields.Many2one(
        "res.users",
        string="Client Concerné",
        domain=_get_client_domain,
        required=True,
        tracking=True
    )
    
    # Nouveaux champs pour juridiction et tribunal
    juridiction = fields.Char(string="Juridiction", tracking=True)
    tribunal = fields.Char(string="Tribunal", tracking=True)
    numero_affaire = fields.Char(string="Numéro d'affaire tribunal", tracking=True)
    
    # Facturation
    honoraires = fields.Float(string="Honoraires", tracking=True)
    
    # Notes et documents
    notes = fields.Text(string="Notes internes")
    
    # Calcul de la durée du dossier
    duree_jours = fields.Integer(string="Durée (jours)", compute='_compute_duree', store=True)
    
    def valider_dossier(self):
        """ Valider le dossier """
        self.write({
            'statut': 'termine',
            'date_cloture': fields.Date.today()
        })
    
    def rejeter_dossier(self):
        """ Rejeter le dossier """
        self.write({
            'statut': 'rejete',
            'date_cloture': fields.Date.today()
        })
    
    # Calculs automatiques
    @api.depends('date_creation', 'date_cloture')
    def _compute_duree(self):
        for dossier in self:
            if dossier.date_creation:
                end_date = dossier.date_cloture or fields.Date.today()
                delta = end_date - dossier.date_creation
                dossier.duree_jours = delta.days
            else:
                dossier.duree_jours = 0
    
    # Création automatique d'une date d'échéance +30 jours par défaut
    @api.onchange('date_creation')
    def _onchange_date_creation(self):
        if self.date_creation and not self.date_echeance:
            self.date_echeance = self.date_creation + timedelta(days=30)