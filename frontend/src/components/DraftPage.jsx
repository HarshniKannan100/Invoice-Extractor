import { useState, useEffect } from "react";
import DraftInvoiceForm from "../components/DraftInvoiceForm";
import { useNavigate } from "react-router-dom";
import React from "react";

function DraftInvoicePage() {
  const [draftInvoice, setDraftInvoice] = useState(null);
  const navigate = useNavigate();

  useEffect(() => {
    const data = sessionStorage.getItem("draftInvoice");
    if (!data) navigate("/");
    // eslint-disable-next-line react-hooks/set-state-in-effect
    else setDraftInvoice(JSON.parse(data));
  }, [navigate]);

  const handleSave = async () => {
    await fetch("http://127.0.0.1:8000/save-invoice", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(draftInvoice)
    });

    sessionStorage.removeItem("draftInvoice");
    navigate("/invoices");
  };

  if (!draftInvoice) return null;

  return (
    <DraftInvoiceForm
      draftInvoice={draftInvoice}
      setDraftInvoice={setDraftInvoice}
      onSave={handleSave}
    />
  );
}

export default DraftInvoicePage;
