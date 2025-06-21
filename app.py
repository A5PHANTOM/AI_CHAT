from flask import Flask, request, jsonify
from pymongo import MongoClient
import redis
import os
import json
from rag_utils import load_pdf_chunks,hybrid_rag_answer
from flask import render_template

app= Flask(__name__,template_folder='templates')
# MongoDB connection
MONGO_URI = "mongodb+srv://arjunmcseawh:r0bq8auJSfYC4JS4@cluster0.eyus4vh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
client=MongoClient(MONGO_URI)
db= client['chtat_db']    #creating db
messages_collection = db['messages'] 


#initialixtion
chunks=load_pdf_chunks("Intern_Task_.pdf")


#rediscloud connectionn

redis_client = redis.StrictRedis(
    host='redis-19208.c11.us-east-1-3.ec2.redns.redis-cloud.com',
    port=19208,
    password= 'X6mTZIz3NtmXvcr8X1YVOk69i168U7Lc',
    decode_responses=True
)


@app.route('/')
def home():
    return "Welcome to the Chat Application!"

@app.route('/send_message',methods=['POST'])
def send_message():
    data=request.json
    if not data or 'username' not in  data or 'message' not in data :
        return jsonify({'error': 'Invalid data'}), 400
    
    messages_collection.insert_one({
        'username': data['username'],
        'message': data['message']
    })

    #adding to redis cache
    cached = redis_client.get('recent_messages')
    messages = json.loads(cached) if cached else []
    messages.append({
        'username': data['username'],
        'message': data['message']
})

    messages=messages[-10:]
    redis_client.set('recent_messages',json.dumps(messages))

    return jsonify({'status':'message stored and chached sucessfully!!'})

@app.route('/get_messages', methods=['GET'])
def get_messages():
    cached = redis_client.get('recent_messages')
    if cached:
        return jsonify(json.loads(cached))

    messages =list(messages_collection.find({},{'_id': 0}))
    return jsonify(messages)

@app.route('/ask',methods=['POST'])
def ask():
    data=request.json
    query=data.get('query')
    if not query:
        return jsonify({'error':'No query provided'}),400
    
    answer=hybrid_rag_answer(chunks,query)
    return jsonify({'answer': answer})


@app.route('/chat')
def chat_ui():
    return render_template('index.html')

if __name__=='__main__':
    app.run(debug=True)

    

                      
