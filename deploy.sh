#!/usr/bin/env bash
git add -f .secrets/
eb deploy --profile ilovefish-eb --staged
git reset HEAD .secrets/