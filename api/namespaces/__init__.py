from flask_restplus import Api
from .paper_controller import api as ns1

api = Api(
    title='Gene Paper Analyzer',
    version='1.0',
    description='APIs to analyze papers containing interactions with genes',
    # All API metadatas
)

api.add_namespace(ns1)