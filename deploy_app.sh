#!/bin/sh

# Clear memcache
echo 'flush_all' | nc localhost 11211

#Move settings file to project dir
cp ~/stash/settings_webapp.py glynk_website/settings.py

#Gracefully restart webserver workers
sudo supervisorctl status argus_webapp | sed "s/.*[pid ]\([0-9]\+\)\,.*/\1/" | xargs sudo  kill -HUP

#Kill any celery process running
# sudo pkill celery

#Graceully restart celery
#sudo supervisorctl status glynk_celery | sed "s/.*[pid ]\([0-9]\+\)\,.*/\1/" | xargs sudo  kill -HUP

#Force restart. Uncomment above line and comment this line for graceful restart - celery@worker1
#sudo supervisorctl restart glynk_celery

#Start celery in background - celery1@app-glynk-sa. celery2@app-glynk-sa. celery3@app-glynk-sa
#celery multi restart 3 -c 5 -A trivialpolls