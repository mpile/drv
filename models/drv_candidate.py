# Copyright 2016-2018 Akretion (http://www.akretion.com)
# @author: Alexis de Lattre <alexis.delattre@akretion.com>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

import logging
from odoo import fields, models,api
from datetime import datetime,timedelta,date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import ValidationError

logger = logging.getLogger(__name__)

class ResCandidate(models.Model):
    _name = "drv.candidate"
    _description = 'Kandidat'
    _order = "name, datum_upisa desc,id"
    _rec_names_search = ['name']  # TODO vat must be sanitized the same way for storing/searching
    
    
    ime = fields.Char(string = 'Ime', required = True)
    prezime = fields.Char(string = 'Prezime', required = True, index = True)
    ime_roditelja = fields.Char(string = 'Ime roditelja')
    id_candidate = fields.Char(string="Id kandidata", compute = '_compute_id_drv', store = True) 
    number_inside_year = fields.Integer(string="Broj u godini", required = True, default= lambda self:self.get_default_no())  
    godina = fields.Char(string="Godina", default = lambda self:self.get_default_year()) 
    datum_upisa = fields.Date(string='Datum upisa', default = lambda self:self.get_default_date(), required = True, index = True)
    drv_category = fields.Selection(string='Kat',default='B',selection = [('A','A'),('AM','AM'),('A1','A1'),('A2','A2'),('B','B'),('B1','B1'),('BE','BE'),('C','C'),('C1','C1'),('C1E','C1E'),
                                                 ('CE','CE'),('D','D'),('D1','D1'),('D1E','D1E'),('DE','DE'),('F','F'),('M','M'),('E','E')], required=True)  
    datum_rodjenja = fields.Date(string='Datum rodjenja', default = lambda self:self.get_default_date())   
    mesto_rodjenja = fields.Char(string = 'Mesto rodjenja') 
    brlk = fields.Char(string = 'Broj lične karte', store = True)
    pu = fields.Char(string = 'Policijska uprava')  
    jmbg = fields.Char(string = 'Maticni broj') 
    adresa_stanovanja = fields.Char(string="Adresa")
    mesto_stanovanja = fields.Char(string="Mesto")
    drzavljanin = fields.Char(string='Državljanstvo')
    telefon_mobilni = fields.Char(string='Telefon mobilni')
    telefon_fiksni = fields.Char(string='Telefon fiksni') 
    email = fields.Char(string='E-mail')  
    company_id = fields.Many2one('res.company', string='Company',  required=True,    default=lambda self: self.env.user.company_id)      
    name = fields.Char(compute='_asignar_nombre', required=True, index = True, store=False)   
    broj_lekarskog = fields.Char(string='Broj lekarskog uverenja')
    datum_lekarskog_od = fields.Date(string='Datum izdavanja lekarskog uverenja', default = lambda self:self.get_default_date()) 
    vazenje_lekarskog = fields.Integer(string='Vaćenje u mesecima', default=12)    
    datum_lekarskog_do = fields.Date(string='Datum do kada važi lekarsko')
    lekarsko_izdala_ustanova = fields.Char(string='Lekarsko izdala ustanova') 
    ti_line_childs = fields.One2many(comodel_name='drv.sql.ti',inverse_name='ti_candidate_id',string='Prijave teorijskog ispita')   
    instruct_id = fields.Many2one('drv.instruct', string='Instruktor') 
    datum_po_od = fields.Date(string='Datum praktične obuke od')     
    datum_po_do = fields.Date(string='Datum praktične obuke do') 
    broj_casova_po = fields.Integer(string='Broj časova praktične obuke', default=20)     
    datum_polozio_teoriju = fields.Date(string='Položio teoriju') 
    dosao = fields.Boolean(string="Došao iz druge auto Škola", default=False) 
    ispisan = fields.Boolean(string="Ispisan", default=False) 
    vec_ima_polozeno = fields.Many2many(comodel_name='drv.cat')  
    komentar = fields.Char(string="komentar") 
    datum_polozio_voznju = fields.Date(string='Položio vozžnju') 
    pi_line_childs = fields.One2many(comodel_name='drv.sql.pi',inverse_name='pi_candidate_id',string='Prijave praktičnog ispita')   
    rn_line_childs = fields.One2many(comodel_name='drv.sql.racun',inverse_name='drv_candidate_id',string='Uplate kandidata')  
    image = fields.Binary(string="Slika kandidata")      
    datum_to_od = fields.Date(string='Datum teorijske obuke od')     
    datum_to_do = fields.Date(string='Datum teorijske obuke do') 
    broj_casova_to = fields.Integer(string='Broj časova teorijske obuke')     
                
        
    @api.onchange('datum_lekarskog_od','vazenje_lekarskog')
    def _compute_lekarsko_do(self):
        self.datum_lekarskog_do = self.datum_lekarskog_od + relativedelta(months=self.vazenje_lekarskog)  

    @api.onchange('datum_po_od','datum_po_do')
    def _get_two_date_comp(self):
        if  (self.datum_po_od ):
            start_date = self.datum_po_od.strftime('%Y-%m-%d')
            if (self.datum_po_do):
                end_date = self.datum_po_do.strftime('%Y-%m-%d')
                if start_date > end_date:
                    raise ValidationError("Datum praktične obuke od ne može biti veći od datuma praktične obuke do !!!'")
            else:
                return
        else:
            return
        
    def _provera_na_datume(self):
         if ( self.datum_po_do > self.datum_po_od ):
            multiline_string = 'Datum praktične obuke od moda biti manji od datuma praktične obuke do'             
            notification = {'type': 'ir.actions.client','tag': 'display_notification','params': {'title': 'Test podaci za izabranu fakturu',
                'message': multiline_string,
                'type':'danger',  #types: success,warning,danger,info
                'sticky': True,  #True/False will display for few seconds if false
                }
            }        

            # return notification  
            return notification  
         
    @api.depends('prezime','ime_roditelja', 'ime')
    def _asignar_nombre(self):
        print("usao u compute")
        for record in self:
            if (record.ime_roditelja):
                record.name = record.prezime + ' (' + record.ime_roditelja + ') ' +  record.ime 
            else:
                 record.name = record.prezime + ' (' +  ') ' +  record.ime 
        


    @api.depends('godina')
    def _compute_id_drv(self):
        for candidate in self:
            if (candidate.id and candidate.number_inside_year and candidate.godina):
                 candidate.id_candidate = str(candidate.number_inside_year) + '/' + candidate.godina 
            else:
                candidate.id_candidate = ''

    @api.depends('godina')
    def _calculate_drv(self):
        new = 0            
        return new + 1    
            
    def get_default_no(self):
        new = 700   
        godina = 2024         
        return new + 1   
        
    @api.model
    def get_default_year(self):
        return str(datetime.now().year)
    
    @api.model
    def get_default_date(self):
        return datetime.now()   
    
    @api.onchange('datum_upisa')
    def onchange_datum_upisa(self):
        if self.datum_upisa:
            godina = self.datum_upisa.year
            broj_u_god=self.next_num()
            self.number_inside_year =  broj_u_god         
            self.godina = godina  

    def next_num(self):
        args = {'godina': str(self.datum_upisa.year)}
        sql = """ select Max(number_inside_year) as max_num from drv_candidate dc where dc.godina = %(godina)s """   
        self.env.cr.execute(sql,args)  
        fetched_data = self.env.cr.dictfetchall()
        cifra = 0
        if  fetched_data:
            for key,value in fetched_data[0].items():
                if  (key == 'max_num'):
                    if ( value is None ):
                     cifra = 1                          
                    else:                        
                        cifra = value  + 1   
                else:
                     cifra = 1                                                 
        return cifra    
    



