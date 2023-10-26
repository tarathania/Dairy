from flask import Flask, render_template, jsonify, request
from pymongo import MongoClient
from datetime import datetime
import certifi

cert = certifi.where()

client = MongoClient('mongodb+srv://test:sparta@cluster0.nrbqjbm.mongodb.net/', tlsCAFile=cert)

db = client.dbsparta

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})

@app.route('/diary', methods=['POST'])
def save_diary():
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]
    
    today = datetime.now()
    myTime = today.strftime('%Y-%m-%d-%H-%M-%S')

    file = request.files['file_give']
    extension = file.filename.split('.')[-1]
    filename = f'static/post-{myTime}.{extension}'
    file.save(filename)

    profile = request.files['profile_give']
    extension = profile.filename.split('.')[-1]
    profilename = f'static/profile-{myTime}.{extension}'
    profile.save(profile)

    doc = {
        'file': filename,
        'profile': profilename,
        'title':title_receive,
        'content':content_receive
    }
    db.diary.insert_one(doc)
    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)