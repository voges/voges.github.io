#!/usr/bin/env bash

# Get Git repository root
git_root="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -n "${git_root}" ]; then
    echo "Git repository root found at: ${git_root}"
else
    echo "Error: Git repository root not found." >&2
    exit 1
fi

# Set up any files
input_file="${git_root}/content/publications/index.md"
echo "Input file: ${input_file}"
tmp_file="$(mktemp)"
output_file="${git_root}/publications.tex"

# Convert Markdown to LaTeX
markdown2latex="${git_root}/utilities/markdown2latex.py"
python3 "${markdown2latex}" "${input_file}" --output "${tmp_file}"

# Remove the Hugo page title
tail --lines=+5 "${tmp_file}" > "${output_file}"

# Make absolute download links
sed -i '' 's#/download#https://voges.github.io/download#g' "${output_file}"

# Remove temporary file
rm "${tmp_file}"

# Point us to the output file
echo "Output file: ${output_file}"
