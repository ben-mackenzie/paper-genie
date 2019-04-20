from flask import Flask
from flask_cors import CORS
from api.namespaces import api

app = Flask(__name__)
api.init_app(app)
CORS(app)

# def run_interaction():
#     gene_names_file = 'gene-names.txt'
#     paper_file_name = 'corpus/1.txt'
#     return main(gene_names_file,paper_file_name)
#
# @api.route('/execute')
# class HelloWorld(Resource):
#     def get(self):
#         return run_interaction()
app.run(debug=False, host='0.0.0.0')
