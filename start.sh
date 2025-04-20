# change directory
cd ./devops/prod/
#shutdown
docker compose down
# start
docker compose up -d --build
# migrate db
docker compose exec web python manage.py migrate --noinput
# collectstatic files
docker compose exec web python manage.py collectstatic --no-input
