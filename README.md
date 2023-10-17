# project2_mongo

This project is to design a mongo docker and a python app that can access mongo docker and provide api for those accesses.

This is the schema for the mongo database

combined_data.py will combined all 5 csv files from mp2-data diretory and put them into one json file.
combined_data.json is the output of that python file.

the docker compose file can set up mongo docker and mount the mp2 file in your computer into mongo mp2 directory

we can use "mongoimport --db careerhub --collection job_info --file /mp2/combined_data.json --jsonArray" to import the json file into mongo database

run-app.py allows us to access the flash app and with the careerhub.py we can have the following apis to use for mongo database access.

api: http://127.0.0.1:5000

<img width="1147" alt="截屏2023-10-16 下午6 56 25" src="https://github.com/Racso777/project2_mongo/assets/111296013/a161265a-6e68-431a-8e54-511ad7349ce9">
