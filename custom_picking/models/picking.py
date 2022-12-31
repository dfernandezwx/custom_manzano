# -*- coding: utf-8 -*-

from odoo.exceptions import UserError
from odoo import fields, models, api, _



class StockPicking(models.Model):
    _inherit = 'stock.picking'

    qty_available = fields.Float('Cantidad Disponible')
    
    


class StockMoveLine(models.Model):
    _inherit = 'stock.move'
     
    qty_available = fields.Float('Disponible',compute='_compute_product_qty')
    
    barcode_product = fields.Char('Barcode', related='product_id.barcode')
     
    @api.depends('product_id')
    def _compute_product_qty(self):
        for line in self:
            line.qty_available = 0
            if line.picking_id.picking_type_id.code == 'incoming':
                
                qty_wh = self.env['stock.quant']._gather(
                    line.product_id, line.picking_id.location_dest_id).mapped('quantity')
                qty_wh_reserved = self.env['stock.quant']._gather(
                    line.product_id, line.picking_id.location_dest_id).mapped('reserved_quantity')
                if qty_wh and qty_wh_reserved:
                    line.qty_available = sum(qty_wh) - sum(qty_wh_reserved)
            else:
                
                qty_wh = self.env['stock.quant']._gather(
                    line.product_id, line.picking_id.location_id).mapped('quantity')
                qty_wh_reserved = self.env['stock.quant']._gather(
                    line.product_id, line.picking_id.location_id).mapped('reserved_quantity')
                if qty_wh and qty_wh_reserved:
                    line.qty_available = sum(qty_wh) - sum(qty_wh_reserved)