import React, { useState } from "react";
import { submitTTSRequest } from "../api/ttsApi";
import LoadingSpinner from "./LoadingSpinner";

const TTSForm = () => {
  const [formData, setFormData] = useState({
    text: "",
    voice: "",
    pitch: 1.0,
    speed: 1.0,
    volume: 1.0,
  });
  const [loading, setLoading] = useState(false);
  const [jobId, setJobId] = useState(null);
  const [error, setError] = useState(null);

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({ ...formData, [name]: value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError(null);
    try {
      const response = await submitTTSRequest(formData);
      setJobId(response.job_id);
    } catch (err) {
      setError(err.response?.data?.detail || "An error occurred");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div>
      <form onSubmit={handleSubmit}>
        <textarea
          name="text"
          placeholder="Enter text"
          value={formData.text}
          onChange={handleChange}
          required
        />
        <input
          type="text"
          name="voice"
          placeholder="Voice"
          value={formData.voice}
          onChange={handleChange}
          required
        />
        <input
          type="number"
          name="pitch"
          placeholder="Pitch"
          value={formData.pitch}
          onChange={handleChange}
          step="0.1"
        />
        <input
          type="number"
          name="speed"
          placeholder="Speed"
          value={formData.speed}
          onChange={handleChange}
          step="0.1"
        />
        <input
          type="number"
          name="volume"
          placeholder="Volume"
          value={formData.volume}
          onChange={handleChange}
          step="0.1"
        />
        <button type="submit" disabled={loading}>
          Submit
        </button>
      </form>
      {loading && <LoadingSpinner />}
      {jobId && <p>Job ID: {jobId}</p>}
      {error && <p className="error">{error}</p>}
    </div>
  );
};

export default TTSForm;
