# UN Numbers

The data directory contains one JSON file for each UN Number, e.g., data/1203.json.

Each JSON file contains five keys: "description", "class", "classCode", "tunnel" and "number".

## Updating the Data

To update the UN Numbers data from the latest ADR PDF:

1. Install the required Python package:
```bash
pip install pdfplumber
```

2. Place your ADR PDF file named `unnumberdata.pdf` in the root directory

3. Run the script:
```bash
python pdftojson.py
```

This will create/update all JSON files in the `data` directory.

## API Usage

You can access the UN Numbers data directly via GitHub's raw content URLs. Each UN number is available as a JSON file:

```
https://raw.githubusercontent.com/beTransIT/UN-Numbers/master/data/{number}.json
```

For example, to get UN number 0004:
```
https://raw.githubusercontent.com/beTransIT/UN-Numbers/master/data/0004.json
```

Response:
```json
{
    "description": "Ammonium picrate, dry or wetted with less than 10 percent water, by mass",
    "number": "0004",
    "class": "1",
    "classCode": "1.1D",
    "tunnel": "B1000C"
}
```

Note: Make sure to pad the UN number with leading zeros if needed (e.g., "0004" instead of "4").

What is a UN number?
--------------------

    UN numbers or UN IDs are four-digit numbers that identify hazardous substances, and
    articles (such as explosives, flammable liquids, toxic substances, etc.) in the
    framework of international transport. Some hazardous substances have their own UN
    numbers (e.g. acrylamide has UN2074), while sometimes groups of chemicals or
    products with similar properties receive a common UN number (e.g. flammable liquids,
    not otherwise specified, have UN1993). A chemical in its solid state may receive a
    different UN number than the liquid phase if their hazardous properties differ
    significantly; substances with different levels of purity (or concentration in
    solution) may also receive different UN numbers.
    
From [UN number - Wikipedia](http://en.wikipedia.org/wiki/UN_number), 16 Feb 2012.

License
-------

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

Attribution
----------

The original UN number data was collected from [List of UN numbers - Wikipedia](http://en.wikipedia.org/wiki/List_of_UN_numbers), 16 Feb 2012.

This project was forked from the original work by [tantalor](https://github.com/tantalor) ([original repository](https://github.com/tantalor/un)), which was licensed under the [Creative Commons Attribution-ShareAlike License](http://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License). The data has since been updated and the codebase has been modified.
