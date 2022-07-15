# SpringerNature-Figshare-Downloader
Downloader for Springer Nature Figshare.
It works for Collection only.

## How to use
1. pip install -r requirements.txt
2. python get_links.py <URL> [--out_names | --out_links]
3. ./get_data.sh names.txt links.txt

Then, you can see the data in ./download directory.

## Requirements
1. Python file is written in python 3.6
2. Selenium 4 is used to get download links. You may download Chrome browser. If you do not want to use chrome browser, change the python code and use other browser.
3. To get data, wget is used in shell script.

## Example
```
python get_links.py https://springernature.figshare.com/collections/EEG_Dataset_for_RSVP_and_P300_Speller_Brain-Computer_Interfaces/5769449/1
./get_data.sh names.txt links.txt
```

## Issue
* Sometimes socket does not allocated to this software, so you may wait until the socket is deallocated from other software. If then, just restart this until it works.


