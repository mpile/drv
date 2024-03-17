from odoo import  models,fields,api,_
from datetime import datetime

class TeorijskiIspitLine(models.Model):
    _name = 'drv.ti.line'
    _description = 'Stavka teorijski ispit'

    ti_parent_id = fields.Many2one(comodel_name='drv.ti',string='Teorijski ispit')
    ti_candidate_id = fields.Many2one(comodel_name='drv.candidate',string='Kandidat')
    ti_parent_id_id = fields.Integer(related='ti_parent_id.id',string='Id spiska')
    ti_id_kandidata = fields.Char(string='Stari id Kandidata')
    datum_prijave = fields.Date(string='Datum prijave',default=fields.Date.today)    
    sifra = fields.Integer(string='Sifra')
    ti_datum_rodjenja = fields.Date(string='Datum rodjenja', related='ti_candidate_id.datum_rodjenja', store=True)
    ti_id_number_inside_year = fields.Integer(string='Broj', related='ti_candidate_id.number_inside_year', store = True)
    ti_id_godina = fields.Char(string='Godina', related='ti_candidate_id.godina', store = True)  
    ti_id_candidate = fields.Char(string="Id kandidata", compute = '_compute_id_drv', store = True) 
    ti_id_drv_category = fields.Selection(string='Kategorija', related='ti_candidate_id.drv_category', store = True)  
    ti_id_datum_upisa = fields.Date(string='Datuum upisa', related='ti_candidate_id.datum_upisa', store = True)  
    ti_id_brlk = fields.Char(string = 'Broj lične karte',related='ti_candidate_id.brlk', store = True)  
    ti_id_pu = fields.Char(string = 'Mesto izdavanja',related='ti_candidate_id.pu', store = True)
    status =  fields.Selection(string='Status',selection = [('ponisten','ISPIT PONIŠTEN'),('prijavljen','PRIJAVLJEN'),('nijepolozio','NIJE POLOZIO'),('odustao','ODUSTAO'),('polozio','POLOŽIO')], default='prijavljen')         
    ti_line_brlk_pu = fields.Char(compute='_compute_brlk_pu')   
    ti_line_brojlekarskog = fields.Char(string='Broj lekarskog', related='ti_candidate_id.broj_lekarskog', store=True)
    ti_line_datumlekarskogod = fields.Date(string='Datum lekarskog', related='ti_candidate_id.datum_lekarskog_od', store = True)  
    ti_line_lekarsko = fields.Char(string='Lekarsko', compute='_daj_lekarsko', store = True)  
    ti_line_brojpolaganja = fields.Integer(string="Broj polaganja", store=True)
    ti_line_brojpoena = fields.Char(string="Ostvaren broj poena", default=1, store = True)  
    ti_line_datumispita = fields.Date(related ='ti_parent_id.dat', string='Datum ispita', store=True)


    def _daj_lekarsko(self):
        for rec in self:
            if (rec.ti_line_brojlekarskog and rec.ti_line_datumlekarskogod):
                rec.ti_line_lekarsko= rec.ti_line_brojlekarskog + ' ' + rec.ti_line_datumlekarskogod.strftime("%d.%m.%Y") 
            else:
                rec.ti_line_lekarsko = ''

    def _compute_brlk_pu(self):
        for rec in self:
            if (rec.ti_id_brlk and rec.ti_id_pu):
                rec.ti_line_brlk_pu = rec.ti_id_brlk + ' ' + rec.ti_id_pu
            else:
                rec.ti_line_brlk_pu = ''



    @api.depends('ti_id_godina')
    def _compute_id_drv(self):
        for candidate in self:
            if ( candidate.ti_id_number_inside_year and candidate.ti_id_godina):
                candidate.ti_id_candidate = str(candidate.ti_id_number_inside_year) + '/' + candidate.ti_id_godina 
            else:
                candidate.ti_id_candidate = ''

