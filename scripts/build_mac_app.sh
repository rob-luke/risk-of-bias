#!/usr/bin/env bash

# Build a macOS standalone application using PyInstaller
pyinstaller --onefile --windowed -n RiskOfBias risk_of_bias/web.py
