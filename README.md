# project2_mongo

This project is to design a mongo docker and a python app that can access mongo docker and provide api for those accesses.

This is the schema for the mongo database.

<img width="378" alt="截屏2023-10-16 下午7 17 38" src="https://github.com/Racso777/project2_mongo/assets/111296013/fa00e5b0-4eb7-4dac-810d-4daf036c5aa1">

since there is no need for grouping seperately, I put all the columns in the csvs in the same group by the job id.


combined_data.py will combined all 5 csv files from mp2-data diretory and put them into one json file.
combined_data.json is the output of that python file.

the docker compose file can set up mongo docker and mount the mp2 file in your computer into mongo mp2 directory

we can use "mongoimport --db careerhub --collection job_info --file /mp2/combined_data.json --jsonArray" to import the json file into mongo database

run-app.py allows us to access the flash app and with the careerhub.py we can have the following apis to use for mongo database access.

api: http://127.0.0.1:5000
This is the base information for the careerhub mongo.

<img width="1147" alt="截屏2023-10-16 下午6 56 25" src="https://github.com/Racso777/project2_mongo/assets/111296013/a161265a-6e68-431a-8e54-511ad7349ce9">

api: http://127.0.0.1:5000/create/jobPost
This api allows you to make a new job post. Title and industry name must be specified.

<img width="1114" alt="截屏2023-10-16 下午6 52 08" src="https://github.com/Racso777/project2_mongo/assets/111296013/1f4e169d-cd8e-423c-9192-319f0942b2bc">

api: http://127.0.0.1:5000//update_by_job_title
This api allows you to update a job post by its title 

<img width="1141" alt="截屏2023-10-16 下午6 52 19" src="https://github.com/Racso777/project2_mongo/assets/111296013/1dfb86cf-868d-4083-a4d6-c9133eec7af2">

api: http://127.0.0.1:5000/search_by_job_id/<job_id>
This api allows you to search a job post by the job id. You need to specify the job id by input it as parameter following the api

<img width="1136" alt="截屏2023-10-16 下午6 52 29" src="https://github.com/Racso777/project2_mongo/assets/111296013/a2c57d59-6605-4a39-b045-952104747fa7">

api: http://127.0.0.1:5000/delete_by_job_title
This api allows you to delete a job post by job titile name. If successfully deleted, it will return 204 message.

<img width="1124" alt="截屏2023-10-16 下午6 55 19" src="https://github.com/Racso777/project2_mongo/assets/111296013/9a02e985-0228-4634-a5cf-3c966b385066">

api: http://127.0.0.1:5000/salary_range_query
This api allows you to search job post by salary range using two parameters min_salary and max_salary. You need to specify both of them to use this api.

<img width="1132" alt="截屏2023-10-16 下午6 55 37" src="https://github.com/Racso777/project2_mongo/assets/111296013/03c5c652-4127-4b1d-b4a7-46e4360a4495">

api: http://127.0.0.1:5000/job_experience_level_query
This api allows you to search job post by job experience level. You can input Entry Level, Mid Level, and Senior Level to search for 1-3, 4-6, above 6 years of experience requried job post.

<img width="1140" alt="截屏2023-10-16 下午6 55 52" src="https://github.com/Racso777/project2_mongo/assets/111296013/b4155dc6-6838-414c-a791-3e8a2d1ab3c8">

api: http://127.0.0.1:5000/top_companies_industry
This api allows you to search top companies that has the most number of jobs posted. id is the company name and job count is how many job posts that it has.

<img width="1160" alt="截屏2023-10-16 下午6 56 15" src="https://github.com/Racso777/project2_mongo/assets/111296013/2e6e79f5-1edd-4ab5-94d1-b188eb6c362e">







