const http = require('http');
const fs = require('fs');
const path = require('path');
const puppeteer = require('puppeteer');

const PORT = 4000;
const SITE_DIR = path.resolve(__dirname, '../_site');
const OUTPUT_PATH = path.resolve(__dirname, '../docs/assets/output.pdf');

// Helper to determine Content-Type
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

// Create a static web server to serve the Jekyll-built site
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
