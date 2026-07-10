const puppeteer = require('puppeteer');

(async () => {
    const browser = await puppeteer.launch();
    const page = await browser.newPage();
    
    page.on('console', msg => console.log('CONSOLE LOG:', msg.text()));
    page.on('pageerror', error => console.log('PAGE ERROR:', error.message));
    page.on('requestfailed', request => {
        console.log('REQUEST FAILED:', request.url(), request.failure().errorText);
    });

    try {
        await page.goto('http://localhost:8080/index.html', { waitUntil: 'networkidle2', timeout: 10000 });
        console.log('Page loaded completely.');
    } catch (e) {
        console.log('Navigation Error:', e.message);
    }
    
    await browser.close();
})();
