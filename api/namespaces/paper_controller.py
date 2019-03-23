import os

from flask import request
from flask_restplus import Namespace, Resource, fields
from werkzeug.datastructures import FileStorage
from werkzeug.utils import secure_filename

import api.services.gene_interaction_detector as detector

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

interaction = api.model('Interaction',interaction)
gene_model = api.model('Gene Model', {
    'name': fields.String(description="Name of the gene"),
    'known_interactions': fields.List(fields.Nested(interaction), description="Interactions with other genes")
})


response = api.model('Paper', {
    'detected_genes': fields.List(fields.Nested(gene_model), required=True, description="A list of genes detected in the paper")
})

parser = api.parser()
parser.add_argument('file', type=FileStorage, location='files', required=True)

# paths
gene_names_file = './genes/reviewed-home-sapien-genes.tab'
UPLOAD_FOLDER = '../uploaded_papers'

gene_names = detector.read_genes_from_tsv(gene_names_file, ['Gene names  (primary )', 'Gene names  (synonym )'])


@api.route('/analyze')
class Paper(Resource):
    @api.doc(id='analyze_paper', description='Upload a paper to analyze')
    @api.expect(parser, validate=True)
    @api.marshal_with(response)
    def post(self):
        paper_file = request.files['file']

        if not os.path.exists(UPLOAD_FOLDER):
            os.makedirs(UPLOAD_FOLDER)

        paper_file.save(os.path.join(UPLOAD_FOLDER, secure_filename(paper_file.filename)))
        paper_file_name = os.path.join(UPLOAD_FOLDER, paper_file.filename)

        detected_genes = detector.detect_genes(gene_names, paper_file_name)
        res = {"detected_genes": detected_genes}
        return res
