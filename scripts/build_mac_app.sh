#!/usr/bin/env bash

# Build a macOS standalone application using PyInstaller
pyinstaller -n RiskOfBias -F risk_of_bias/web.py
