'''
Communication with aws s3 and transcribe

@author: Nebojsa
'''
import boto3

if __name__ == '__main__':

    print("Starting...")

    # Get s3 instance
    s3 = boto3.resource('s3')

    list_of_buckets = []
    # Get all buckets from s3, adding them to list
    for bucket in s3.buckets.all():
        print("Bucket: " + bucket.name)
        list_of_buckets.append(bucket.name)

    # Using first bucket as source for audio files
    my_bucket = s3.Bucket(list_of_buckets[0])

    # Upload files to s3 (supported wav, mp3, mp4, flac)
    my_bucket.upload_file('../data/one_ring.wav', 'newname.wav')
    
    list_of_audio_files = []
    # Read all files from s3
    for obj in my_bucket.objects.all(): 
        print("File: " + obj.key)
        list_of_audio_files.append(obj.key)

    # Get transcribe instance
    transcribe = boto3.client('transcribe')

    # Making transcribe jobs for every file
    # OutputBucketName is name of the bucket where it will store json file with transciption
    for file in list_of_audio_files:
        transcribe.start_transcription_job(TranscriptionJobName=('newjob' + file),
            LanguageCode='en-US',
            MediaSampleRateHertz=16000,
            MediaFormat='wav',
            Media={
                'MediaFileUri': ('https://s3-eu-central-1.amazonaws.com/' + my_bucket.name + "/" + file)
            },
            OutputBucketName='returntextfilesvalues',
        )

    # If we want to check when the job is done (instead of newjobnewname.wav change to real job name)
    
    while True:
        status = transcribe.get_transcription_job(TranscriptionJobName="newjobnewname.wav")
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            break
        print("Not ready yet...")
        time.sleep(5)

    print("Status of job is: " + status['TranscriptionJob']['TranscriptionJobStatus'])

    print("Finished.")
