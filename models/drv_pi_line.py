from odoo import  models,fields,api
from odoo.exceptions import ValidationError
from datetime import datetime,timedelta,date

class PrakticniIspitLine(models.Model):
    _name = 'drv.pi.line'
    _description = 'Stavka praktični ispit'

    pi_parent_id = fields.Many2one(comodel_name='drv.pi',string='Praktični ispit')
    pi_candidate_id = fields.Many2one(comodel_name='drv.candidate',string='Kandidat', required = True)
    pi_parent_id_id = fields.Integer(related='pi_parent_id.id',string='Id spiska')
    pi_id_kandidata = fields.Char(string='Stari id Kandidata')  
    sifra = fields.Integer(string='Sifra')
    pi_id_drv_category = fields.Selection(string='Kategorija', related='pi_candidate_id.drv_category', store = True)      
    pi_datum_rodjenja = fields.Date(string='Datum rodjenja', related='pi_candidate_id.datum_rodjenja', store=True)
    pi_line_brojlekarskog = fields.Char(string='Broj lekarskog', related='pi_candidate_id.broj_lekarskog', store = True)
    pi_line_datumlekarskogod = fields.Date(string='Datum lekarskog', related='pi_candidate_id.datum_lekarskog_od', store = True)  
    pi_line_brojpolaganja = fields.Integer(string="Broj polaganja", default = 1)    
    pi_status_candidate = fields.Selection(string='Status',selection = [('prijavljen','PRIJAVLJEN'),('nijepolozio','NIJE POLOZIO'),('odustao','ODUSTAO'),('polozio','POLOŽIO')], store = True, default='prijavljen') 
    pi_id_brlk = fields.Char(string = 'Broj lične karte',related='pi_candidate_id.brlk', store = True)  
    pi_id_pu = fields.Char(string = 'Mesto izdavanja',related='pi_candidate_id.pu', store = True) 
    pi_id_drv_category = fields.Selection(string='Kategorija', related='pi_candidate_id.drv_category', store = True)  
    pi_datum_rodjenja = fields.Date(string='Datum rodjenja', related='pi_candidate_id.datum_rodjenja', store=True)    
    pi_datum_prijave = fields.Date(string='Datum prijave',default=fields.Date.today)   
    pi_id_broj = fields.Char(string = "brlk") 
    pi_line_lekarsko = fields.Char(string='Lekarsko', compute='_daj_lekarsko', store = True) 
    pi_line_datum_po_od = fields.Date(string='Datum praktične obuke od', related='pi_candidate_id.datum_po_od', store = True)      
    pi_line_datum_po_do = fields.Date(string='Datum praktične obuke do', related='pi_candidate_id.datum_po_do', store = True)  
    pi_line_broj_casova_po = fields.Integer(string='Broj časova praktične obuke', related='pi_candidate_id.broj_casova_po', store = True)      
    pi_line_datumpolt = fields.Date(string='Polozio teoriju', related='pi_candidate_id.datum_polozio_teoriju', store = True) 
    pi_line_datumispita = fields.Date(related ='pi_parent_id.pi_dat', string='Datum ispita', store=True)     


    @api.onchange('pi_status_candidate')
    def _upisi_polozio_voznju(self):
        status = self.pi_status_candidate # status npr polozio     
        datum = self.pi_parent_id.pi_dat.strftime('%Y-%m-%d') # datum polaganja
    #    datum = datetime.today().strftime('%Y-%m-%d') # datum polaganja
        id_kandidata = int(self.pi_candidate_id.id)
        print(dict(self._fields['pi_status_candidate'].selection).get(self.pi_status_candidate))  
        args = {'datum':datum,'id_kandidata': id_kandidata}
        sql_polozio = """ update drv_candidate set datum_polozio_voznju = %(datum)s where id = %(id_kandidata)s"""        
        if (status == 'polozio'):          
            self.env.cr.execute(sql_polozio,args)
        else:
            sql_nije_polozio = """ update drv_candidate set datum_polozio_voznju = NULL where id = %(id_kandidata)s"""              
            self.env.cr.execute(sql_nije_polozio,args)

    @api.onchange('pi_line_brojpolaganja')
    def _valid_broj(self):
        if not ( self.pi_line_brojpolaganja > 0 ):
            raise ValidationError("Redni broj polaganja treba da bude veći od nule!!!'") 
    
    @api.onchange('pi_candidate_id')
    def _izracunaj_broj_polaganja (self):
        cifra = 0
        if  self.pi_candidate_id:
            id_kandidata = int(self.pi_candidate_id.id)
            self.pi_line_brojpolaganja = 1  
            args = {'id_kandidata':id_kandidata}
            sql = """ select Count(id) as count_num from drv_pi_line ln where ln.pi_candidate_id = %(id_kandidata)s"""
            self.env.cr.execute(sql,args)
            fetched_data = self.env.cr.dictfetchall()
            for key,value in fetched_data[0].items():
                if  (key == 'count_num'):
                    if ( value is None ):
                     cifra = 1                          
                    else:                        
                        cifra = value  + 1   
                else:
                     cifra = 1   
            self.pi_line_brojpolaganja = cifra                                 
        else:
            self.pi_line_brojpolaganja = 1                   
    
    def _daj_lekarsko(self):
        for rec in self:
            if (rec.pi_line_brojlekarskog and rec.pi_line_datumlekarskogod):
                rec.pi_line_lekarsko= rec.pi_line_brojlekarskog + ' ' + rec.pi_line_datumlekarskogod.strftime("%d.%m.%Y") 
            else:
                rec.pi_line_lekarsko = ''                  
