import tempfile

from flask import request
from flask_restful import Resource, reqparse, abort

from core.extractor.entity.extract_setting import ExtractSetting
from core.extractor.extract_processor import ExtractProcessor
from web import api


class FileExtractor(Resource):
    """
    A Flask-RESTful resource for extracting text from uploaded files.

    This resource accepts POST requests with a file part, saves the file to a temporary directory,
    and then processes the file to extract text. The extracted text is returned in the response.
    """

    def post(self):
        """
        Handle a POST request to the TextExtractor resource.

        The request should include a file part with the key 'file'. If the file part is missing,
        or if no file is selected, an error message is returned.

        The file is saved to a temporary directory, and then processed to extract text. The
        extracted text is returned in the response as a list of documents, where each document
        is a dictionary that can be serialized to JSON.

        Returns:
            A dictionary that can be serialized to JSON. If the request is successful, the
            dictionary contains a single key-value pair, where the key is 'documents' and the
            value is a list of documents. Each document is a dictionary that represents the
            extracted text.

            If the request is not successful, the dictionary contains a single key-value pair,
            where the key is 'error' and the value is an error message.
        """
        if 'file' not in request.files:
            abort(400, message='No file part')

        file = request.files['file']
        if file.filename == '':
            abort(400, message='No selected file')

        with tempfile.TemporaryDirectory() as temp_dir:
            file_path = f"{temp_dir}/{file.filename}"
            file.save(file_path)

            documents = ExtractProcessor.extract(ExtractSetting(), file_path=file_path)

        return {'documents': [document.to_dict() for document in documents]}


class WebExtractor(Resource):
    """
    A Flask-RESTful resource for extracting text from web pages.

    This resource accepts POST requests with a form part 'url', fetches the content of the web page,
    and then processes the content to extract text. The extracted text is returned in the response.
    """

    def post(self):
        """
        Handle a POST request to the WebExtractor resource.

        The request should include a form part with the key 'url'. If the 'url' part is missing,
        an error message is returned.

        The content of the web page is fetched and then processed to extract text. The
        extracted text is returned in the response as a list of documents, where each document
        is a dictionary that can be serialized to JSON.

        Returns:
            A dictionary that can be serialized to JSON. If the request is successful, the
            dictionary contains a single key-value pair, where the key is 'documents' and the
            value is a list of documents. Each document is a dictionary that represents the
            extracted text.

            If the request is not successful, the dictionary contains a single key-value pair,
            where the key is 'error' and the value is an error message.
        """
        target_url = request.form.get('url')
        if not target_url:
            abort(400, message='No url provided')

        documents = ExtractProcessor.load_from_url(target_url)

        return {'documents': [document.to_dict() for document in documents]}


api.add_resource(FileExtractor, '/extractor/file')
api.add_resource(WebExtractor, '/extractor/url')
