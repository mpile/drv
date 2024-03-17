from odoo import fields,models,api,_

class RacunLine(models.Model):
    _name = 'drv.racun.line'
    _description = 'Uplate kandidata stavka'

    drv_racun_id = fields.Many2one(string="Racun",comodel_name="drv.racun")
    drv_cena_id = fields.Many2one(string="Vrsta usluge",comodel_name="drv.cena", required = True)
    drv_cena_final = fields.Float(string="Iznos",required = True)
    drv_cena_kol = fields.Integer(string="Količina", default = 1, required = True)
    drv_jmere = fields.Selection(string="Jedinica mere", selection=[('A','Kom')], required = True, default='A')
    drv_stara_sifra = fields.Integer(string="Stara šifra")
    drv_stara_sifra_usluge = fields.Integer(string="Stara šifra usluge")    