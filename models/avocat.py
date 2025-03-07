from odoo import models, fields

class Avocat(models.Model):
    _name = "avocat"
    _description = "Avocat"

    name = fields.Char(string="Nom", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Téléphone")
