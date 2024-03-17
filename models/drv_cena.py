from odoo import fields,models,api

class Cenovnik(models.Model):
    _name = 'drv.cena'
    _description = 'Cenovnik usluga'

    name = fields.Char(string='Naziiv usluge', required=True)
    drv_cena_bez_poreza = fields.Float(string='Cena bez poreza')
    drv_procenat = fields.Float(string='Procenat poreza')
    drv_porez = fields.Float(string='Porez')
    drv_cena_sa_porezom = fields.Float(string='Cena sa porezom')    
    drv_moto_cas = fields.Boolean(string="Moto čas")
    dvr_aktivna = fields.Boolean(string="Usluga je aktivna")
    drv_redosled = fields.Integer(string="Redosled")
    drv_prijava = fields.Boolean(string="Prijava ispita")
    drv_jed_mere = fields.Char(string="Jedinica mere")
    drv_sifra_stara = fields.Integer(string="Šifra stara")