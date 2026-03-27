const fs = require('fs');
const html = fs.readFileSync('frontend/reports.html', 'utf8');
const scripts = html.split('<script>');
const scriptContent = scripts[scripts.length - 1].split('</script>')[0];
try {
  new Function(scriptContent);
  console.log("Syntax OK!");
} catch (e) {
  console.error("Syntax Error:", e.name, e.message);
}
