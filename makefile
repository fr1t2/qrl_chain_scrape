venv:
 pip install pip-tools
 pip-compile requirements.in
 pip install -r requirements.txt
check_compile:
 pip-compile --quiet requirements.in && git diff --exit-code
build: | venv
 pip install setuptools wheel
 python setup.py sdist bdist_wheel

#build:
# pip install twine
# twine upload --repository-url https://api.packagr.app/${PACKAGR_HASH_ID} dist/* -u $PACKAGR_USERNAME -p $PACKAGR_PASSWORD