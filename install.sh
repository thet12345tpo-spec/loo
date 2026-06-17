#!/bin/bash

echo "Starting Installation..."
pkg update && pkg upgrade -y
pkg install python clang make git -y
pip install cython aiohttp requests

echo "Compiling pa.py to pa.so..."
python setup.py build_ext --inplace

# Rename the compiled file to pa.so
mv pa.*.so pa.so 2>/dev/null

echo "Setting up alias..."
# Remove old alias if exists and add new one
sed -i '/alias loo=/d' ~/.bashrc
echo "alias loo='cd ~/loo && python -c \"import pa; pa.run()\"'" >> ~/.bashrc

echo "Cleaning up..."
rm pa.py
rm setup.py
rm -rf build
rm pa.c

echo "------------------------------------------------"
echo "Installation Complete!"
echo "Please restart Termux or type: source ~/.bashrc"
echo "Then you can run the tool by typing: loo"
echo "------------------------------------------------"
