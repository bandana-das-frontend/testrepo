#!/bin/sh

# Clear memcache
echo 'flush_all' | nc localhost 11211

#Move settings files to project dir
cp ~/stash/settings_webapp.py glynk_website/settings.py

#Gracefully restart webserver workers
sudo supervisorctl status argus_celery | sed "s/.*[pid ]\([0-9]\+\)\,.*/\1/" | xargs sudo  kill -HUP

#Kill any celery process running
sudo pkill celery

#Graceully restart celery
#sudo supervisorctl status glynk_celery | sed "s/.*[pid ]\([0-9]\+\)\,.*/\1/" | xargs sudo  kill -HUP

#Force restart. Uncomment above line and comment this line for graceful restart - celery@worker1
sudo supervisorctl restart argus_celery

#Start celery in background - celery1@app-glynk-sa. celery2@app-glynk-sa. celery3@app-glynk-sa
celery multi restart 2 -c 2 -A glynk_website