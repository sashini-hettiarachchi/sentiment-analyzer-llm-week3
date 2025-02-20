import React, { useState } from "react";
import { Container, TextField, MenuItem, Button, Typography, Card, CardContent } from "@mui/material";
import axios from "axios";

const App = () => {
  const [text, setText] = useState("");
  const [model, setModel] = useState("custom");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const handleAnalyze = async () => {
    if (!text) return;
    setLoading(true);
    try {
      const response = await axios.post("http://localhost:8080/analyze", { text, model });
      console.log('response', response);
      setResult(response.data);
    } catch (error) {
      console.error("Error analyzing sentiment:", error);
      setResult({ error: "Failed to analyze sentiment" });
    }
    setLoading(false);
  };

  return (
    <Container maxWidth="sm" sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>
        Sentiment Analysis
      </Typography>
      <TextField
        label="Enter text"
        variant="outlined"
        fullWidth
        multiline
        rows={4}
        value={text}
        onChange={(e) => setText(e.target.value)}
        sx={{ mb: 2 }}
      />
      <TextField
        select
        label="Select Model"
        fullWidth
        value={model}
        onChange={(e) => setModel(e.target.value)}
        sx={{ mb: 2 }}
      >
        <MenuItem value="custom">Custom Model</MenuItem>
        <MenuItem value="llama">Llama 3</MenuItem>
      </TextField>
      <Button variant="contained" color="primary" fullWidth onClick={handleAnalyze} disabled={loading}>
        {loading ? "Analyzing..." : "Analyze Sentiment"}
      </Button>
      {result && (
        <Card sx={{ mt: 3, p: 2 }}>
          <CardContent>
            {result.error ? (
              <Typography color="error">{result.error}</Typography>
            ) : (
              <>
                <Typography variant="h6">Sentiment: {result.sentiment}</Typography>
                {result.confidence !== null && (
                  <Typography>Confidence: {(result.confidence * 100).toFixed(2)}%</Typography>
                )}
              </>
            )}
          </CardContent>
        </Card>
      )}
    </Container>
  );
};

export default App;
