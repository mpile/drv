from odoo import  models,fields,api,_
import base64

class TeorijskiIspit(models.Model):
    _name = 'drv.ti'
    _description = 'Teorijski ispit'
    _order = "dat desc"    

    dat = fields.Date(string='Datum polaganja',default=fields.Date.today, required=True)
    name = fields.Char(compute='_izracunaj', required=True)
    sifra = fields.Integer(string='Sifra')
    ti_child_ids = fields.One2many(comodel_name='drv.ti.line',inverse_name='ti_parent_id',string='Stavke')
    ti_status = fields.Selection(selection=[('1','ISPIT JE U PRIPREMI'),('2','ISPIT JE ZAVRŠEN')],default = '1',string='Status teorijskog ispita')

    @api.depends('dat')
    def _izracunaj(self):
        for record in self:
            record.name = fields.Date.from_string(
                record.dat).strftime('%d.%m.%Y')
            
    def uradi_update(self):
        sql = """ 
                update drv_ti_line b
                set ti_parent_id = a.id
                from 
                drv_ti a
                where 
                a.sifra = b.sifra """
        self.env.cr.execute(sql)

    def update_kandidati(self):
        sql = """ 
                update drv_ti_line b
                    set ti_candidate_id = a.id, ti_datum_rodjenja = a.datum_rodjenja, ti_id_datum_upisa = a.datum_upisa, 
                    ti_id_drv_category = a.drv_category, ti_id_brlk = a.brlk, ti_id_pu = a.pu,
                    ti_line_brojlekarskog = a.broj_lekarskog,
                    ti_line_datumlekarskogod = a.datum_lekarskog_od
                from 
                    drv_candidate a
                where 
                    trim(a.id_candidate) = trim(b.ti_id_kandidata) """
        self.env.cr.execute(sql)

    def get_report(self):
        sql = """ 
                select res_model * from ir_attachment where name = 'Testovi-24.11.2023.pdf'
                  """
        self.env.cr.execute(sql)

    def action_get_attachment(self):
            pdf = self.env.ref('drv.ti_report_action')._render_qweb_pdf(self.ids)
            b64_pdf = base64.b64encode(pdf[0])
            name = "MyAttachment"
            return self.env['ir.attachment'].create({
                'name': name,
                'type': 'binary',
                'datas': b64_pdf,
                # 'datas_fname': name + '.pdf',
                'store_fname': name,
                'res_model': self._name,
                'res_id': self.id,
                'mimetype': 'application/x-pdf'
            })                        

                    