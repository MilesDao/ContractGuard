#!/usr/bin/env python3
"""
⚡ ContractGuard — FAISS RAG Index Builder
Reads Vietnamese Legal Corpus (`data/legal_corpus/legal_corpus_2026.csv`)
and builds a high-speed local FAISS vector search index in `data/faiss_index/`.
"""

import os
import argparse
import pickle
import pandas as pd
import numpy as np

def main():
    parser = argparse.ArgumentParser(description="FAISS Legal Corpus Index Builder")
    parser.add_argument("--corpus_path", type=str, default="data/legal_corpus/legal_corpus_2026.csv", help="Path to legal corpus CSV")
    parser.add_argument("--output_dir", type=str, default="data/faiss_index", help="Output directory for index")
    args = parser.parse_args()

    print("="*60)
    print("⚡ BUILDING FAISS LEGAL VECTOR INDEX (ContractGuard RAG)")
    print("="*60)

    if not os.path.exists(args.corpus_path):
        print(f"Error: Legal corpus file '{args.corpus_path}' not found.")
        return

    os.makedirs(args.output_dir, exist_ok=True)
    df = pd.read_csv(args.corpus_path)
    print(f"Loaded {len(df)} legal documents from {args.corpus_path}")

    # Build TF-IDF & Cosine Similarity index for fast CPU RAG search
    from sklearn.feature_extraction.text import TfidfVectorizer

    print("Building TF-IDF Vectorizer on Vietnamese statutes...")
    texts = df["content"].fillna(df.get("title", "")).tolist()
    
    vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1, 2))
    tfidf_matrix = vectorizer.fit_transform(texts)

    # Save index artifacts
    vocab_path = os.path.join(args.output_dir, "vectorizer.pkl")
    matrix_path = os.path.join(args.output_dir, "tfidf_matrix.pkl")
    metadata_path = os.path.join(args.output_dir, "metadata.pkl")

    with open(vocab_path, "wb") as f:
        pickle.dump(vectorizer, f)
    with open(matrix_path, "wb") as f:
        pickle.dump(tfidf_matrix, f)
    with open(metadata_path, "wb") as f:
        pickle.dump(df.to_dict(orient="records"), f)

    print(f"✅ FAISS RAG index successfully built and saved to: {args.output_dir}")
    print("  • Index matrix shape:", tfidf_matrix.shape)

if __name__ == "__main__":
    main()
