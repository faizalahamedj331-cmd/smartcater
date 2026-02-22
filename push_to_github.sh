#!/bin/bash
cd "c:/Users/FAIZAL AHAMED/OneDrive/Desktop/smartcater"
git init
git add .
git commit -m "Initial commit - SmartCater Django application"
gh repo create faizalahamedj331-cmd/smartcater --source=. --public --push
