from odoo import models, fields, api

class CabinetUser(models.Model):
    _name = "cabinet.user"
    _description = "Utilisateur Cabinet Avocats"
    
    name = fields.Char(string="Nom", required=True)
    email = fields.Char(string="Email", required=True)
    phone = fields.Char(string="Téléphone")
    
    x_role = fields.Selection([
        ('avocat', 'Avocat'),
        ('client', 'Client')
    ], string="Rôle", required=True)
    
    state = fields.Selection([
        ('draft', 'Brouillon'),
        ('validated', 'Validé'),
        ('rejected', 'Rejeté'),
    ], string="État", default="draft")
    
    user_id = fields.Many2one("res.users", string="Utilisateur Odoo", readonly=True)
    
    @api.model
    def create(self, vals):
        """ Crée un utilisateur Odoo et l'assigne au bon rôle """
        existing_user = self.env["res.users"].sudo().search([("login", "=", vals.get("email"))], limit=1)
        
        if existing_user:
            vals["user_id"] = existing_user.id
        else:
            user_vals = {
                "name": vals.get("name"),
                "login": vals.get("email"),
                "email": vals.get("email"),
                "phone": vals.get("phone"),
                # Ne pas ajouter x_role ici
            }
            
            new_user = self.env["res.users"].sudo().create(user_vals)
            vals["user_id"] = new_user.id
            
            # Assigner le groupe approprié en fonction du rôle
            if vals.get("x_role") == "avocat":
                avocat_group = self.env.ref('cabinets_d\'avocats.group_avocat')
                new_user.sudo().write({'groups_id': [(4, avocat_group.id)]})
            elif vals.get("x_role") == "client":
                client_group = self.env.ref('cabinets_d\'avocats.group_client')
                new_user.sudo().write({'groups_id': [(4, client_group.id)]})
        
        return super(CabinetUser, self).create(vals)
    
    def action_validate(self):
        """ Valide l'utilisateur et met son état à validé """
        for record in self:
            record.write({'state': 'validated'})
    
    def action_reject(self):
        """ Rejette l'utilisateur et met son état à rejeté """
        for record in self:
            record.write({'state': 'rejected'})