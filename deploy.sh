#!/usr/bin/env bash
git add -f .secrets/
eb deploy --profile coffeecalorie-eb --staged
git reset HEAD .secrets/