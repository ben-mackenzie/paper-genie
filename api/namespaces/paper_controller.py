import os

from flask import request
from flask_restplus import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

from api.services.gene_interaction_detector import detect_genes

api = Namespace('paper', description="Paper related operations")

interaction = {}
interaction["preferredName_A"] = fields.String
interaction["fscore"] = fields.Float
interaction["tscore"] = fields.Float
interaction["score"] = fields.Float
interaction["ascore"] = fields.Float
interaction["ncbiTaxonId"] = fields.String
interaction["pscore"] = fields.Float
interaction["nscore"] = fields.Float
interaction["dscore"] = fields.Float
interaction["stringId_A"] = fields.String
interaction["escore"] = fields.Float
interaction["preferredName_B"] = fields.String
interaction["stringId_B"] = fields.String

# interaction = api.model('Interaction',interaction)
gene_model = api.model('Gene Model', {
    'name': fields.String(description="Name of the gene"),
    'interactions': fields.List(fields.Nested(interaction), description="Interactions with other genes")
})


response = api.model('Paper', {
    'detected_genes': fields.List(fields.Nested(gene_model), required=True, description="A list of genes detected in the paper")
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
