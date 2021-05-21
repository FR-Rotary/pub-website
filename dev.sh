#!/bin/sh

export FLASK_ENV=development
export FLASK_APP=rotary

cd website/rotary/static
ls ../../..
sass --sourcemap=none sass/style.scss:css/style.css 2>&1 | tee -a ../../../devlog/sass.log &
cd ../../
flask run 2>&1 | tee -a ../devlog/flask.log
