# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import fields, models, api, _



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    qty_available = fields.Float('Cantidad Disponible')
    
    def product_qty_available(self):
            
        for line in self.move_ids_without_package:
            line.qty_available = 0
            qty_wh = self.env['stock.quant']._gather(
                line.product_id, self.location_id).mapped('quantity')
            qty_wh_reserved = self.env['stock.quant']._gather(
                line.product_id, self.location_id).mapped('reserved_quantity')
            if qty_wh and qty_wh_reserved:
                line.qty_available = sum(qty_wh) - sum(qty_wh_reserved)


class StockMoveLine(models.Model):
    _inherit = 'stock.move.line'
     
    qty_available = fields.Float('Cantidad Disponible')
    stock_product = fields.Float('Stock')
    barcode_product = fields.Char('Barcode', related='product_id.barcode')
     