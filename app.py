import os
import csv
import openai
from flask import Flask, redirect, render_template, request, url_for, jsonify
import json
from flask_migrate import Migrate
import re
# import psycopg2
from flask_jwt_extended import (
    JWTManager, jwt_required, create_access_token,
    get_jwt_identity
)

from models import db, Word, AppUser, WordPrompt

app = Flask(__name__)
# openai.api_key = os.getenv("OPENAI_API_KEY")

openai.api_key = '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'

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:P0stgresap00rv@database-1.c91397hbzfpf.us-east-1.rds.amazonaws.com:5432/greprep'
app.config['JWT_SECRET_KEY'] = 'super-secret'


db.init_app(app)

migrate = Migrate(app, db)

jwt = JWTManager(app)


"""
psql postgres://postgres:P0stgresap00rv@database-1.c91397hbzfpf.us-east-1.rds.amazonaws.com:5432/bhunaksha
with app.app_context():
    db.create_all()
"""


@app.route("/", methods=("GET", "POST"))
def index():
    if request.method == "POST":
        animal = request.form["animal"]
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=generate_prompt(animal),
            temperature=0.6,
        )
        return redirect(url_for("index", result=response.choices[0].text))

    result = request.args.get("result")
    return render_template("index.html", result=result)


#@app.route('/auth', methods=['POST'])
#def authenticate():
     #username = request.json.get('username')
     #password = request.json.get('password')

     # Validate the user credentials
     #if username != 'valid_username' or password != 'valid_password':
         #return jsonify({'message': 'Invalid credentials'}), 404

    # Generate a JWT access token
     #access_token = create_access_token(identity=username)

     # Return the access token as a JSON response
     #return jsonify({'access_token': access_token}), 200
     
# log in form
@app.route('/authlogin', methods=['POST'])
def authenticate_login():
    Email=request.json.get('Email')
    Password=request.json.get('password')
     

    #validate the user credentials
    if Email !='valid_Email' or Password !='valid_password':
        return jsonify({'message':'Invalid credentials'}),404

     #generate a jwt access token
    access_token=create_access_token(identity=Email)

    #rreturn the access token as a json response
    return jsonify({'access_token':access_token}),200

    
def generate_prompt():
    start_sequence = "\nAI:"
    restart_sequence = "\nHuman: "

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="I want to give a prompt to user that starts discussion about a random topic. Also give user random GRE words that user needs to use in the response. Don't use AI as a topic. Output in json form with keys prompt and gre_word.\n",
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    text = response['choices'][0]['text']
    print(text)
    if 'Output:' in text:
        text = text.replace("o", "")

    data = json.loads(text)

    new_word = Word(name=data['gre_word'])

    db.session.add(new_word)
    db.session.commit()

    new_word_prompt = WordPrompt(
        prompt='This is an example prompt.', word_id=new_word.id)

    db.session.add(new_word_prompt)

    db.session.commit()

    return True


def get_openai_response(prompt):

    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.9,
        max_tokens=150,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0.6,
        stop=[" Human:", " AI:"]
    )

    text = response['choices'][0]['text']

    return text


def create_passage_for_mutiple_gre_words(no_of_words):
    prompt = f"Create a random passage of {no_of_words} words containing a 4-5 GRE words and also list those GRE words at the end. Give output only as key value pairs with keys passage and words."
    return get_openai_response(prompt)


def create_question_what_could_be_meaning(word):
    prompt = f"give four options 'A', 'B', 'C', 'D'. that could be meaning of word '{word}'. Give output in below format given as example, and tell which one is correct out of four."
    return get_openai_response(prompt)

def insert_words_from_csv(file_path):
    # Open the CSV file
    with open(file_path, 'r') as csv_file:
        # Use the csv library to read the contents of the file
        csv_reader = csv.reader(csv_file)

        # Skip the first row (header)
        next(csv_reader)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Get the word name from the current row
            word = row[0]
            defination = row[1]
            frequency = row[2]

            # Create a new Word object with the name from the CSV file
            word = Word(word=word,defination=defination,
                        frequency=frequency)

            # Add the Word object to the database session
            db.session.add(word)

         # open with csv file
        #with open(file_path,"r+")as csvfile:
             # use csv library to read the file
            #csv_reader = csv.reader(csv_file)

              #csv file header names
            #filename=['name','meaning','frequency']
               # write new header names
             #writer=csv.DictWriter(fieldnames=word)
             #writer.writeheader()


           # Iterate over each row in the CSV file
        #for row in csv_reader:

             #Getthe new header names in row
           # writer.writerow({
               # "word":row["name"],
                #"defination":row["meaning"],
                #"frequency":row["frequency"],
           # }
           #Add the filename object to the database session
          # db.session.add(filename)

    # Commit the changes to the database
    db.session.commit()



def insert_words_from_csv(file_path):
    # Open the CSV file
    with open(file_path, 'r') as csv_file:
        # Use the csv library to read the contents of the file
        csv_reader = csv.reader(csv_file)

        # Skip the first row (header)
        next(csv_reader)

        # Iterate over each row in the CSV file
        for row in csv_reader:
            # Get the word name from the current row
            word_name = row[0]
            meaning = row[1]
            part_of_speech = row[2]
            example = row[3]

            # Create a new Word object with the name from the CSV file
            word = Word(name=word_name, meaning=meaning,
                        part_of_speech=part_of_speech, example=example)

            # Add the Word object to the database session
            db.session.add(word)

    # Commit the changes to the database
    db.session.commit()
