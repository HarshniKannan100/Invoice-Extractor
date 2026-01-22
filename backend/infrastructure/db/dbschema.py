from pydantic import BaseModel, EmailStr
from typing import Optional, List
from decimal import Decimal
from datetime import date


class VendorSchema(BaseModel):
    name: Optional[str] = None
    address: Optional[str] = None
    email: Optional[EmailStr] = None
    gst_no: Optional[str] = None
    contact: Optional[str] = None

    class Config:
        from_attributes = True

class InvoiceHeaderSchema(BaseModel):
    invoice_number: Optional[str] = None
    invoice_date: Optional[date] = None
    due_date: Optional[date] = None
    invoice_amount: Optional[Decimal] = None
    ntby_no: Optional[str] = None
    po_reference: Optional[dict] = None
    irn: Optional[str] = None

    class Config:
        from_attributes = True


class InvoiceItemsSchema(BaseModel):
    code: Optional[str] = None
    description: Optional[str] = None
    uom: Optional[str] = None
    billed_qty: Optional[Decimal] = None
    rate: Optional[Decimal] = None
    discount_percent: Optional[Decimal] = None
    discount_amount: Optional[Decimal] = None
    taxable_value: Optional[Decimal] = None
    hsn_code: Optional[str] = None
    cgst_percent: Optional[Decimal] = None
    cgst_amount: Optional[Decimal] = None
    sgst_percent: Optional[Decimal] = None
    sgst_amount: Optional[Decimal] = None
    igst_percent: Optional[Decimal] = None
    igst_amount: Optional[Decimal] = None
    roundOff: Optional[Decimal] = None
    total_value: Optional[Decimal] = None

    class Config:
        from_attributes = True

class InvoiceSummarySchema(BaseModel):
    product_total: Optional[Decimal] = None
    taxable_value_total: Optional[Decimal] = None
    freight_charges: Optional[Decimal] = None
    tax_percentage: Optional[Decimal] = None
    cgst_total: Optional[Decimal] = None
    sgst_total: Optional[Decimal] = None
    igst_total: Optional[Decimal] = None
    tcs_percent: Optional[Decimal] = None
    tcs_amount: Optional[Decimal] = None
    round_off_amount: Optional[Decimal] = None
    grand_total: Optional[Decimal] = None
    buyer_name: Optional[str] = None

    class Config:
        from_attributes = True
