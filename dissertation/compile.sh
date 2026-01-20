#!/bin/bash
# Compile LaTeX dissertation

set -euo pipefail

for tool in pdflatex bibtex; do
  if ! command -v "$tool" >/dev/null 2>&1; then
    echo "Error: '$tool' not found. Install a LaTeX distribution (e.g., TeX Live/MacTeX) and try again." >&2
    exit 127
  fi
done

echo "Compiling dissertation..."

# Run pdflatex
pdflatex -interaction=nonstopmode main.tex

# Run bibtex
bibtex main

# Run pdflatex twice more for references
pdflatex -interaction=nonstopmode main.tex
pdflatex -interaction=nonstopmode main.tex

# Clean up auxiliary files
rm -f *.aux *.log *.out *.toc *.bbl *.blg *.synctex.gz *.fdb_latexmk *.fls

echo "Compilation complete! Output: main.pdf"

