import { useState } from "react";
import { uploadFile, trainModel } from "../api";

function Upload() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleUpload = async () => {
    if (!file) {
      alert("⚠️ Please select a file first");
      return;
    }

    try {
      setLoading(true);
      const formData = new FormData();
      formData.append("file", file);

      await uploadFile(formData);
      alert("✅ File uploaded successfully");
    } catch (err) {
      console.error(err);
      alert("❌ Upload failed. Check the backend and file format.");
    } finally {
      setLoading(false);
    }
  };

  const handleTrain = async () => {
    try {
      setLoading(true);
      await trainModel();
      alert("✅ Model trained successfully");
    } catch (err) {
      console.error(err);
      alert("❌ Training failed. Upload the dataset first.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="upload-panel">
      <div className="section-header">
        <div>
          <p className="section-eyebrow">Data Upload</p>
          <h2>Dataset Management</h2>
        </div>
      </div>

      <p className="section-description">
        Upload your Excel dataset to prepare demand history and train the forecasting model.
      </p>

      <input
        className="file-input"
        type="file"
        onChange={(e) => setFile(e.target.files[0])}
      />

      <div className="button-row">
        <button className="button primary" onClick={handleUpload} disabled={loading}>
          {loading ? "Uploading..." : "Upload File"}
        </button>
        <button className="button secondary" onClick={handleTrain} disabled={loading}>
          {loading ? "Training..." : "Train Model"}
        </button>
      </div>
    </div>
  );
}

export default Upload;
