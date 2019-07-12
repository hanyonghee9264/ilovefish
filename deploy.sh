#!/usr/bin/env bash
git add -f .secrets/
git add -f .static/
eb deploy --profile coffeecalorie-eb --staged
git reset HEAD .secrets/
git reset HEAD .static/