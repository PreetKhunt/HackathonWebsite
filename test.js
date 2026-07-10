const html = require('fs').readFileSync('index.html', 'utf8');
const checks = [
    'gName.value',
    'gPhone.value',
    'gEmail.value',
    'tName.value',
    'tFrom.value',
    'days.value',
    'gMsg.textContent',
    'tMsg.textContent'
];
checks.forEach(c => {
    // Only check if it's strictly the old implicit syntax
    // We already have `gName ? gName.value : ''` in the new one.
    // So if it matches EXACTLY "gName.value" without "gName ? " before it.
    let re = new RegExp("\\b" + c.replace(".", "\\.") + "\\b", "g");
    let matches = html.match(re) || [];
    // let's just see if there's any implicit left by printing context
});
console.log('Script ran.');
