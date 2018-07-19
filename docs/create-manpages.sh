#!/bin/bash
# needs pandoc and php installed

# remove old files
rm fenrir.1
rm user.md

# convert to markdown
php DokuWiki-to-Markdown-Converter/convert.php user.txt

# convert markdown to manpage
pandoc user.md -f markdown -t man -s -o fenrir.1

