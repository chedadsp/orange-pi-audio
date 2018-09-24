'''
Communication with aws s3 and transcribe

@author: Nebojsa
'''
import json
import os
import argparse
import re
from wer.wer import Wer
from aws.aws_bucket_api import AwsBucket
from aws.aws_transcribe_api import AwsTranscribe
from utils.file_system_utils import FileSystemUtils


class UploadToBucketAction(argparse.Action):


    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is None or nargs != 1:
            raise ValueError("Argument is path to the folder with files for uploading.")
        super(UploadToBucketAction, self).__init__(option_strings, dest, **kwargs)


    def __call__(self, parser, namespace, values, option_string=None):
        print("Starting with process for uploading files to bucket.")
        
        aws_bucket = AwsBucket()
        file_system_utils = FileSystemUtils()
        dir_path = values
        audio_format = 'wav'

        print("Given folder for uploading: {}".format(dir_path))

        validation = file_system_utils.check_if_exist([dir_path])
    
        if not validation:
            raise("Missing folder! Check {} if exists.".format(dir_path))

        list_of_buckets = aws_bucket.get_list_of_buckets()

        # Check
        if (len(list_of_buckets) < 2):
            raise("Need two or more buckets, one for loading files, one for storing results.")
        
        # Using first bucket as source for audio files
        bucket_with_files = list_of_buckets[0]
        print("Uploading to bucket named: {}".format(bucket_with_files.name))

        # Upload files to s3 (supported wav, mp3, mp4, flac)
        aws_bucket.upload_files_to_bucket(bucket_with_files, dir_path, 
                               file_system_utils.get_list_of_file_names_in_directory(dir_path, audio_format))

        print("Uploading is done.")


class StartTranscribeJobsAction(argparse.Action):


    def __init__(self, option_strings, dest, nargs=0, **kwargs):
        if nargs != 0:
            raise ValueError("No arguments for this process.")
        super(StartTranscribeJobsAction, self).__init__(option_strings, dest, **kwargs, nargs=nargs)


    def __call__(self, parser, namespace, values, option_string=None):
        print("Starting with process for running transcribe jobs.")
        aws_bucket = AwsBucket()
        aws_transcribe = AwsTranscribe()
        aws_uri = 'https://s3-eu-west-1.amazonaws.com/'
        audio_format = 'wav'
        language_code = 'en-US'
        sample_rate = 16000

        list_of_buckets = aws_bucket.get_list_of_buckets()

        # Check
        if (len(list_of_buckets) < 2):
            print("Need two or more buckets, one for loading files, one for storing results.")
            return

        # Using first bucket as source for audio files
        bucket_with_files = list_of_buckets[0]
        # Using second bucket as place to store results
        bucket_for_storing = list_of_buckets[1]

        print("Getting files from bucket named: {}".format(bucket_with_files.name))
        print("Uploading results to bucket named: {}".format(bucket_for_storing.name))

        # Getting all files on first bucket
        list_of_audio_files = aws_bucket.get_list_of_file_names_from_bucket(bucket_with_files)
        bucket_uri = aws_uri + bucket_with_files.name + "/"

        # Making transcribe jobs for every file
        # OutputBucketName is name of the bucket where it will store json file with transciption
        for file in list_of_audio_files:
            file_without_extension = file.replace("." + audio_format, "")
            aws_transcribe.start_transcribe_job_for_every_file(file, language_code, sample_rate, 
                                        audio_format, bucket_uri, bucket_for_storing, file_without_extension)
            aws_transcribe.check_if_job_is_done(file_without_extension)

        print("All jobs are done.")


class DownloadResultsAction(argparse.Action):


    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is None or nargs != 1:
            raise ValueError("Argument is path to the folder where to download files.")
        super(DownloadResultsAction, self).__init__(option_strings, dest, **kwargs)


    def __call__(self, parser, namespace, values, option_string=None):
        print("Starting with process for word error rate algorithm.")
        results_folder_path = values
        aws_bucket = AwsBucket()
        list_of_buckets = aws_bucket.get_list_of_buckets()

        # Check
        if (len(list_of_buckets) < 2):
            print("Need two or more buckets, one for loading files, one for storing results.")
            return
        # Using second bucket as place to store results
        bucket_for_storing = list_of_buckets[1]

        file_system_utils.make_folder(results_folder_path)

        validation = file_system_utils.check_if_exist([results_folder_path])
    
        if not validation:
            raise("Missing folder! Check {} if exists.".format(results_folder_path))

        # Read all files from s3
        aws_bucket.download_all_files_from_bucket(bucket_for_storing, results_folder_path)

        print("Downloading is done.")


class TestWerAction(argparse.Action):


    def __init__(self, option_strings, dest, nargs=None, **kwargs):
        if nargs is None or nargs != 1:
            raise ValueError("Argument is path to the folder with results.")
        super(TestWerAction, self).__init__(option_strings, dest, **kwargs)


    def __call__(self, parser, namespace, values, option_string=None):
        print("Starting with process for downloading results.")
        results_folder_path = values
        text_for_comparing_folder_path = './text_for_comparing/'
        file_system_utils = FileSystemUtils()
        wer = Wer()
        print("Reading all files from result directory: {}".format(results_folder_path))
        list_of_json_files = file_system_utils.get_list_of_file_names_in_directory(results_folder_path)
        # Reading json files
        for file in list_of_json_files:

            # There are files for access rights, ignoring those
            if (not file.endswith('.json')):
                continue

            try:
                with open(results_folder_path + file) as f:
                    print("Reading {}".format(results_folder_path + file))
                    result_data = json.load(f)

                reference_file = file.replace('json', 'txt')
                with open(text_for_comparing_folder_path + reference_file) as f:
                    print("Reading {}".format(text_for_comparing_folder_path + reference_file))
                    reference_data = f.read()
            except:
                print("Something is wrong with files! Check if compare files have same name or if program has read permission.")
                raise
            
            # Aws Transcribe is returning string with interpuctions and large letters, this makes sure it's removed for most accurate results
            hypotesis_string = re.sub(r'[,.!]', '', result_data['results']['transcripts'][0]['transcript']).lower()
            
            print("***********************************************************************************")
            print(wer.wer(reference_data, hypotesis_string, True))
            print("***********************************************************************************")

        print("Comparing results with expected value is done.")


def parse_input_arguments():
    parser = argparse.ArgumentParser(description='inputs for script')
    group = parser.add_mutually_exclusive_group()

    group.add_argument('-upf', '--upload-files',
                        help='Upload audio files to given s3 bucket. Argument is folder path with \
                                audio files for uploading.',
                        nargs=1,
                        default='../audio_data_wav/',
                        action=UploadToBucketAction)

    group.add_argument('-st', '--start-transcribe',
                        help='For every file in given s3 bucket, start new transcribe job.',
                        nargs=0,
                        action=StartTranscribeJobsAction)

    group.add_argument('-dr', '--download-results',
                        help='Download results from given s3 bucket. Argument is folder path where to download results.',
                        nargs=1,
                        default='../results_from_transcribe/',
                        action=DownloadResultsAction)

    group.add_argument('-wer', '--test-wer',
                        help='Run the wer algorithm for every file in results folder. Argument is path to result folder.',
                        nargs=1,
                        default='../results_from_transcribe/',
                        action=TestWerAction)

    args = parser.parse_args()


if __name__ == '__main__':
    print("Welcome to system for testing.")

    parse_input_arguments()

    print("Goodbye, have a nice day!")