const fs = require("fs");

const supported = JSON.parse(fs.readFileSync("supported_flutter_google.json"));

for (const [key, value] of Object.entries(supported)) {
    fs.writeFileSync(`./assets/${key}.json`, JSON.stringify({}));
}