#!/bin/sh
set -e

# Resolve the directory this script lives in and use wait-for-it from there
SCRIPTDIR="$(cd "$(dirname "$0")" && pwd)"
# Wait once for DB to be ready
if [ -x "$SCRIPTDIR/wait-for-it.sh" ]; then
	"$SCRIPTDIR/wait-for-it.sh" db:5432 -- echo "Database is ready"
else
	# If the script is not executable (for example when the host mount overrides image permissions),
	# run it explicitly with bash so we don't get a 'Permission denied' error.
	bash "$SCRIPTDIR/wait-for-it.sh" db:5432 -- echo "Database is ready"
fi

echo "Running database migrations..."
python manage.py migrate --noinput

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."

exec gunicorn shop_analyzer.wsgi:application \
	--bind 0.0.0.0:8000 \
	--workers 3 \
	--log-level info