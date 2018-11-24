import boto3
import os


class AwsBucket():

    def __init__(self):
        self.s3 = boto3.resource('s3')
        self.transcribe_job_prefix = 'new_job_for_'


    def get_s3_object(self):
        return self.s3


    def get_list_of_file_names_from_bucket(self, bucket):
        list_of_file_names = []
        # Read all files from s3
        try:
            for obj in bucket.objects.all():
                list_of_file_names.append(obj.key)
        except:
            raise

        return list_of_file_names

    def get_list_of_buckets(self):
        # Get all buckets from s3, as list
        try:
            return list(self.s3.buckets.all())
        except:
            raise


    def upload_files_to_bucket(self, bucket, directory_path, list_of_file_names, list_of_new_names=None):
        if (list_of_new_names is None):
            list_of_new_names = list_of_file_names

        for i in range(len(list_of_file_names)):
            try:
                file_name = list_of_file_names[i]
                print("Uploading file {}".format(file_name))
                bucket.upload_file(os.path.join(directory_path, file_name), list_of_new_names[i])
                print("File {} uploaded.".format(file_name))
            except:
                raise


    def download_file_from_bucket(self, bucket, object_from_bucket, results_folder_path):
        try:
            new_file_name = object_from_bucket.key.replace(self.transcribe_job_prefix, '')
            print("Downloading file {} with new name {}...".format(object_from_bucket.key, new_file_name))
            bucket.download_file(object_from_bucket.key, results_folder_path + new_file_name)
        except botocore.exceptions.ClientError as e:
            if e.response['Error']['Code'] == "404":
                print("The object does not exist.")
            else:
                raise
        print("Finished downloading file {}".format(new_file_name))


    def download_all_files_from_bucket(self, bucket, results_folder_path):
        for obj in bucket.objects.all():
            self.download_file_from_bucket(bucket, obj, results_folder_path)
