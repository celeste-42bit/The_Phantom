echo "Welcome to The Phantom installer"

FILE=./requirements.txt
if ! [[ -f "$FILE" ]]; then
    echo "Please run this installer in the source directory!"
    sleep 2
    exit
fi

echo "Getting things ready..."

python3 -m venv env
source ./env/bin/activate
python3 -m pip install -r ./requirements.txt

mv ./template_config.yaml ./config.yaml

python3 -m ./installer.py

echo "DONE!"
sleep 2
exit