#!/bin/bash

rm *.spec
rm ./dist/*

pyinstaller --onefile -w app/__init__.py 