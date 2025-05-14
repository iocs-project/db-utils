#!/bin/bash
echo "Kontrola flake8..."

flake8 db_utils tests --max-line-length 120
