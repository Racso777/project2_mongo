'''Module for serving API requests'''

from app import app
from bson.json_util import dumps, loads
from flask import request, jsonify
import json
import ast # helper library for parsing data from string
from importlib.machinery import SourceFileLoader
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime


client = MongoClient(host="localhost", port=27017)

# Import the utils module
utils = SourceFileLoader('*', './app/utils.py').load_module()

# Select the database
db = client.careerhub

# Select the collection
collection = db.job_info

# route decorator that defines which routes should be navigated to this function
@app.route("/") # '/' for directing all default traffic to this function get_initial_response()
def get_initial_response():

    # Message to the user
    message = {
        'apiVersion': 'v1.0',
        'status': '200',
        'message': 'Welcome to careerhub on MongoDB with Web API'
    }
    resp = jsonify(message)
    # Returning the object
    return resp


@app.route("/create/jobPost", methods=['POST'])
def create_jobpost():
    '''
       Function to create new job post
    '''
    try:
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except:
            # Bad request as request body is not available
            # Add message for debugging purpose
            return "", 400

        for job in body:
            if 'title' not in job or 'industry_name' not in job:
                return jsonify({"error": "You need to specify title and industry to make a post"}), 400

        record_created = collection.insert_many(body)

        if record_created:
            inserted_id = record_created.inserted_ids
            # Prepare the response
            if isinstance(inserted_id, list):
                # Return list of Id of the newly created item

                ids = []
                for _id in inserted_id:
                    ids.append(str(_id))

                return jsonify(ids), 201
            else:
                # Return Id of the newly created item
                return jsonify(str(inserted_id)), 201

    except Exception as e:
        # Error while trying to create customers
        # Add message for debugging purpose
        print(e)
        return 'Server error', 500

@app.route('/search_by_job_id/<job_id>', methods=['GET'])
def get_by_id(job_id):
    '''
       Function to get info by job id.
    '''
    try:
        # Query the document
        result = collection.find_one({"id": int(job_id)})

        # If document not found
        if not result:
            return jsonify({"message": "Document not found"}), 404
        
        # Convert ObjectId to string for JSON serialization
        #result['job_id'] = str(result['job_id'])
        return dumps(result)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@app.route('/update_by_job_title', methods=['POST'])
def update_by_job_title():  
    '''
       Function to update by job title.
    '''
    try:
        # Get the value which needs to be updated
        try:
            body = ast.literal_eval(json.dumps(request.get_json()))
        except Exception as e:
            # Bad request as the request body is not available
            # Add message for debugging purpose
            return '', 400
        
        for job in body:
            if 'title' in job:
                title = body[0]['title']
                del body[0]['title']
                #return body[0]
            else:
                return jsonify({"error": "You need to specify title to make a change"}), 400

        # Updating the user
        records_updated = collection.update_one({'title': title}, {'$set':body[0]})

        # Check if resource is updated
        if records_updated.modified_count > 0:
            # Prepare the response as resource is updated successfully
            return records_updated.raw_result, 200
        else:
            # Bad request as the resource is not available to update
            # Add message for debugging purpose
            return 'No modification was made', 304

    except Exception as e:
        # Error while trying to update the resource
        # Add message for debugging purpose
        print(e)
        return 'Server error', 500


@app.route("/delete_by_job_title", methods=['DELETE'])
def delete_by_job_title():
    """
       Function to remove the job post.
       """
    try:
        title = request.args.get('title')

        if not title:
            return jsonify({"error": "You need to specify title to remove a job post"}), 400

        # Delete the user
        delete_title = collection.delete_one({'title':title})

        print(delete_title.raw_result)
        if delete_title.deleted_count > 0 :
            # Prepare the response
            return 'Job post removed', 204
        else:
            # Resource not found
            return 'Job post not found', 404

    except Exception as e:
        # Error while trying to delete the resource
        # Add message for debugging purpose
        print(e)
        return "", 500


@app.route("/salary_range_query", methods=['GET'])
def salary_range_query():
    '''
       Function to query salary range.
    '''
    try:
        min_salary = request.args.get('min_salary')
        max_salary = request.args.get('max_salary')

        if not min_salary or not max_salary:
            return jsonify({"error": "You need to specify min and max salary"}), 400

        # Query the document
        records_fetched = collection.find({
            'average_salary':{'$gt':int(min_salary),'$lt':int(max_salary)}
        })
        
        # If document not found
        if not records_fetched:
            return jsonify({"message": "Document not found"}), 404
    
        # Prepare the response
        return dumps(records_fetched)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/job_experience_level_query", methods=['GET'])
def job_experience_level_query():
    '''
       Function to query job experience level query.
    '''
    try:
        experience_level = request.args.get('experience_level')

        if not experience_level:
            return jsonify({"error": "You need to specify an experience level"}), 400

        # Query the document
        if experience_level == "Entry Level":
            records_fetched = collection.find({
                'years_of_experience':{'$lt':4}
            })
        elif experience_level == "Mid Level":
            records_fetched = collection.find({
                'years_of_experience':{'$gt':3,'$lt':7}
            })
        elif experience_level == "Senior Level":
            records_fetched = collection.find({
                'years_of_experience':{'$gt':6}
            })


        # If document not found
        if not records_fetched:
            return jsonify({"message": "Document not found"}), 404
    
        # Prepare the response
        return dumps(records_fetched)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route("/top_companies_industry", methods=['GET'])
def top_companies_industry_query():
    '''
       Function to query top companies in industry.
    '''
    try:
        industry = request.args.get('industry')

        if not industry:
            return jsonify({"error": "You need to specify an industry"}), 400

        # Query the document
        records_fetched = collection.aggregate([
        {
            '$match': {
                "industry_name": industry
            }
        },
        {
            '$group': {
                '_id': "$name",
                'job_listings_count': { '$sum': 1 }
            }
        },
        {
            '$sort': { 'job_listings_count': -1 }
        }
        ])
        
        # If document not found
        if not records_fetched:
            return jsonify({"message": "Document not found"}), 404
    
        # Prepare the response
        return dumps(records_fetched)

    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.errorhandler(404)
def page_not_found(e):
    '''Send message to the user if route is not defined.'''

    message = {
        "err":
            {
                "msg": "This route is currently not supported."
            }
    }

    resp = jsonify(message)
    # Sending 404 (not found) response
    resp.status_code = 404
    # Returning the object
    return resp
