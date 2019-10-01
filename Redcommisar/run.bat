cd /d D://Redcommisar
heroku login
git init
heroku git:remote -a redcommisar
git add .
git commit -am "make it better"
git push heroku master