from odoo import models, fields


class EffectiveDateWizard(models.TransientModel):
    _name = 'effective.date.wizard'
    _description = 'Effective Date Wizard'

    effective_date = fields.Datetime(string='Effective Date')
    apply_effective_date = fields.Boolean(
        string='Apply to other stock picking')

    def change_effective_date(self):
        record = (self.env['stock.picking'].browse(
            [self._context.get('active_id')]))
        record.write({'date_done': self.effective_date})
        move_rec = self.env['stock.valuation.layer'].search(
            [('reference', '=', record.name)])
        valuation_rec = self.env['stock.move.line'].search(
            [('reference', '=', record.name)])
        journal = self.env['account.move'].search(
            [('ref', 'ilike', record.name)])
        move_rec.write({'create_date': self.effective_date})
        move_rec = self.env['stock.move'].search(
            [('picking_id', '=', record.id)])
        query = """ UPDATE stock_valuation_layer 
                    SET create_date = '%s' WHERE 
                    stock_move_id = %s""" % (self.effective_date, move_rec.id)
        self.env.cr.execute(query)
        valuation_rec.sudo().write({'date': self.effective_date})
        journal.write({'date': self.effective_date})
        if self.apply_effective_date:
            orders = self.env['stock.picking'].search(
                [('origin', '=', record.origin)])
