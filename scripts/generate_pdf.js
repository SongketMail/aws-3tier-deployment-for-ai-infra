/**
 * @file generate_pdf.js
 * @description Automates repository-wide A4 PDF generation from a compiled Jekyll static site
 * by running a local HTTP server and using Puppeteer to print the aggregated print_all.html.
 * @author Harisfazillah Jamel (LinuxMalaysia)
 * @license GNU General Public License v3.0
 */

const http = require('http');
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

/**
 * Port number on which the local HTTP server will listen.
 * @type {number}
 */
const PORT = 4000;

/**
 * Absolute path to the Jekyll statically built output directory.
 * @type {string}
 */
const SITE_DIR = path.resolve(__dirname, '../_site');

/**
 * Absolute path where the generated high-fidelity PDF will be saved.
 * @type {string}
 */
const OUTPUT_PATH = path.resolve(__dirname, '../docs/assets/output.pdf');

/**
 * Returns the HTTP 'Content-Type' header value for a given file path based on its extension.
 *
 * @param {string} filePath - The path to the file.
 * @returns {string} The appropriate MIME content-type string.
 */
function getContentType(filePath) {
  const ext = path.extname(filePath).toLowerCase();
  switch (ext) {
    case '.html': return 'text/html';
    case '.css': return 'text/css';
    case '.js': return 'application/javascript';
    case '.png': return 'image/png';
    case '.jpg':
    case '.jpeg': return 'image/jpeg';
    case '.gif': return 'image/gif';
    case '.svg': return 'image/svg+xml';
    case '.ico': return 'image/x-icon';
    case '.pdf': return 'application/pdf';
    case '.json': return 'application/json';
    default: return 'application/octet-stream';
  }
}

/**
 * HTTP server to serve the statically built Jekyll site.
 * Resolves safe URLs, prevents path traversal, and returns files with appropriate content types.
 */
const server = http.createServer((req, res) => {
  // Prevent path traversal
  const safeUrl = req.url.split('?')[0].replace(/\.\./g, '');
  let filePath = path.join(SITE_DIR, safeUrl === '/' ? 'index.html' : safeUrl);

  // If the path exists and is a directory, append index.html
  if (fs.existsSync(filePath) && fs.statSync(filePath).isDirectory()) {
    filePath = path.join(filePath, 'index.html');
  }

  fs.readFile(filePath, (err, data) => {
    if (err) {
      res.writeHead(404, { 'Content-Type': 'text/plain' });
      res.end('404 Not Found');
    } else {
      res.writeHead(200, { 'Content-Type': getContentType(filePath) });
      res.end(data);
    }
  });
});

/**
 * Starts the HTTP server, launches a headless Puppeteer browser instance,
 * navigates to print_all.html, prints to a high-fidelity A4 PDF with appropriate margins,
 * and cleans up all resources on completion or failure.
 */
server.listen(PORT, async () => {
  console.log(`[Server] Running at http://localhost:${PORT}`);
  let browser;
  try {
    console.log('[Puppeteer] Launching browser...');
    browser = await puppeteer.launch({
      headless: 'new',
      args: ['--no-sandbox', '--disable-setuid-sandbox', '--disable-dev-shm-usage']
    });

    const page = await browser.newPage();
    const url = `http://localhost:${PORT}/print_all.html`;

    console.log(`[Puppeteer] Navigating to ${url}...`);
    await page.goto(url, {
      waitUntil: 'networkidle0',
      timeout: 90000
    });

    console.log('[Puppeteer] Generating PDF from print_all.html...');

    // Ensure the output directory exists
    const outputDir = path.dirname(OUTPUT_PATH);
    if (!fs.existsSync(outputDir)) {
      fs.mkdirSync(outputDir, { recursive: true });
    }

    await page.pdf({
      path: OUTPUT_PATH,
      format: 'A4',
      printBackground: true,
      margin: {
        top: '10mm',
        bottom: '10mm',
        left: '10mm',
        right: '10mm'
      }
    });

    console.log(`[Puppeteer] Successfully generated PDF at ${OUTPUT_PATH}`);
    await browser.close();
    server.close();
    process.exit(0);
  } catch (error) {
    console.error('[Error] Failed to generate PDF:', error);
    if (browser) {
      try {
        await browser.close();
      } catch (e) {
        console.error('[Error] Failed to close browser:', e);
      }
    }
    server.close();
    process.exit(1);
  }
});
