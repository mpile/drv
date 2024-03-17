from odoo import  models,fields,api,_
from odoo import tools

class SqlSvjed(models.Model):
    _name = 'drv.sql.svjed' 
    _description = 'Query svjedočanstva'
    _auto = False   

    svjed_parent_id = fields.Many2one(comodel_name='drv.pi',string='Praktični ispit')
    svjed_candidate_id = fields.Many2one(comodel_name='drv.candidate',string='Kandidat')     
    svjed_drv_category = fields.Selection(string='Kategorija', related='svjed_candidate_id.drv_category', store = True) 
    svjed_number = fields.Integer(string='Broj u godini', related='svjed_candidate_id.number_inside_year', store = True)       
    svjed_godina = fields.Char(string='Godina', related='svjed_candidate_id.godina', store = True)  
    svjed_id_candidate = fields.Char(string='Id kandidata',compute='_compute_id_svjed') 
    svjed_datum = fields.Date('Datum izdavanja', related='svjed_parent_id.pi_dat')


    def _compute_id_svjed(self):
        for candidate in self:
            if (candidate.id and candidate.svjed_number  and candidate.svjed_godina):
                 candidate.svjed_id_candidate = str(candidate.svjed_number) + '/' + candidate.svjed_godina
            else:
                candidate.svjed_id_candidate= ''     

    def init(self):
        tools.drop_view_if_exists(self.env.cr, 'drv_sql_svjed')        
        self.env.cr.execute("""  
                create or replace view drv_sql_svjed as ( 
                SELECT row_number() OVER() as id, line.svjed_parent_id, line.svjed_candidate_id, line.svjed_drv_category, line.svjed_number, line.svjed_godina, line.svjed_datum FROM (
                SELECT
                        ln.pi_parent_id as svjed_parent_id,
                        ln.pi_candidate_id as svjed_candidate_id,
                        ln.pi_id_drv_category as svjed_drv_category,
                        cn.number_inside_year as svjed_number,
                        cn.godina as svjed_godina,
                        pi.pi_dat as svjed_datum
                FROM drv_pi_line ln 
                LEFT JOIN drv_pi pi ON ln.pi_parent_id = pi.id
                LEFT JOIN drv_candidate cn ON ln.pi_candidate_id = cn.id
                WHERE ln.pi_status_candidate = 'polozio') line )""")