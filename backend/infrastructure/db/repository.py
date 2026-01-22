from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import delete, select
from fastapi import HTTPException
from infrastructure.db.models import (
    Vendor,
    InvoiceHeader,
    InvoiceItems,
    InvoiceSummary
)
from infrastructure.db.connections import AsyncSessionLocal

async def save_invoice(
    db: AsyncSession,
    vendor_data,
    invoice_header_data,
    invoice_items_data,
    invoice_summary_data
):
    # -------------------
    # Vendor
    # -------------------
    vendor = Vendor(**vendor_data.model_dump())
    db.add(vendor)
    await db.flush()   # get vendor_id

    # -------------------
    # Invoice Header
    # -------------------
    invoice_header = InvoiceHeader(
        vendor_id=vendor.vendor_id,
        **invoice_header_data.model_dump()
    )
    db.add(invoice_header)
    await db.flush()   # get invoice_id

    # -------------------
    # Invoice Items
    # -------------------
    for item in invoice_items_data:
        db.add(
            InvoiceItems(
                invoice_header_id=invoice_header.invoice_id,
                **item.model_dump()
            )
        )

    # -------------------
    # Invoice Summary
    # -------------------
    summary = InvoiceSummary(
        invoice_header_id=invoice_header.invoice_id,
        **invoice_summary_data.model_dump()
    )
    db.add(summary)

    await db.commit()

    return invoice_header.invoice_id

async def get_invoice_by_id(db: AsyncSession, invoice_id: int):
    header_result = await db.execute(
        select(InvoiceHeader).where(InvoiceHeader.invoice_id == invoice_id)
    )
    invoice_header = header_result.scalar_one_or_none()
    if not invoice_header:
        return None
    vendor = await db.get(Vendor, invoice_header.vendor_id)
    items_result = await db.execute(
        select(InvoiceItems).where(
            InvoiceItems.invoice_header_id == invoice_id
        )
    )
    items = items_result.scalars().all()
    summary_result = await db.execute(
        select(InvoiceSummary).where(
            InvoiceSummary.invoice_header_id == invoice_id
        )
    )
    summary = summary_result.scalar_one_or_none()
    return {
        "vendor": vendor,
        "invoice_header": invoice_header,
        "invoice_items": items,
        "invoice_summary": summary
    }

async def get_all_invoices(db: AsyncSession):
    header_result = await db.execute(select(InvoiceHeader))
    invoice_headers = header_result.scalars().all()
    invoices = []
    for invoice_header in invoice_headers:
        vendor = await db.get(Vendor, invoice_header.vendor_id)
        items_result = await db.execute(
            select(InvoiceItems).where(
                InvoiceItems.invoice_header_id == invoice_header.invoice_id
            )
        )
        items = items_result.scalars().all()
        summary_result = await db.execute(
            select(InvoiceSummary).where(
                InvoiceSummary.invoice_header_id == invoice_header.invoice_id
            )
        )
        summary = summary_result.scalar_one_or_none()
        invoices.append({
            "vendor": vendor,
            "invoice_header": invoice_header,
            "invoice_items": items,
            "invoice_summary": summary
        })
    return invoices

async def delete_invoice_item(db, item_id: int):
    item = await db.get(InvoiceItems, item_id)
    if item:
        await db.delete(item)
        await db.commit()


