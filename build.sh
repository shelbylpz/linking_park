#!/bin/bash

rm *.spec
rm dist/__init__

pyinstaller --onefile -w --hidden-import jinja2 app/__init__.py 