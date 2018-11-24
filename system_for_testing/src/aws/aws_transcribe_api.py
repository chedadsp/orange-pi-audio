import boto3
import time


class AwsTranscribe():

    def __init__(self):
        self.transcribe = boto3.client('transcribe')
        self.transcribe_job_prefix = 'new_job_for_'


    def set_job_prefix(self, new_prefix):
        self.transcribe_job_prefix = new_prefix


    def start_transcribe_job_for_every_file(self, file_name, language_code, sample_rate, media_format, bucket_uri, bucket_for_result, file_without_extension):
        try:
            print("Starting job for audio file: {}.".format(file_name))
            self.transcribe.start_transcription_job(TranscriptionJobName=(self.transcribe_job_prefix + file_without_extension),
                LanguageCode='en-US',
                MediaSampleRateHertz=sample_rate,
                MediaFormat=media_format,
                Media={
                    'MediaFileUri': (bucket_uri + file_name)
                },
                OutputBucketName=bucket_for_result.name,
            )
            print("Job started.")
        except:
            raise


    def check_if_job_is_done(self, file_name):
        print("Checking if job for {} is done...".format(file_name))
        job_name = self.transcribe_job_prefix + file_name
        while True:
            status = self.transcribe.get_transcription_job(TranscriptionJobName=job_name)
            if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
                break
            print("Not ready yet...")
            time.sleep(5)

        print("Status of job {} is: {}".format(job_name, status['TranscriptionJob']['TranscriptionJobStatus']))