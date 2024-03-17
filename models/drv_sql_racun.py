from odoo import  models,fields,api,_
from odoo import tools

class SqlRacunln(models.Model):
    _name = 'drv.sql.racun' 
    _description = 'Query Racun'
    _auto = False   

    drv_racun_id = fields.Many2one(string="Racun",comodel_name="drv.racun")   # id od parent modela 
    drv_cena_final = fields.Float(string="Cena")
    drv_cena_id = fields.Many2one(string="Vrsta usluge",comodel_name="drv.cena")  
    drv_candidate_id = fields.Many2one(comodel_name='drv.candidate', string='Kandidat')  
    drv_datum_racuna = fields.Date(string='Datum računa')            


    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'drv_sql_racun')
        self.env.cr.execute("""
           create or replace view drv_sql_racun as (
            select row_number() OVER() as id, line.drv_racun_id, line.drv_cena_final,line.drv_cena_id,line.drv_candidate_id,line.drv_datum_racuna FROM (
                select   
                        ln.drv_racun_id as drv_racun_id,    
                        ln.drv_cena_final as drv_cena_final,
                        rn.drv_candidate_id as drv_candidate_id,
                        ln.drv_cena_id as  drv_cena_id ,
                        rn.drv_datum_racuna as drv_datum_racuna                                                                                                                                                              
                from
                    drv_racun_line ln 
                left join  drv_racun rn ON ln.drv_racun_id = rn.id  
                left join  drv_candidate cn ON cn.id = rn.drv_candidate_id 
                left join drv_cena ca ON ca.id = ln.drv_cena_id                                                                                                      
           ) line )""")
    #    for rec in self.env.cr.fetchall():
    #         print("Name is", rec[0])