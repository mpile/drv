from odoo import  models,fields,api,_

class PrakticniIspit(models.Model):
    _name = 'drv.pi'
    _description = 'Praktični ispit'
    _order = "pi_dat desc"    

    pi_dat = fields.Date(string='Datum polaganja',default=fields.Date.today, required=True)
    name = fields.Char(compute='_izracunaj', required=True)
    pi_stara_sifra = fields.Integer(string='Sifra')
    pi_status = fields.Selection(selection=[('1','ISPIT JE U PRIPREMI'),('2','ISPIT JE ZAVRŠEN')],default = '1',string='Status praktičnog ispita ispita')
    pi_child_ids = fields.One2many(comodel_name='drv.pi.line',inverse_name='pi_parent_id',string='Stavke')
    pi_prvi_clan = fields.Char(string="Prvi član komisije", store = False, default = lambda self:self._get_prvi_clan())  
    svjed_child_ids = fields.One2many(comodel_name='drv.sql.svjed',inverse_name='svjed_parent_id',string='Svjedočanstva')      

    def _get_prvi_clan(self):
        value = self.env['ir.config_parameter'].get_param('drv.drv_prvi_clan')
        return value

    @api.depends('pi_dat')
    def _izracunaj(self):
        for record in self:
            record.name = fields.Date.from_string(
                record.pi_dat).strftime('%d.%m.%Y')
            
    def pi_uradi_update(self):
        sql = """ 
                update drv_pi_line b
                set pi_parent_id = a.id
                from 
                drv_pi a
                where 
                a.pi_stara_sifra = b.sifra """
        self.env.cr.execute(sql)   

    def pi_update_kandidati(self):
        sql = """ 
                update drv_pi_line b
                    set pi_candidate_id = a.id,
                    pi_line_brojlekarskog = a.broj_lekarskog,
                    pi_line_datumlekarskogod = a.datum_lekarskog_od,
                    pi_id_brlk = a.brlk, 
                    pi_id_pu = a.pu,
                    pi_datum_rodjenja = a.datum_rodjenja,                    
                    pi_id_drv_category = a.drv_category                                                          
                from 
                    drv_candidate a
                where 
                    trim(a.id_candidate) = trim(b.pi_id_kandidata) """
        self.env.cr.execute(sql)                 