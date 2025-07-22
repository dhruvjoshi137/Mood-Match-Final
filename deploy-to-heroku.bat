@echo off
echo.
echo ## HEROKU DEPLOYMENT GUIDE FOR MOOD MATCH ##
echo.
echo Your project is ready for Heroku deployment!
echo.
echo STEP 1: Install Heroku CLI
echo Visit: https://devcenter.heroku.com/articles/heroku-cli
echo Download and install Heroku CLI for Windows
echo.
echo STEP 2: After installation, restart PowerShell and run:
echo heroku login
echo.
echo STEP 3: Connect to your existing Heroku app:
echo heroku git:remote -a mood-match-ai-e84a7a0d8c6f
echo.
echo STEP 4: Deploy your changes:
echo git push heroku main
echo.
echo STEP 5: Scale your app (if needed):
echo heroku ps:scale web=1
echo.
echo STEP 6: View logs:
echo heroku logs --tail
echo.
echo STEP 7: Open your app:
echo heroku open
echo.
echo == TROUBLESHOOTING ==
echo If you get build errors due to memory limits:
echo 1. Copy requirements-heroku.txt to requirements.txt
echo 2. git add .
echo 3. git commit -m "Use optimized requirements"
echo 4. git push heroku main
echo.
echo Your backend URL will be: https://mood-match-ai-e84a7a0d8c6f.herokuapp.com
echo.
pause
