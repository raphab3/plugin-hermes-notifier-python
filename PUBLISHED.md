python3 -m venv venv
source venv/bin/activate
pip install build twine
python -m build
git add .
git commit -m "feat: initial commit - v1.1.0"
git push origin main
twine upload dist/*