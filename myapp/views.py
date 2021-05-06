from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from django.contrib import messages
from django.conf import settings
import pandas as pd
import googlemaps

media_root = settings.MEDIA_ROOT
gmap_key = googlemaps.Client(key='AIzaSyBkagw73GosQC4XYPlgpjz-bWvB6VShqL4')



def file_upload(request):
    if request.method == 'POST':
        if not request.FILES.get('document'):
            messages.error(request, ('You have not selected any File. Please select a file to upload!'))
        else:
            myfile = request.FILES.get('document')
            if not myfile.name.endswith('.xls') and not myfile.name.endswith('.xlsx'):
                messages.error(request, ('Please upload only excel file!'))
            else:
                fs = FileSystemStorage()
                filename = fs.save(myfile.name, myfile)
                full_file_path = media_root + '\\' + filename
                get_geocode_result(full_file_path)

                messages.success(request, ('Congrats !!! File uploaded successfully!'))
                return render(request, 'file_upload.html')
    return render(request, 'file_upload.html')


def get_geocode_result(full_file_path):
    df = pd.read_excel(full_file_path)
    df['LAT'] = None
    df['LON'] = None
    for i in range(0, len(df), 1):
        gcode_result = gmap_key.geocode(df.iat[i, 0])
        try:
            lat = gcode_result[0]['geometry']['location']['lat']
            lon = gcode_result[0]['geometry']['location']['lng']
            df.iat[i, df.columns.get_loc('LAT')] = lat
            df.iat[i, df.columns.get_loc('LON')] = lon
        except:
            lat = None
            lon = None
    return df
