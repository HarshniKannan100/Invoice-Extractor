import { useState } from "react";
import { useNavigate } from "react-router-dom";
import DraftInvoiceForm from "./DraftInvoiceForm";
import { uploadInvoice } from "../api";
import "./UploadInvoice.css";
function UploadInvoice() {
      const navigate = useNavigate();
      const [file, setFile] = useState(null);
      const [loading, setLoading] = useState(false);
      const [error, setError] = useState("");

    
      const handleUpload = async () => {
        if (!file) {
          alert("Please select a PDF");
          return;
        }
    
        setLoading(true);
        setError("");
    
        try {
      const extractedData = await uploadInvoice(file);

      // store draft temporarily
      sessionStorage.setItem("draftInvoice", JSON.stringify(extractedData));

      // move to draft page
      navigate("/draft");
    } catch (err) {
      setError("Upload failed", err);
    } finally {
      setLoading(false);
    }
  };
      return (
        <div className="box">
          <p>📄 Invoice Extractor</p>
    
          <input
            type="file"
            accept=".pdf"
            onChange={(e) => setFile(e.target.files[0])}
            className="file-input"
          />
    
          <button onClick={handleUpload} disabled={loading} className="upload-button">
            {loading ? "Processing..." : "Upload Invoice"}
          </button>
    
          {error && <p className="error">{error}</p>}
        </div>
      );
    }
export default UploadInvoice;