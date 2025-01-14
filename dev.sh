#!/bin/sh
./gen_html.sh && docker compose down && docker compose up --build -d && ./gen_html.sh watch