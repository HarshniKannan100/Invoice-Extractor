export async function uploadInvoice(file) {
  const formData = new FormData();
  formData.append("file", file);

  const response = await fetch("http://127.0.0.1:8000/uploadfile/", {
    method: "POST",
    body: formData,
  });

  return response.json();
}

export async function getInvoiceById(invoiceId) {
  const response = await fetch(
    `http://127.0.0.1:8000/invoice/${invoiceId}`
  );
  return response.json();
}

export async function getAllInvoices() {
  const response = await fetch("http://127.0.0.1:8000/invoices");
  return response.json();
}

export async function deleteInvoice(itemId) {
  const response = await fetch(
    `http://127.0.0.1:8000/invoice-item/${itemId}`,
    { method: "DELETE" }
  );

  if (!response.ok) {
    throw new Error("Delete failed");
  }

  return response.json();
}
