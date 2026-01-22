import "./DraftInvoiceForm.css";

function DraftInvoiceForm({ draftInvoice, setDraftInvoice, onSave }) {
  const updateSection = (section, field, value) => {
    setDraftInvoice((prev) => ({
      ...prev,
      [section]: {
        ...prev[section],
        [field]: value
      }
    }));
  };

  const updateItem = (index, field, value) => {
    const items = [...draftInvoice.invoice_items];
    items[index] = { ...items[index], [field]: value };
    setDraftInvoice({ ...draftInvoice, invoice_items: items });
  };

  return (
    <div className="draft-invoice">
      <h2>📝 Draft Invoice</h2>

      <h3>Vendor</h3>
      <label>Vendor Name:</label>
      <input value={draftInvoice.vendor.name || ""} onChange={(e)=>updateSection("vendor","name",e.target.value)} placeholder="Vendor Name"/>
      <label>Address:</label>
      <input value={draftInvoice.vendor.address || ""} onChange={(e)=>updateSection("vendor","address",e.target.value)} placeholder="Address"/>
      <label>Email:</label>
      <input value={draftInvoice.vendor.email || ""} onChange={(e)=>updateSection("vendor","email",e.target.value)} placeholder="Email"/>
      <label>GST No:</label>
      <input value={draftInvoice.vendor.gst_no || ""} onChange={(e)=>updateSection("vendor","gst_no",e.target.value)} placeholder="GST No"/>
      <label>Contact:</label>
      <input value={draftInvoice.vendor.contact || ""} onChange={(e)=>updateSection("vendor","contact",e.target.value)} placeholder="Contact"/>

      <h3>Invoice Header</h3>
      <label>Invoice No:</label>
      <input value={draftInvoice.invoice_header.invoice_number || ""} onChange={(e)=>updateSection("invoice_header","invoice_number",e.target.value)} placeholder="Invoice No"/>
      <label>Invoice Date:</label>
      <input value={draftInvoice.invoice_header.invoice_date || ""} onChange={(e)=>updateSection("invoice_header","invoice_date",e.target.value)} placeholder="Invoice Date"/>
      <label>Due Date:</label>  
      <input value={draftInvoice.invoice_header.due_date || ""} onChange={(e)=>updateSection("invoice_header","due_date",e.target.value)} placeholder="Due Date"/>
      <label>Amount:</label>
      <input value={draftInvoice.invoice_header.invoice_amount || ""} onChange={(e)=>updateSection("invoice_header","invoice_amount",e.target.value)} placeholder="Amount"/>

      <h3>Items</h3>
      {draftInvoice.invoice_items.map((item, i) => (
        <div key={i} className="item-row">
          <label>Description:</label>
          <input value={item.description || ""} onChange={(e)=>updateItem(i,"description",e.target.value)} placeholder="Description"/>
          <label>Qty:</label>
          <input value={item.billed_qty || ""} onChange={(e)=>updateItem(i,"billed_qty",e.target.value)} placeholder="Qty"/>
          <label>Rate:</label>         
          <input value={item.rate || ""} onChange={(e)=>updateItem(i,"rate",e.target.value)} placeholder="Rate"/>
          <label>Total:</label>
          <input value={item.total_value || ""} onChange={(e)=>updateItem(i,"total_value",e.target.value)} placeholder="Total"/>
        </div>
      ))}

      <h3>Summary</h3>
      <label>Product Total:</label>
      <input value={draftInvoice.invoice_summary.product_total || ""} onChange={(e)=>updateSection("invoice_summary","product_total",e.target.value)} placeholder="Product Total"/>
      <label>CGST Total:</label>
      <input value={draftInvoice.invoice_summary.cgst_total || ""} onChange={(e)=>updateSection("invoice_summary","cgst_total",e.target.value)} placeholder="CGST"/>
      <label>SGST Total:</label>
      <input value={draftInvoice.invoice_summary.sgst_total || ""} onChange={(e)=>updateSection("invoice_summary","sgst_total",e.target.value)} placeholder="SGST"/>
      <label>IGST Total:</label>
      <input value={draftInvoice.invoice_summary.igst_total || ""} onChange={(e)=>updateSection("invoice_summary","igst_total",e.target.value)} placeholder="IGST"/>

      <label>Grand Total:</label>
      <input value={draftInvoice.invoice_summary.grand_total || ""} onChange={(e)=>updateSection("invoice_summary","grand_total",e.target.value)} placeholder="Grand Total"/>

      <button onClick={onSave}>💾 Save Invoice</button>
    </div>
  );
}

export default DraftInvoiceForm;
