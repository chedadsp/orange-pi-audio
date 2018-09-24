# orange-pi-audio

Orange PI zero audio related stuff

# audio recorder

Python (version 3) program for running Flask server that can record a sound.
It's going to be visible in local network with upnp implementation.

#### Requirements:

* Run requirements.bat or requirements.sh to install required python libraries. Script is going to install Flask, pyaudio, wave and miniupnpc with pip3.

#### Running:

Run main.py to run the server.
```
python3 audio_recorder/src/main.py
```

# system for testing

Python (version 3) program for testing voice recognition accuracy.

It's using aws boto3 library to communicate with S3 and Transcribe.
First S3 bucket is used to store audio files, read them and send them
to aws Transcribe for automatic speech recognition. Second bucket is used
for aws Transcribe to store json result files.

It's using WER algorithm to calculate difference between reference and aws result.
It's writting results in procent and it's writting all the words and operations so
user can see what's happening.

#### Requirements:

* Run requirements.bat or requirements.sh to install required python libraries. Script is going to install boto3 with pip3.

* Set up credentials (in e.g. *~/.aws/credentials*):

```
[default]
aws_access_key_id = YOUR_KEY
aws_secret_access_key = YOUR_SECRET
```

* Then, set up a default region (in e.g. *~/.aws/config*):

```
[default]
region=eu-west-1
```

* Create two S3 buckets that are going to be used as described. Create access key for your aws account.

Helpful description in [aws documentation](https://docs.aws.amazon.com/transcribe/latest/dg/getting-started-python.html).

#### Running:

Run different bash scripts for different actions:

* Uploading audio files to s3 bucket:
```
system_for_testing/upload_audio_files.sh
```

* Running transcribe jobs:
```
system_for_testing/start_transcribe_jobs.sh
```

* Downloading results from s3 bucket that transcribe jobs provided:
```
system_for_testing/download_results.sh
```

* Run Word error rate algorithm:
```
system_for_testing/run_wer.sh
```

These scripts are calling system_for_testing/src/main.py with different parameters, look into them to
see how to call python script directly.
