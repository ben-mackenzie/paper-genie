import os

from flask import request
from flask_restplus import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from api.services.gene_interaction_detector import detect_genes

api = Namespace('paper', description="Paper related operations")

gene_model = fields.String(description='A gene')

response = api.model('Paper', {
    'detected_genes': fields.List(gene_model, required=True, description="A list of genes detected in the paper")
})

parser = api.parser()
parser.add_argument('file', type=FileStorage, location='files', required=True)

# paths
gene_names_file = '../gene-names.txt'
UPLOAD_FOLDER = '../uploaded_papers'


@api.route('/analyze')
class Paper(Resource):
    @api.doc(id='analyze_paper', description='Upload a paper to analyze')
    @api.expect(parser, validate=True)
    @api.marshal_with(response)
    def post(self):
        file = request.files['file']

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        file.save(os.path.join(UPLOAD_FOLDER, secure_filename(file.filename)))
        detected_genes = detect_genes(gene_names_file, os.path.join(UPLOAD_FOLDER, file.filename))
        res = {"detected_genes": detected_genes}
        return res
