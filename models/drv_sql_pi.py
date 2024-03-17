from odoo import  models,fields,api,_
from odoo import tools

class SqlPi(models.Model):
    _name = 'drv.sql.pi' 
    _description = 'Query praktični ispit'
    _auto = False   

    pi_parent_id = fields.Many2one(comodel_name='drv.pi',string='Praktični ispit')
    pi_candidate_id = fields.Many2one(comodel_name='drv.candidate',string='Kandidat')  
    pi_datum_prijave = fields.Char(string='Datum prijave')   
    pi_status = fields.Selection(string='Status',selection = [('ponisten','ISPIT PONIŠTEN'),('prijavljen','PRIJAVLJEN'),('nijepolozio','NIJE POLOZIO'),('odustao','ODUSTAO'),('polozio','POLOŽIO')], default='prijavljen')     
    pi_line_datumispita = fields.Date(string="Datum ispita")  
    vrsta_ispita = fields.Char(string='Vrsta ispita')           


    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'drv_sql_pi')
        self.env.cr.execute("""
           create or replace view drv_sql_pi as (
            select row_number() OVER() as id, line.pi_parent_id,line.pi_candidate_id, line.pi_datum_prijave, line.pi_status, line.pi_line_datumispita, line.vrsta_ispita FROM (
                select   
                        ln.pi_parent_id as pi_parent_id,
                        ln.pi_candidate_id as pi_candidate_id, 
                        TO_CHAR(ln.pi_datum_prijave::DATE,'dd.mm.yyyy') as pi_datum_prijave,  
                        ln.pi_status_candidate as pi_status,
                        pi.pi_dat as pi_line_datumispita,  
                        'PRAKTIČNI ISPIT' as vrsta_ispita                                                                                  
                from
                    drv_pi_line ln 
                left join  drv_pi pi ON ln.pi_parent_id = pi.id  
                left join  drv_candidate cn ON ln.pi_candidate_id = cn.id   
                ORDER BY pi_line_datumispita DESC                                                                           
           ) line )""")
    #    for rec in self.env.cr.fetchall():
    #         print("Name is", rec[0])