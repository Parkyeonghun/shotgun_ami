#!/usr/bin/env python3

import os
import sys
import shutil
from urllib import request

import shotgun_api3

# from handler import ShotgunAction
from download_video.file_dialog import FileDialog

class DownloadVideo:
    def __init__(self, project, selected_ids_filter, entity_type):
        # self.protocol_url = sys.argv[1]
        # self.sa = ShotgunAction(self.protocol_url)
        self.fd = FileDialog()

        SERVER_PATH = 'https://westrnd2.shotgrid.autodesk.com'
        SCRIPT_NAME = 'download_video'
        SCRIPT_KEY = '^trurx1vahkkezwyDotlzxvbs'

        self.sg = shotgun_api3.Shotgun(SERVER_PATH, SCRIPT_NAME, SCRIPT_KEY)
        
        self.filter = selected_ids_filter
        self.entity_type = entity_type
        print(self.filter)
        print(self.entity_type)

        self.download_path = self.fd.download_path(project)
        print("downloadpath ==", self.download_path)
        if self.download_path:
            print(self.download_path)
            self.run_download()

    def run_download(self):
        self.format = (".jpg", ".jpeg", ".png", ".exr", ".dpx", ".mp4", ".mov")
        for one_filter in self.filter:
            self.result_file = self.sg.find_one('Version', [one_filter], ['code', 'image', 'sg_path_to_movie', 'sg_uploaded_movie'])
  
            self.video_file_path=self.download_path+"/video"

            if self.result_file['sg_uploaded_movie'] == None and \
                self.result_file['sg_path_to_movie'] == None:
                print(self.result_file['code'], ", No [uploaded movie], [Path to Movie]")

            elif self.result_file['sg_uploaded_movie'] == None and \
                self.result_file['sg_path_to_movie']:
                print(self.result_file['code'], ", No [uploaded movie]")

                if os.path.isfile(self.result_file['sg_path_to_movie']):
                    self.download_file_from_path()
                else:
                    print("Path to Moive is incurrect")

            elif self.result_file['sg_uploaded_movie'] and \
                self.result_file['sg_path_to_movie'] == None:
                print(self.result_file['code'], ", No [Path to movie]")

                self.download_attachment()
                    
            else :
                self.download_attachment()

            self.thumnail_file_path = self.download_path + "/thumbnail"

            if self.result_file['image'] :
                self.download_thumnail_image()
            else:
                print(self.result_file['code'], ', No [image]]. Can\'t download')

            self.file_path = None
            self.result_file = None

    def download_attachment(self):
        if not os.path.isdir(self.video_file_path):
            os.makedirs(self.video_file_path)
        
        file_format = os.path.splitext(self.result_file['sg_uploaded_movie']['name'])[1]
        
        if file_format in self.format and \
            not os.path.isfile(self.video_file_path + "/" + self.result_file["code"] + file_format):
            
            self.sg.download_attachment(self.result_file['sg_uploaded_movie'], 
                                        file_path = self.video_file_path + "/" + self.result_file["code"] + file_format)
            print(self.result_file['code'], 'downloaded from [Uploaded Moive]')
        else:
            print(self.result_file['code'], 'Video already exists')

    def download_file_from_path(self):
        if not os.path.isdir(self.video_file_path):
            os.makedirs(self.video_file_path)
        
        file_format = os.path.splitext(self.result_file['sg_path_to_movie'])[1]
        
        if file_format in self.format and \
            not os.path.isfile(self.video_file_path + "/" + self.result_file["code"] + file_format):
            
            shutil.copyfile(self.result_file['sg_path_to_movie'], self.video_file_path +"/" + self.result_file["code"] + file_format)
            print(self.result_file['code'], "downloaded from [Path to Movie]")
        else:
            print(self.result_file['code'], 'Video already exists')
    
    def download_thumnail_image(self):
        if not os.path.isdir(self.thumnail_file_path):
            os.makedirs(self.thumnail_file_path)
        if not os.path.isfile(self.thumnail_file_path + "/" + self.result_file["code"] +'.jpeg'):
            request.urlretrieve(self.result_file['image'], self.thumnail_file_path + "/" + self.result_file["code"] +".jpeg")
            print(self.result_file['code'], "Thumbnail download")
        else:
            print(self.result_file['code'], 'Thumbnail already exists')

# ----------------------------------------------
# Main Block
# ----------------------------------------------
if __name__ == "__main__":
    dv = DownloadVideo()

# if os.environ.get('USER') == 't003':
