from odoo import fields,models

class DrvCat(models.Model):
    _name = 'drv.cat'
    _description = 'Kategorije'

    name=fields.Char(string='Kategorija')