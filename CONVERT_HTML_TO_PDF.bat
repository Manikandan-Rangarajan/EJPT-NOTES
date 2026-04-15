@echo off
REM Batch script to convert HTML files to PDF using Puppeteer/Node.js
REM Requires: Node.js and npm

echo Installing html-pdf converter if not present...
npm install -g html-pdf 2>nul

echo Converting HTML files to PDF...
for %%f in (PDF_OUTPUT\*.html) do (
    echo Converting %%f...
    node -e "const html = require('fs').readFileSync('%%f', 'utf8'); const pdf = require('html-pdf'); pdf.create(html, {}).toFile('%%~nf.pdf', function(err, res) { if (err) console.log(err); else console.log('Created: ' + res.filename); });"
)

echo.
echo Conversion complete! Check current directory for PDF files.
pause
