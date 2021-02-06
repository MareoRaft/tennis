this entire repo is less than 500 MB

# Dev README
This is the repo for the **frontend** of the Tennis Capstone Project for TDI (The Data Incubator).  The repo for the [**backend** is here](https://github.com/MareoRaft/tennis-backend-tdi).  The actual [deployed app is here](https://tennis-frontend-tdi.herokuapp.com).


## Docker dev

NOT IN USE:

    docker build -t mvlancellotti/tennis-frontend:dev -f dev.Dockerfile . && docker run --rm -it -p 5001:5001 -e CHOKIDAR_USEPOLLING=true -v $(pwd):/home/node/app mvlancellotti/tennis-frontend:dev

## Docker prod

    docker build -f prod.Dockerfile -t mvlancellotti/tennis-frontend:prod . && docker run --rm -it -p 5001:80 -e CHOKIDAR_USEPOLLING=true --name tennis-frontend-container mvlancellotti/tennis-frontend:prod





See <https://mherman.org/blog/dockerizing-a-react-app/> for more, and a prod example.




## Run
You can optionally do `export PORT=3000` or similar to fix the port.  In PROD it's always 80 automatically.

    npm run dev
    # do NOT do `heroku local`, since that would run the start command, which is now reserved for production build


## Build & Deploy
Heroku has built-in support for "create-react-app" apps.  Therefore, pushing updates to heroku is enough.  Heroku should do the rest.  Make sure the Heroku config vars are set properly.

	git push heroku master



## Notes

  * This project was bootstrapped with [Create React App](https://github.com/facebook/create-react-app).
