from PyPDF2 import PdfReader
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView
from text_processor.consts import MAX_PDF_FILE_PAGES_NUM
from text_processor.serializers import FileUploadSerializer
from text_processor.utils import summarize_text


class SummarizePDF(APIView):
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer(self, *args, **kwargs):
        return FileUploadSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        if 'file' not in request.FILES:
            return Response({"error": "No file provided"}, status=status.HTTP_400_BAD_REQUEST)

        pdf_file = request.FILES['file']
        reader = PdfReader(pdf_file)
        pages = reader.pages

        if len(pages) > MAX_PDF_FILE_PAGES_NUM:
            return Response({
                "error": "Max pages limit exceeded. Max number of pages: " + str(MAX_PDF_FILE_PAGES_NUM)},
                status=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE
            )

        text = ""
        for page in pages:
            text += page.extract_text()

        try:
            summary = summarize_text(text)
        except Exception as e:  # TODO: implement more diverse exceptions (with other statuses)
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return Response({"summary": summary}, status=status.HTTP_200_OK)
