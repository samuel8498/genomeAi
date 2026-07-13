import { useState } from "react";
import axios from "axios";

function Dashboard() {
  const [file, setFile] = useState(null);
  const [prediction, setPrediction] = useState("");
  const [confidence, setConfidence] = useState("");

  const handlePredict = async () => {
    if (!file) {
      alert("Please select a CSV file");
      return;
    }

    const formData = new FormData();
    formData.append("file", file);

    try {
      const response = await axios.post(
        "http://127.0.0.1:8000/predict",
        formData
      );

      if (response.data.prediction) {
        setPrediction(response.data.prediction);
        setConfidence(response.data.confidence + "%");
      } else if (response.data.predictions) {
        setPrediction(response.data.predictions[0].prediction);
        setConfidence(response.data.predictions[0].confidence + "%");
      }
    } catch (err) {
      console.log(err);
      alert("Prediction Failed");
    }
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        width: "100%",
        background:
          "linear-gradient(135deg,#eef5ff,#dbeafe,#bfdbfe)",
        display: "flex",
        justifyContent: "center",
        alignItems: "center",
        padding: "40px",
        boxSizing: "border-box",
      }}
    >
      <div
        style={{
          width: "95%",
          maxWidth: "1200px",
          background: "#fff",
          borderRadius: "20px",
          padding: "50px",
          boxShadow: "0 15px 40px rgba(0,0,0,0.15)",
        }}
      >
        <h1
          style={{
            textAlign: "center",
            fontSize: "60px",
            color: "#2563eb",
            marginBottom: "10px",
          }}
        >
          🧬 GenomeAI
        </h1>

        <p
          style={{
            textAlign: "center",
            color: "#555",
            fontSize: "20px",
            marginBottom: "40px",
          }}
        >
          AI-Powered Cancer Type Prediction using Gene Expression Data
        </p>

        <div
          style={{
            display: "flex",
            justifyContent: "space-between",
            gap: "40px",
          }}
        >
          {/* Left Section */}
          <div style={{ flex: 1 }}>
            <h2 style={{ color: "#111", marginBottom: "20px" }}>
              Upload Dataset
            </h2>

            <input
              type="file"
              accept=".csv"
              onChange={(e) => setFile(e.target.files[0])}
            />

            <br />
            <br />

            <button
              onClick={handlePredict}
              style={{
                background: "#2563eb",
                color: "white",
                padding: "15px 30px",
                border: "none",
                borderRadius: "10px",
                fontSize: "18px",
                cursor: "pointer",
              }}
            >
              Predict Cancer
            </button>

            <div
              style={{
                marginTop: "30px",
                background: "#f8fafc",
                padding: "20px",
                borderRadius: "10px",
              }}
            >
              <h3 style={{ color: "#111" }}>Dataset Information</h3>

              <p style={{ color: "#444" }}>
                ✔ Upload TCGA Gene Expression CSV
              </p>

              <p style={{ color: "#444" }}>
                ✔ Supports BRCA, LUAD, COAD, PRAD, KIRC
              </p>

              <p style={{ color: "#444" }}>
                ✔ ML Accuracy: <strong>98.13%</strong>
              </p>
            </div>
          </div>

          {/* Right Section */}
          <div
            style={{
              flex: 1,
              background: "#eff6ff",
              borderRadius: "15px",
              padding: "30px",
            }}
          >
            <h2
              style={{
                color: "#1e40af",
                textAlign: "center",
              }}
            >
              Prediction Result
            </h2>

            <div
              style={{
                marginTop: "40px",
                fontSize: "24px",
                color: "#111",
              }}
            >
              <p>
                <strong>Cancer Type:</strong>{" "}
                {prediction || "Not Predicted"}
              </p>

              <p>
                <strong>Confidence:</strong>{" "}
                {confidence || "--"}
              </p>
            </div>

            <div
              style={{
                marginTop: "50px",
                background: "#dbeafe",
                padding: "20px",
                borderRadius: "10px",
              }}
            >
              <h3 style={{ color: "#1e3a8a" }}>
                About GenomeAI
              </h3>

              <p style={{ color: "#333", lineHeight: "28px" }}>
                GenomeAI predicts cancer types using TCGA gene expression
                datasets. It combines Random Forest and XGBoost models with
                FastAPI and React to provide fast, accurate predictions.
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;