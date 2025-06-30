# 🧠 FUCHS Data Discovery Hackathon – AI-Powered Document Intelligence

## 🥈 Ranked 2nd Place | GPT-4 + Python + Prompt Engineering

This project was built for the [FUCHS Intelligent Data Discovery Hackathon](https://www.hackerearth.com/challenges/hackathon/fuchs-intelligent-data-discovery/). It demonstrates an end-to-end pipeline that automatically extracts structured experimental data from unstructured R&D documents across PDF, Word, Excel, and CSV formats.

---

## 🔍 Problem Statement

R&D teams often rely on diverse technical documents to store test results, machine configurations, chemical formulations, and performance metrics. However, these documents are:

- Unstructured
- Inconsistently formatted
- Not machine-readable

The challenge: **Automatically extract machine name, input products, output result, and unit** from such documents and generate a structured CSV for downstream use.

---

## 🚀 Solution Overview

We built an **AI-assisted pipeline** powered by GPT-4 to:

- Parse experimental data from heterogeneous files
- Chunk and clean content for prompt processing
- Prompt GPT-4 to extract structured JSON outputs
- Normalize and map results using CSV-based lookup dictionaries
- Generate a final submission-ready CSV

---

