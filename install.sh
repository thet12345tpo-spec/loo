#!/bin/bash

echo "Starting Installation..."
pkg update && pkg upgrade -y
pkg install python clang make git -y
pip install cython aiohttp requests

echo "Compiling pa.py to pa.so..."
python setup.py build_ext --inplace

# Rename the compiled file to pa.so (it might have a long name like pa.cpython-311.so)
mv pa.*.so pa.so 2>/dev/null

echo "Cleaning up..."
rm pa.py
rm setup.py
rm -rf build
rm pa.c

echo "------------------------------------------------"
echo "Installation Complete!"
echo "To run the tool, use the following command:"
echo "python -c 'import pa; pa.run()'"
echo "------------------------------------------------"
