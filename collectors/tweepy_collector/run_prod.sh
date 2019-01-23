source environment/py_environment/bin/activate;
pip3 install -r requirements.txt --user;
cd src;

setsid python3 people_collector.py ../config/config.json people_data --env PROD;
setsid python3 posts_collector.py ../config/config.json posts_data --env PROD;
