#!/bin/bash
# Compile LaTeX dissertation

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

