#!flask/bin/python
import time
from modeling import Model
from modeling import LemmasPt
from flask import Flask, request
from flask_restplus import Api, Resource
from main import classify_subject

flask_app = Flask(__name__)
app = Api(app = flask_app, version="1.0", title="Subject Analyzer")

name_space = app.namespace('subjectanalyzer/rating', description="Get subject quality")
@name_space.route("/")
class RatingClass(Resource):

    @name_space.doc(responses={ 200: 'OK', 500: 'Server Internal Error'}, params={'country' : 'Specify the customer country', 'sector' : 'Specify the customer business sector', 'subject':'Specify the subject to be analyzed'})
    def get(self):
        country = request.args.get('country')
        sector = request.args.get('sector')
        subject = request.args.getlist('subject')
        
        if (country is None and sector is None and subject is None) or not subject: 
            return 1   
 
        quality = classify_subject(country, sector, str(subject[0]), Model.get_instance(), LemmasPt.get_instance())

        return int(quality[0])   

if __name__ == '__main__':
    flask_app.run(host='0.0.0.0', debug=True)