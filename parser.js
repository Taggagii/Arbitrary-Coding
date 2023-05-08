const fs = require("fs");

const reader = (location = undefined, temp = {}) => {
    if (lineReader.length === 0) {
        return temp;
    }
    let match = null;

    const line = lineReader.shift();
    const matches = (type) => {
        match = line.match(new RegExp(`\\d+ ${type} ?(.*)`));
        return match;
    }

    let needsReturn = false;
    switch (location) {
        case undefined:
            if (match = line.match(/0 (.*) INDI/)) {
                temp[match[1]] = reader("indi");
            } else if (match = line.match(/0 (.*) FAM/)) {
                temp[match[1]] = reader("fam");
            }
            break;
        case "indi":
            if (matches("NAME")) {
                if (!temp.hasOwnProperty("names")) {
                    temp["names"] = [];
                }

                temp["names"].push({
                    "fullName": match[1],
                    ...reader("name", {}),
                });
            } else if (matches("SEX")) {
                temp["sex"] = match[1];
            } else if (matches("BIRT")) {
                temp["birthday"] = reader("birt", {});
            } else if (matches("DEAT")) {
                temp["death"] = reader("deat", {});
            } else if (matches("FAMS")) {
                temp["spouseToFamilyLink"] = match[1];
            } else if (matches("FAMC")) {
                temp["childToFamilyLink"] = {
                    "code": match[1],
                    ...reader("famc", {}),
                };
            } else if (matches("PLAC")) {
                temp["place"] = {
                    "location": match[1],
                    ...reader("plac", {}),
                }
            } else if (matches("CHAN")) {
                temp["changed"] = reader("chan", {});
            } else {
                needsReturn = true;
            }
            break;
        case "plac":
            if (matches("MAP")) {
                break;
            } else if (matches("LATI")) {
                temp["lat"] = match[1];
            } else if (matches("LONG")) {
                temp["long"] = match[1];
            } else {
                needsReturn = true;
            }
            break;
        case "name":
            if (matches("GIVN")) {
                temp["givenName"] = match[1];
            } else if (matches("SURN")) {
                temp["surName"] = match[1];
            } else if (matches("TYPE")) {
                temp["type"] = match[1];
                reader("type", {});
            } else if (matches("NICK")) {
                temp["nickname"] = match[1];
            } else if (matches("SPFX")) {
                temp["spfx"] = match[1];
            } else {
                needsReturn = true;
            }
            break;
        case "type":
            if (matches("CONC")) {
                temp["conc"] = match[1];
            } else {
                needsReturn = true;
            }
            break;
        case "birt":
            if (matches("DATE")) {
                temp["date"] = match[1];
            } else if (matches("TYPE")) {
                temp["type"] = match[1];
                reader("type", {});
            } else if (matches("PLAC")) {
                temp["place"] = {
                    "location": match[1],
                    ...reader("plac", {}),
                }
            } else {
                needsReturn = true;
            }
            break;
        case "deat":
            if (matches("DATE")) {
                temp["date"] = match[1];
            } else if (matches("TYPE")) {
                temp["type"] = match[1];
                reader("type", {});
            } else if (matches("PLAC")) {
                temp["place"] = {
                    "location": match[1],
                    ...reader("plac", {}),
                }
            } else {
                needsReturn = true;
            }
            break;
        case "chan":
            if (matches("DATE")) {
                temp["date"] = match[1];
            } else if (matches("TIME")) {
                temp["time"] = match[1];
            } else {
                needsReturn = true;
            }
            break;
        case "famc":
            if (matches("PEDI")) {
                temp["pedi"] = match[1];
            } else {
                needsReturn = true;
            }
            break;

        case "fam":
            if (matches("HUSB")) {
                temp["husband"] = match[1];
            } else if (matches("WIFE")) {
                temp["wife"] = match[1];
            } else if (matches("CHIL")) {
                if (!temp.hasOwnProperty("children")) {
                    temp["children"] = [];
                }

                temp["children"].push(match[1]);
            } else if (matches("NCHIL")) {
                temp["childrenCount"] = match[1];
            } else if (matches("RIN")) {
                temp["recordID"] = match[1];
            } else if (matches("CHAN")) {
                temp["changed"] = reader("chan", {});
            } else {
                needsReturn = true;
            }
            break;   
    }

    if (needsReturn) {
        lineReader.unshift(line);
        return temp;
    }

    return reader(location, temp);
}

let lineReader = fs.readFileSync("file.ged", "utf-8").split(/\r?\n/);
console.log(reader());

lineReader = fs.readFileSync("file.ged", "utf-8").split(/\r?\n/);
fs.writeFileSync("parsedOutput.json", JSON.stringify(reader(), null, 2));

