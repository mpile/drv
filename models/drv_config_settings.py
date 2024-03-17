from odoo import models,fields,api

class DrvConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    drv_prvi_clan = fields.Char(string='Prvi ćlan komisije je iz:', config_parameter = 'drv.drv_prvi_clan')
    message = fields.Char(string="Poruka")


    def get_values(self):
        res = super(DrvConfigSettings, self).get_values()
        res.update(
            drv_prvi_clan = self.env['ir.config_parameter'].sudo().get_param('drv.drv_prvi_clan')
        )
        return res


    def set_values(self):
        super(DrvConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()

        field1 = self.drv_prvi_clan and self.drv_prvi_clan or False


        param.set_param('drv.drv_prvi_clan', field1)
