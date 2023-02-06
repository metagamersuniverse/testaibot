# testaibot

Here are the steps to create a repository and deploy your code on Heroku:

    Create a new directory for your code and navigate into it in the terminal.
    Initialize a new Git repository by running git init.
    Create a file named requirements.txt and add requests to it. This will make sure that the required library is installed on Heroku.
    Create a file named Procfile with the following content:

makefile

web: python app.py

    Create a file named app.py and copy the code you provided into it.
    Add and commit all the changes to the repository by running the following commands:

sql

git add .
git commit -m "Initial Commit"

    Create a new Heroku app by running heroku create.
    Push the code to Heroku by running git push heroku master.
    Finally, open your Heroku app by running heroku open.

Note: You'll need to replace <your_telegram_bot_token> and <your_blip_api_key> with your own values in the code and set the BLiP bucket and collection ID accordingly before running the code on Heroku.
