from odoo import fields,models,api,_
from datetime import datetime

class Racun(models.Model):
    _name = 'drv.racun'
    _description = 'Uplata kandidata'
    _order = 'drv_datum_racuna desc'

    drv_datum_racuna = fields.Date(string='Datum računa', required= True, default = lambda self:self.get_default_date())
    drv_candidate_id = fields.Many2one(comodel_name='drv.candidate', string='Kandidat')
    drv_stari_id_kandidata = fields.Char(string='Stari id kandidata')
    drv_broj_racuna = fields.Integer(string="Stari broj racuna")
    drv_racun_ids = fields.One2many(comodel_name="drv.racun.line", inverse_name="drv_racun_id", string="Stavke")
    name = fields.Char(string = 'Broj računa', readonly = True)

    @api.model
    def get_default_date(self):
        return datetime.now()   

    @api.model # neopodan dekorater
    def create(self,vals): # metoda koja se aktivira kada se klikne na dugme Novi
        vals['name']=self.env['ir.sequence'].next_by_code("drv_racun.refseq") # dodeljivanje vrednosti iz ir. sequnce , funkcija je next_by_code
        ref = super(Racun,self).create(vals)
        return ref

    def update_drv_kandidati(self):
        sql = """ update drv_racun  b
                    set drv_candidate_id = a.id
                from 
                    drv_candidate a
                where 
                trim(a.id_candidate) = trim(b.drv_stari_id_kandidata) """
        self.env.cr.execute(sql)

    def update_drv_cenovnik(self):
        sql = """ update drv_racun_line  b
                    set drv_cena_id  = a.id
                    from  drv_cena a
                    where 
                    a.drv_sifra_stara  = b.drv_stara_sifra_usluge """
        self.env.cr.execute(sql)   

    def update_drv_stavke(self):   
        sql =""" update drv_racun_line b
                    set drv_racun_id = a.id
                    from drv_racun a
                    where 
                    a.drv_broj_racuna = b.drv_stara_sifra""" 
        self.env.cr.execute(sql)                