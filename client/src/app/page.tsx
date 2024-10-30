"use client";
import { tiktok_api } from "@/api";
import { LoadingButton } from "@mui/lab";
import { Box, Button, Divider, TextField, Typography } from "@mui/material";
import React, { useState } from "react";
import { toast } from "react-toastify";

const Home = () => {
  const [loading, setLoading] = useState(false);

  const [step, setStep] = useState(0);

  const [content, setContent] = useState<any>(null);

  const handleGenerateContent = async () => {
    setLoading(true);
    console.log("Content generated");

    try {
      const response = await tiktok_api.generateContent();

      console.log("Response", response.data);
      setContent(response.data);
      toast.success("Content generated successfully");
      setStep(1);
      setLoading(false);
    } catch (error) {
      console.error("Failed to generate content", error);
      toast.error("Failed to generate content");
      toast.error(String(error));
      setLoading(false);
    }
  };

  const handleApproveCitation = async () => {
    console.log("Citation approved");
    setStep(2);
    toast.success("Citation approved");
  };

  const handleRejectCitation = async () => {
    console.log("Citation rejected");
    setStep(0);
    setContent(null);
    toast.warning("Citation rejected successfully");
  };

  const handleGenerateVideoContent = async () => {
    console.log("Video content generated");
    toast.success("Video content generated successfully");
    setContent(null);
    setStep(0);
  };

  // const handleCopy = () => {
  //   navigator.clipboard.writeText(content);
  //   toast.success("Content copied to clipboard");
  // };

  return (
    <Box
      sx={{
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        gap: "1rem",
        minHeight: "100vh",
        justifyContent: "center",
      }}
    >
      {step === 0 && (
        <LoadingButton
          variant="contained"
          onClick={handleGenerateContent}
          loading={loading}
          loadingIndicator="Loading..."
          color="success"
        >
          Generate Content
        </LoadingButton>
      )}

      {step !== 0 && (
        <Box
          sx={{
            backgroundColor: "#454545",
            p: 1,
            borderRadius: 1,
            maxWidth: "500px",
            width: "100%",
            m: 1,
          }}
        >
          <Typography
            variant="h6"
            sx={{
              textAlign: "center",
              fontStyle: "italic",
            }}
          >
            "{content?.citation}"
          </Typography>
          <Divider sx={{ my: 1 }} />

          {step === 1 && (
            <Box
              sx={{
                display: "flex",
                gap: "1rem",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Button
                variant="contained"
                color="success"
                fullWidth
                onClick={handleApproveCitation}
              >
                Approve
              </Button>
              <Button
                variant="contained"
                color="error"
                fullWidth
                onClick={handleRejectCitation}
              >
                Reject
              </Button>
            </Box>
          )}

          {step === 2 && (
            <Box>
              <Button
                variant="contained"
                type="link"
                target="_blank"
                fullWidth
                href={content?.photo_search_url}
              >
                Open Photo Search
              </Button>
              {/* textarea */}
              <TextField
                label="Photo links"
                fullWidth
                multiline
                placeholder="Enter photo links separated with semicolon `;`"
                rows={4}
                sx={{
                  my: 2,
                }}
              />
              <Button
                variant="contained"
                color="success"
                fullWidth
                onClick={handleGenerateVideoContent}
              >
                Generate Video Content
              </Button>
            </Box>
          )}

          {/* <Button variant="contained" onClick={handleCopy}>
          Copy
        </Button> */}
        </Box>
      )}
    </Box>
  );
};

export default Home;
