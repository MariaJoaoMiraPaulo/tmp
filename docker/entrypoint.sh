#installing requirements
pip install -r $(pwd)/requirements.txt

#Installing languages
python -m spacy download en
python -m spacy download es
python -m spacy download pt

#scheduling monthly task 
chmod +x $(pwd)/update.sh
cat $(pwd)/cron >> /etc/crontab
crontab /etc/crontab
crond

python api.py