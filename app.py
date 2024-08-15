from flask import Flask, request, jsonify, make_response, render_template
from flask_sqlalchemy import SQLAlchemy
from os import environ
import pandas as pd
import csv
from io import StringIO
from datetime import datetime
elapsed_time = 0.00
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = environ.get('DB_URL')
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def json(self):
        return {'id': self.id,'username': self.username, 'email': self.email}
db.create_all()

@app.route('/test', methods=['GET'])
def test():
  return make_response(jsonify({'message': 'test route'}), 200)

# create a user
@app.route('/users', methods=['POST'])
def create_user():
  try:
    start_time = datetime.now()
    data = request.get_json()
    new_user = User(username=data['username'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    global elapsed_time
    elapsed_time = datetime.now() - start_time
    return make_response(jsonify({'message': 'user created', 'elapsed-time': f"{elapsed_time.total_seconds()}"}), 201)
  except Exception as e:
    return make_response(jsonify({'message': 'error creating user'}), 500)

# get all users
@app.route('/users', methods=['GET'])
def get_users():
  try:
    users = User.query.all()
    return make_response(jsonify([user.json() for user in users]), 200)
  except Exception as e:
    return make_response(jsonify({'message': 'error getting users'}), 500)

# time control for service health
@app.route('/time', methods=['GET'])
def time():
  try:
    return make_response(str(elapsed_time.total_seconds()), 202)
  except Exception as e:
    return make_response("timing not found", 500)


# get a user by id
@app.route('/users/<int:id>', methods=['GET'])
def get_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      return make_response(jsonify({'user': user.json()}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error getting user'}), 500)

@app.route('/upload', methods=['POST'])
def upload_file():
  try:
   if 'file' not in request.files:
     return jsonify({'error':'No file'})

   raw_file = request.files['file']
   print("recieved file")
   df = pd.read_csv(StringIO(raw_file.read().decode('utf-8')))
   print("csv file went successful")
#   return make_response(jsonify({'message': 'file uploads successfully dumbo'}), 201)
   return data_processing(df)
  except Exception as e:
    return make_response(jsonify({'message': 'error processing file'}), 500)

def data_processing(pfile):
  try:
    discarded_users = []
    start_time = datetime.now()
    for index,row in pfile.iterrows():
      try:
        new_user = User(username=row['username'], email=row['email'])
        db.session.add(new_user)
        db.session.commit()
      except:
        discarded_users.append(row['username'])
    global elapsed_time
    elapsed_time = datetime.now() - start_time
    if not discarded_users:
      return make_response(jsonify({'message':'users created successfully'}),201)
    return make_response(jsonify({'discarded users':f'{discarded_users}','message':'users created with discarded users'}),201)
  except Exception as e:
     return make_response(jsonify({'message': 'error creating user'}), 500)


# update a user
@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      data = request.get_json()
      user.username = data['username']
      user.email = data['email']
      db.session.commit()
      return make_response(jsonify({'message': 'user updated'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error updating user'}), 500)

# delete a user
@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
  try:
    user = User.query.filter_by(id=id).first()
    if user:
      db.session.delete(user)
      db.session.commit()
      return make_response(jsonify({'message': 'user deleted'}), 200)
    return make_response(jsonify({'message': 'user not found'}), 404)
  except e:
    return make_response(jsonify({'message': 'error deleting user'}), 500)
