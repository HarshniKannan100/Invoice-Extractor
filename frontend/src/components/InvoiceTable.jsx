import { useEffect, useState } from "react";
import { getAllInvoices } from "../api";
import { deleteInvoice } from "../api";
import React from "react";
import "./InvoiceTable.css";

function InvoiceTable() {
  const [invoices, setInvoices] = useState([]);

   useEffect(() => {
    const loadInvoices = async () => {
      try {
        const data = await getAllInvoices();
        setInvoices(data);
      } catch (err) {
        console.error("Failed to load invoices", err);
      }
    };

    loadInvoices();
  }, []);


  const handleDelete = async (id) => {
    if (!window.confirm("Delete invoice?")) return;
    await deleteInvoice(id);
    const data = await getAllInvoices();
    setInvoices(data);
  };
  let idx=1;
  return (
    <div>
    {invoices.length > 0 && (
            <div className="table-wrapper">
            <table>
                <thead>
                  <tr>
                    <th>S.No</th>
    
                    {/* Vendor */}
                    <th>Vendor Name</th>
                    <th>Address</th>
                    <th>Email</th>
                    <th>GST No</th>
                    <th>Contact</th>
    
                    {/* Invoice Header */}
                    <th>Invoice No</th>
                    <th>Invoice Date</th>
                    <th>Due Date</th>
                    <th>Invoice Amount</th>
                    <th>NTBY No</th>
                    <th>IRN</th>
    
                    {/* Item */}
                    <th>Item Code</th>
                    <th>Description</th>
                    <th>UOM</th>
                    <th>Qty</th>
                    <th>Rate</th>
                    <th>Discount %</th>
                    <th>Discount Amt</th>
                    <th>Taxable Value</th>
                    <th>HSN</th>
                    <th>CGST</th>
                    <th>SGST</th>
                    <th>IGST</th>
                    <th>Total</th>
    
                    {/* Summary */}
                    <th>Product Total</th>
                    <th>CGST Total</th>
                    <th>SGST Total</th>
                    <th>IGST Total</th>
                    <th>Round Off</th>
                    <th>Grand Total</th>
                    <th>Buyer</th>
                  </tr>
                </thead>
    
                <tbody>
                  {invoices.map((inv, i) =>
                    inv.invoice_items.map((item, j) => (
                      <tr key={`${i}-${j}`}>
                        <td>{idx++}</td>
                        {/* Vendor */}
                        <td>{inv.vendor.name}</td>
                        <td>{inv.vendor.address}</td>
                        <td>{inv.vendor.email}</td>
                        <td>{inv.vendor.gst_no}</td>
                        <td>{inv.vendor.contact}</td>
    
                        {/* Header */}
                        <td>{inv.invoice_header.invoice_number}</td>
                        <td>{inv.invoice_header.invoice_date}</td>
                        <td>{inv.invoice_header.due_date}</td>
                        <td>{inv.invoice_header.invoice_amount}</td>
                        <td>{inv.invoice_header.ntby_no}</td>
                        <td>{inv.invoice_header.irn}</td>
    
                        {/* Item */}
                        <td>{item.code}</td>
                        <td>{item.description}</td>
                        <td>{item.uom}</td>
                        <td>{item.billed_qty}</td>
                        <td>{item.rate}</td>
                        <td>{item.discount_percent}</td>
                        <td>{item.discount_amount}</td>
                        <td>{item.taxable_value}</td>
                        <td>{item.hsn_code}</td>
                        <td>{item.cgst_percent}% ({item.cgst_amount})</td>
                        <td>{item.sgst_percent}% ({item.sgst_amount})</td>
                        <td>{item.igst_percent}% ({item.igst_amount})</td>
                        <td>{item.total_value}</td>
    
                        {/* Summary */}
                        <td>{inv.invoice_summary.product_total}</td>
                        <td>{inv.invoice_summary.cgst_total}</td>
                        <td>{inv.invoice_summary.sgst_total}</td>
                        <td>{inv.invoice_summary.igst_total}</td>
                        <td>{inv.invoice_summary.round_off_amount}</td>
                        <td>{inv.invoice_summary.grand_total}</td>
                        <td>{inv.invoice_summary.buyer_name}</td>
    
                        <td><button className="delete-icon" onClick={() =>handleDelete(item.item_id)} title="Delete item">🗑️</button></td>
                      </tr>
                    ))
                  )}
                </tbody>
              </table>
            </div>
          )}
          </div>
    );  
}

export default InvoiceTable;