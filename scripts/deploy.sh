source '.env'

if test -z "${APP_NAME}"
then
    echo "Please provide an APP_NAME variable for deploy."
else
    cf push "${APP_NAME}"
fi