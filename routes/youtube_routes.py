from flask import Blueprint, request, jsonify
import os,sys
from pytube import YouTube
from pydub import AudioSegment
script_dir = os.path.dirname(os.path.abspath(__file__))
azure_python_dir = os.path.join(script_dir, '..', 'azure-python')
sys.path.append(azure_python_dir)
import mp3s_blob
youtube_routes = Blueprint('youtube_routes', __name__)


@youtube_routes.route('/upload_youtube_song_to_blob_storage', methods=['POST'])
def download_upload_router():
    data = request.get_json()
    name_of_mp3 = data.get('name_of_mp3', 'hulio')
    link = data.get('link', 'https://www.youtube.com/watch?v=RDo3PeKpvOk')
    strt_min = data.get('StrtMin', 1)
    strt_sec = data.get('StrtSec', 1)
    end_min = data.get('EndMin', 1)
    end_sec = data.get('EndSec', 20)

    try : 
        print("hello")
        file_path = download_mp3(name_of_mp3, link, strt_min, strt_sec, end_min, end_sec)
        print("kappa")
        url = mp3s_blob.upload_to_mp3s_container(file_path)
    except Exception as e:
        print(e)
        return e,400
    return {'url': url}, 200



def download_mp3(name_of_mp3="hulo", link="https://www.youtube.com/watch?v=RDo3PeKpvOk", StrtMin=1, StrtSec=1, EndMin=1, EndSec=20):
    # arguments
    yt = YouTube(link)

    # download of the file
    out_file = yt.streams.filter(only_audio=True).first().download()

    # save of the file
    base, ext = os.path.splitext(out_file)
    new_file = name_of_mp3 + '.mp3'
    os.rename(out_file, new_file)

    sound = AudioSegment.from_file(new_file)

    # Time to milliseconds conversion
    StrtTime = StrtMin*60*1000+StrtSec*1000
    EndTime = EndMin*60*1000+EndSec*1000

    # Opening file and extracting portion of it
    extract = sound[StrtTime:EndTime]
    extract = extract.fade_in(3000)
    extract = extract.fade_out(5000)
    # Saving file in required location
    extract.export(os.path.dirname(os.path.realpath(__file__)) +
                   "/mp3s/"+new_file, format="mp3")
    os.remove(new_file)

    return new_file

if __name__ == '__main__':
    download_mp3()