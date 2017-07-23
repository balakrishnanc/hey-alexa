# About

`hey-alexa` is a python program to scrape the top _N_ Web sites that are freely
 available on Alexa's Web site.


# Requirements

The utility requires the
excellent [requests](http://docs.python-requests.org/en/master/) python library.


# Usage

```
§ ./hey-alexa.py -h
usage: hey-alexa.py [-h] [--unsafe] [--url url] [--out output] mode

Retrieve the top N Web sites from Alexa's Web site

positional arguments:
  mode          <global|by-country|by-category>

optional arguments:
  -h, --help    show this help message and exit
  --unsafe      Include even Web sites in the "adult" category
  --url url     Web page containing the relevant details
  --out output  Output file path
```


# Example Invocations

Run the following command to retrieve the top _N_ Web sites listed on
Alexa’s Web site.

```
§ ./hey-alexa.py global --out global-07232017.txt
```

To retrieve the top _N_ Web sites by country, run the following command. If the
option `–out` is not specified, the output is printed on the console.

```
§ ./hey-alexa.py by-country --url http://www.alexa.com/topsites/countries
1,Afghanistan,google.com.af
2,Afghanistan,google.com
...
```

You can use the following options to retrieve the top Web sites per category.
```
§ ./hey-alexa.py by-category --url http://www.alexa.com/topsites/category
1,Arts,youtube.com
2,Arts,facebook.com/#!/JeffDunham
...
```
