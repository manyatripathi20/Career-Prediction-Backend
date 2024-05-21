from flask import Flask, request, jsonify, send_from_directory
import pandas as pd
import json
from flask_cors import CORS , cross_origin


app = Flask(__name__,static_folder="../dist",static_url_path="")
CORS(app)

carrier_mapping={6: 'Software Developer', 7: 'Teacher/Educator', 4: 'No suitable match', 0: 'Artist', 1: 'Athlete', 3: 'Doctor', 5: 'Scientist/Researcher', 2: 'Chef'}
# Career options dictionary
career_options = {
    "Software Developer": {"Programming", "Logical Thinking", "Coding", "Problem Solving", "Mathematics", "Team Management"},
    "Scientist/Researcher": {"Problem Solving", "Mathematics", "Logical Thinking", "Research", "Analytical Skills", "Data Analysis"},
    "Artist": {"Art", "Creative Writing", "Music", "Photography", "Painting", "Sculpting", "Drawing"},
    "Chef": {"Culinary Arts", "Creativity", "Attention to Detail", "Cooking", "Baking", "Food Presentation", "Menu Planning"},
    "Teacher/Educator": {"Public Speaking", "Leadership", "Subject Knowledge", "Teaching", "Curriculum Development", "Classroom Management"},
    "Doctor": {"Medical Knowledge", "Problem Solving", "Attention to Detail", "Critical Thinking", "Empathy", "Patient Care"},
    "Athlete": {"Physical Fitness", "Sports Skills", "Teamwork", "Endurance", "Determination", "Discipline"}
} 

def find_career_path(skills_list, career_options):
    max_matching_skills = 0
    most_appropriate_career = "No suitable Career for you"

    for career, career_skills in career_options.items():
        matching_skills = len(set(skills_list) & career_skills)
        if matching_skills > max_matching_skills:
            max_matching_skills = matching_skills
            most_appropriate_career = career

    return most_appropriate_career

@app.route("/")
@cross_origin()
def index():
  return send_from_directory(app.static_folder,"index.html")
@app.errorhandler(404)
@cross_origin()
def not_found(e):
  return send_from_directory(app.static_folder,'index.html')

@app.route("/predict", methods=["POST"])
def predict():
    data=request.get_json()
    data["Skills"]=[skill.strip() for skill in data["Skills"].split(",")]
    Skills_list = data["Skills"]
    input=[]
    for sub in data.values():
        if type(sub)==list:
            for x in sub:
                input.append(x)
        else:
            input.append(sub)

    data = pd.DataFrame([input], columns=["Name","Sex","Age","10th","12th","Stream","IQ","General Test Score","Skill1","Skill2","Skill3","Skill4","Competetive Exam"])
    name = data['Name'][0]
 
    career = find_career_path(
        Skills_list,career_options
    )
    print(career)
    return  jsonify({'username': name,
                     'career': career
                     })


if __name__ == "__main__":
  app.run(debug=True)