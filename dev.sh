#!/bin/sh

# Set Flask environment variables
export FLASK_ENV=development
export FLASK_DEBUG=1
export FLASK_APP=rotary

# Change directory to the static assets directory
cd website/rotary/static

# Compile Sass to CSS, disable source maps, and log output
sass --no-source-map sass/style.scss:css/style.css 2>&1 | tee -a ../../../devlog/sass.log &

# Return to the project root directory
cd ../../

# Run Flask application and log output
flask run 2>&1 | tee -a ../devlog/flask.log