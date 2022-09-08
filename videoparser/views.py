from django.core.files.storage import FileSystemStorage
from django.shortcuts import render
from django.views.generic import View
from .tasks import subtitle_extraction
from bezen import dynamodb_table
from boto3.dynamodb.conditions import Attr
from django.template.defaulttags import register


@register.filter
def get_value(dictionary, key):
    return dictionary.get(key)


class UploadView(View):
    """Handles request for get and post method of uploading file.
    """

    def get(self, request):
        return render(request, 'videoparser/index.html')

    def post(self, request):
        file_to_upload = request.FILES.get('video')
        fs = FileSystemStorage()  # defaults to MEDIA_ROOT
        filename = fs.save(file_to_upload.name, file_to_upload)
        subtitle_extraction.delay(f"./media/{filename}", file_to_upload.name)

        return render(request, 'videoparser/index.html', {
            'message': 'File uploaded successfully'
        })


class VideoListView(View):
    """Handles the request for listing all videos available in the database.
    """

    def get(self, request):
        response = dynamodb_table.scan(
            FilterExpression=Attr('video_name').exists()
        )
        items = response['Items']
        context = {'videos': items}
        return render(request, 'videoparser/video_list.html', context)


class SearchSubtitlesView(View):
    """Handles request for searching subtitles from the video.
    """
    def get(self, request, subtitle_id):
        return render(request, 'videoparser/search_subtitle.html')

    def post(self, request, subtitle_id):
        if phase := request.POST.get('phrase').upper():
            response = dynamodb_table.scan(
                FilterExpression=Attr('video_id').exists() & Attr('video_id').eq(subtitle_id) & Attr('text').contains(phase)
            )
            items = response['Items']
            context = {'values': items, 'phase': phase}
            return render(request, 'videoparser/result.html', context)
        return render(request, 'videoparser/search_subtitle.html')
