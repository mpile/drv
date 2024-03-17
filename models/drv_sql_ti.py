from odoo import  models,fields,api,_
from odoo import tools

class SqlTi(models.Model):
    _name = 'drv.sql.ti' 
    _description = 'Query teorijski ispit'
    _auto = False   

    ti_parent_id = fields.Many2one(comodel_name='drv.ti',string='Teorijski ispit')
    ti_candidate_id = fields.Many2one(comodel_name='drv.candidate',string='Kandidat')  
    datum_prijave = fields.Char(string='Datum prijave')   
    status = fields.Selection(string='Status',selection = [('ponisten','ISPIT PONIŠTEN'),('prijavljen','PRIJAVLJEN'),('nijepolozio','NIJE POLOZIO'),('odustao','ODUSTAO'),('polozio','POLOŽIO')], default='prijavljen')         
    sql_dat = fields.Date(string="Datum ispita")  
    vrsta_ispita = fields.Char(string='Vrsta ispita')        


    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'drv_sql_ti')
        self.env.cr.execute("""
           create or replace view drv_sql_ti as (
            select row_number() OVER() as id, line.ti_parent_id,line.ti_candidate_id, line.datum_prijave, line.status, line.sql_dat, line.vrsta_ispita FROM (
                select   
                        ln.ti_parent_id as ti_parent_id,
                        ln.ti_candidate_id as ti_candidate_id, 
                        TO_CHAR(ln.datum_prijave::DATE,'dd.mm.yyyy') as datum_prijave,  
                        ln.status as status,
                        ti.dat as sql_dat, 
                        'TEORIJSKI ISPIT' as vrsta_ispita                                                   
                from
                    drv_ti_line ln 
                left join  drv_ti ti ON ln.ti_parent_id = ti.id  
                left join  drv_candidate cn ON ln.ti_candidate_id = cn.id  
                union ALL
                select   
                        ln.pi_parent_id as ti_parent_id,
                        ln.pi_candidate_id as ti_candidate_id, 
                        TO_CHAR(ln.pi_datum_prijave::DATE,'dd.mm.yyyy') as datum_prijave,  
                        ln.pi_status_candidate as status,
                        pi.pi_dat as sql_dat, 
                        'PRAKTIČNI ISPIT' as vrsta_ispita                                                                                   
                from
                    drv_pi_line ln 
                left join  drv_pi pi ON ln.pi_parent_id = pi.id  
                left join  drv_candidate cn ON ln.pi_candidate_id = cn.id     
                ORDER BY sql_dat DESC                                                                                                                                                            
           ) line )""")
    #    for rec in self.env.cr.fetchall():
    #         print("Name is", rec[0])