from odoo import models, fields

class Client(models.Model):
    _name = "client"
    _description = "Client"

    name = fields.Char(string="Nom", required=True)
    email = fields.Char(string="Email")
    phone = fields.Char(string="Téléphone") 