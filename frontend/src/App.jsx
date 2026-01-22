import { Routes, Route, Link } from "react-router-dom";
import UploadInvoice from "./components/uploadInvoice";
import InvoiceTable from "./components/InvoiceTable";
import "./App.css";
import DraftInvoiceForm from "./components/DraftInvoiceForm";
import DraftPage from "./components/DraftPage";

function App() {
  return (
    <div>
      <nav style={{ marginBottom: "20px" }} className="RoutingButton">
        <Link to="/" style={{ marginRight: "15px" }} id="ui">Upload Invoice</Link>
        <Link to="/invoices" id="vi">View Invoices</Link>
      </nav>

      <Routes>
        <Route path="/" element={<UploadInvoice />} />
        <Route path="/invoices" element={<InvoiceTable />} />
        <Route path="/draft" element={<DraftPage />} />

      </Routes>
    </div>
  );
}

export default App;
