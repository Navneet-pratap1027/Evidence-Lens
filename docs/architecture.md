# Architecture

5-layer design:

1. **Multimodal Input Layer** — video, audio, caption, metadata ingestion
2. **Evidence Extraction Layer** — CLIP (caption↔video), Whisper (ASR), OCR, reverse search, claim extraction
3. **Knowledge Retrieval Layer** — RAG over curated trusted corpus (vector DB)
4. **Evidence Fusion Layer** — weighted scoring + deterministic rule engine + source reliability weighting
5. **Explainability Layer** — evidence graph, confidence breakdown, citations, limitations

TODO: add diagram once frame extraction + fusion modules are implemented.
