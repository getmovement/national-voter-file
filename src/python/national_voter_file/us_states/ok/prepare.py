from src.main.python.transformers.ok_transformer import OKTransformer
from src.main.python.transformers import DATA_DIR
import os


if __name__ == '__main__':
    input_fields = [
        'Precinct',
        'LastName',
        'FirstName',
        'MiddleName',
        'Suffix',
        'VoterID',
        'PolitalAff',
        'Status',
        'StreetNum',
        'StreetDir',
        'StreetName',
        'StreetType',
        'BldgNum',
        'City',
        'Zip',
        'DateOfBirth',
        'OriginalRegistration',
        'MailStreet1',
        'MailStreet2',
        'MailCity',
        'MailState',
        'MailZip',
        'Muni',
        'MuniSub',
        'School',
        'SchoolSub',
        'TechCenter',
        'TechCenterSub',
        'CountyComm',
        'VoterHist1',
        'HistMethod1',
        'VoterHist2',
        'HistMethod2',
        'VoterHist3',
        'HistMethod3',
        'VoterHist4',
        'HistMethod4',
        'VoterHist5',
        'HistMethod5',
        'VoterHist6',
        'HistMethod6',
        'VoterHist7',
        'HistMethod7',
        'VoterHist8',
        'HistMethod8',
        'VoterHist9',
        'HistMethod9',
        'VoterHist10',
        'HistMethod10'
    ]

    # Fieldnames listed, but can be omitted because they're the column names
    ok_transformer = OKTransformer(date_format="%m/%d/%Y", sep=',')
    ok_transformer(
        os.path.join(DATA_DIR, 'Oklahoma', 'Oklahoma_Sample.csv'),
        os.path.join(DATA_DIR, 'Oklahoma', 'Oklahoma_Sample_OUT.csv'),
    )
