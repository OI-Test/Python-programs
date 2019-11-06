python3 setup.py build_ext --inplace
rm -r *.c build/
pyinstaller --onefile "run.py"
mv dist/run .
rm -r dist/ build/ *.spec *.pyx
