#!/bin/bash

echo "🖤 Kontrola formátování pomocí black..."

black --check db_utils tests --line-length 120
