from odoo import  models,fields,api,_

class Instruktor(models.Model):
    _name = 'drv.instruct'
    _description = 'Instruktor'


    instruct_ime = fields.Char(string='Ime instruktora', required=True)
    instruct_prezime = fields.Char(string='Prezime instruktora', required=True)    
    name = fields.Char(compute='_compute_instruct_name', required=True)
    instruct_status = fields.Selection(selection=[('1','AKTIVAN'),('2','NEAKTIVAN')],default = '1',string='Status')

    def _compute_instruct_name(self):
        for record in self:
            if (record.instruct_ime and record.instruct_prezime):
                record.name = record.instruct_ime + ' ' + record.instruct_prezime
            else:
                record.name = "Nekompletni podaci"