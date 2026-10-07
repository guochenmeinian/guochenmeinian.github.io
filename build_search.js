// Keep the same elasticlunr search-index format that Zola generated.
const fs = require('fs');
const elasticlunr = require('./static/elasticlunr.min.js');

const documents = JSON.parse(fs.readFileSync(0, 'utf8'));
const index = elasticlunr(function () {
  this.addField('title');
  this.addField('body');
  this.setRef('id');
});
for (const document of documents) index.addDoc(document);
process.stdout.write('window.searchIndex = ' + JSON.stringify(index.toJSON()) + ';\n');
