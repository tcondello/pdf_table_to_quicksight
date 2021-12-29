import boto3
import os
from botocore.exceptions import ClientError


class DocumentProcessor:

    def __init__(self, role, bucket, document, region):
        self.roleArn = role
        self.bucket = bucket
        self.document = document
        self.region_name = region
        self.textract = boto3.client('textract', region_name=self.region_name)
        self.s3 = boto3.client('s3')
        self.textract_JobId = '5fb9ba7f2ba17d1c36af8a7ffd6e6b42bd8a30a655280e975131c94b3c1c80d3'        

    
    def upload_file(self):
      object_name = os.path.basename(self.document)
      with open(self.document, 'rb') as file:        
        try:
          response = self.s3.upload_file(file, self.bucket, object_name)
        except ClientError as e:
          print(f'Error: {e}')
          return False
        return True


    def ProcessDocument(self):
        response = self.textract.start_document_analysis(
          DocumentLocation={'S3Object': {'Bucket': self.bucket, 'Name': self.document}},
          FeatureTypes=["TABLES"]
        )        
        self.textract_JobId = response.get('JobId')
                
        print('Start Job Id: ' + self.textract_JobId)    

def main():
    roleArn = 'arn:aws:iam::733452200191:user/eboyIAM'
    bucket = 'eboygan'
    document = 'PDFtoExcel.pdf'
    region_name = 'us-east-1'
    
    analyzer = DocumentProcessor(roleArn, bucket, document, region_name)
    # analyzer.ProcessDocument()
    analyzer.GetDocument()
    
    

if __name__ == "__main__":
    main()


