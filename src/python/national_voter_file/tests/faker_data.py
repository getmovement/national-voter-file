from src.main.python.transformers import base_transformer, wa_transformer, \
    co_transformer, ok_transformer, oh_transformer, fl_transformer, \
    ny_transformer, pa, mi
from faker import Faker
import random
from random import randint
import csv
import os
import sys


TEST_DATA_DIR = os.path.join(os.path.dirname(__file__), 'test_data')
NUM_ROWS = 100

fake = Faker()

# Helpers for making items empty easier
def _empty(item):
    return random.choice([item, ' '])

def _blank(item):
    return random.choice([item, ''])

COLORADO_FIELDS = [
    'VOTER_ID',
    'COUNTY_CODE',
    'COUNTY',
    'LAST_NAME',
    'FIRST_NAME',
    'MIDDLE_NAME',
    'NAME_SUFFIX',
    'VOTER_NAME',
    'STATUS_CODE', # A = active, I = inactive
    'PRECINCT_NAME',
    'ADDRESS_LIBRARY_ID',
    'HOUSE_NUM',
    'HOUSE_SUFFIX',
    'PRE_DIR',
    'STREET_NAME',
    'STREET_TYPE',
    'POST_DIR',
    'UNIT_TYPE',
    'UNIT_NUM',
    'ADDRESS_NON_STD',
    'RESIDENTIAL_ADDRESS',
    'RESIDENTIAL_CITY',
    'RESIDENTIAL_STATE',
    'RESIDENTIAL_ZIP_CODE',
    'RESIDENTIAL_ZIP_PLUS',
    'EFFECTIVE_DATE',
    'REGISTRATION_DATE',
    'STATUS', # Active, Inacti
    'STATUS_REASON', # Undeliverable Ballot, Returned Mail, NCOA, 
    'BIRTH_YEAR', # YYYY
    'GENDER',
    'PRECINCT',
    'SPLIT',
    'VOTER_STATUS_ID',
    'PARTY',
    'PARTY_AFFILIATION_DATE',
    'PHONE_NUM',
    'MAIL_ADDR1',
    'MAIL_ADDR2',
    'MAIL_ADDR3',
    'MAILING_CITY',
    'MAILING_STATE',
    'MAILING_ZIP_CODE',
    'MAILING_ZIP_PLUS',
    'MAILING_COUNTRY',
    'SPL_ID',
    'PERMANENT_MAIL_IN_VOTER', # No
    'CONGRESSIONAL', # Congressional 6
    'STATE_SENATE', # State Senate 2
    'STATE_HOUSE', # State House 45
    'ID_REQUIRED' # Y or N
]

OHIO_SCHEMA = {
    'SOS_VOTERID': lambda: 'OH{}'.format(str(randint(1000, 999999)).zfill(10)),
    'COUNTY_NUMBER': lambda: str(randint(1, 88)),
    'COUNTY_ID': lambda: str(randint(1000, 999999999)),
    'LAST_NAME': lambda: fake.last_name().upper(),
    'FIRST_NAME': lambda: fake.first_name().upper(),
    'MIDDLE_NAME': lambda: _empty(fake.first_name().upper()),
    'SUFFIX': lambda: _empty(fake.suffix().upper()),
    'DATE_OF_BIRTH': lambda: fake.date(pattern='%m/%d/%Y'),
    'REGISTRATION_DATE': lambda: fake.date(pattern='%m/%d/%Y'),
    'VOTER_STATUS': lambda: random.choice(['ACTIVE', 'INACTIVE', 'CONFIRMATION']),
    'PARTY_AFFILIATION': lambda: random.choice(list(oh_transformer.OHTransformer.ohio_party_map.keys())),
    'RESIDENTIAL_ADDRESS1': lambda: fake.street_address().upper(),
    'RESIDENTIAL_SECONDARY_ADDR': lambda: _empty(fake.secondary_address().upper()),
    'RESIDENTIAL_CITY': lambda: fake.city().upper(),
    'RESIDENTIAL_STATE': lambda: 'OH',
    'RESIDENTIAL_ZIP': lambda: fake.zipcode(),
    'RESIDENTIAL_ZIP_PLUS4': lambda: _empty(fake.numerify(text='####')),
    'RESIDENTIAL_COUNTRY': lambda: 'USA',
    'RESIDENTIAL_POSTCODE': lambda: fake.zipcode(),
    'MAILING_ADDRESS1': lambda: _empty(fake.street_address().upper()),
    'MAILING_SECONDARY_ADDRESS': lambda: _empty(fake.street_address().upper()),
    'MAILING_CITY': lambda: _empty(fake.city().upper()),
    'MAILING_STATE': lambda: _empty(fake.state_abbr()),
    'MAILING_ZIP': lambda: _empty(fake.zipcode()),
    'MAILING_ZIP_PLUS4': lambda: _empty(fake.numerify(text='####')),
    'MAILING_COUNTRY': lambda: _empty(fake.state_abbr()),
    'MAILING_POSTAL_CODE': lambda: _empty(fake.zipcode()),
    'CAREER_CENTER': lambda: fake.city().upper(),
    'CITY': lambda: fake.city().upper(),
    'CITY_SCHOOL_DISTRICT': lambda: fake.city().upper(),
    'COUNTY_COURT_DISTRICT': lambda: str(randint(1, 99)).zfill(2),
    'CONGRESSIONAL_DISTRICT': lambda: str(randint(1, 99)).zfill(2),
    'COURT_OF_APPEALS': lambda: str(randint(1, 99)).zfill(2),
    'EDU_SERVICE_CENTER_DISTRICT': lambda: str(randint(1, 99)).zfill(2),
    'EXEMPTED_VILL_SCHOOL_DISTRICT': lambda: _empty(str(randint(1, 99)).zfill(2)),
    'LIBRARY': lambda: _empty(str(randint(1, 99)).zfill(2)),
    'LOCAL_SCHOOL_DISTRICT': lambda: _empty(str(randint(1, 99)).zfill(2)),
    'MUNICIPAL_COURT_DISTRICT': lambda: _empty(str(randint(1, 99)).zfill(2)),
    'PRECINCT_NAME': lambda: fake.city().upper(),
    'PRECINCT_CODE': lambda: '{}-{}'.format(randint(10,80), fake.lexify(text='???').upper()),
    'STATE_BOARD_OF_EDUCATION': lambda: str(randint(1, 100)),
    'STATE_REPRESENTATIVE_DISTRICT': lambda: str(randint(1, 100)),
    'STATE_SENATE_DISTRICT': lambda: str(randint(1, 100)),
    'TOWNSHIP': lambda: _empty(fake.city().upper()),
    'VILLAGE': lambda: _empty(fake.city().upper()),
    'WARD': lambda: _empty(fake.city().upper())
}


# Defining fields because order matters for csvs without header rows
FLORIDA_FIELDS = [
    'County Code',
    'Voter ID',
    'Name Last',
    'Name Suffix',
    'Name First',
    'Name Middle',
    'Requested public records exemption',
    'Residence Address Line 1',
    'Residence Address Line 2',
    'Residence City (USPS)',
    'Residence State',
    'Residence Zipcode',
    'Mailing Address Line 1',
    'Mailing Address Line 2',
    'Mailing Address Line 3',
    'Mailing City',
    'Mailing State',
    'Mailing Zipcode',
    'Mailing Country',
    'Gender',
    'Race',
    'Birth Date',
    'Registration Date',
    'Party Affiliation',
    'Precinct',
    'Precinct Group',
    'Precinct Split',
    'Precinct Suffix',
    'Voter Status',
    'Congressional District',
    'House District',
    'Senate District',
    'County Commission District',
    'School Board District',
    'Daytime Area Code',
    'Daytime Phone Number',
    'Daytime Phone Extension',
    'Email address'
]

FLORIDA_SCHEMA = {
    'County Code': lambda: random.choice(['OKE', 'ALA', 'ABC']),
    'Voter ID': lambda: fake.numerify(text='##########'),
    'Name Last': lambda: fake.last_name().upper(),
    'Name Suffix': lambda: _empty(fake.suffix().upper()),
    'Name First': lambda: fake.first_name().upper(),
    'Name Middle': lambda: _empty(fake.first_name().upper()),
    'Requested public records exemption': lambda: random.choice(['Y', 'N']),
    'Residence Address Line 1': lambda: fake.street_address().upper(),
    'Residence Address Line 2': lambda: _empty(fake.secondary_address().upper()),
    'Residence City (USPS)': lambda: fake.city().upper(),
    'Residence State': lambda: ' ',
    'Residence Zipcode': lambda: fake.zipcode(),
    'Mailing Address Line 1': lambda: _empty(fake.street_address().upper()),
    'Mailing Address Line 2': lambda: _empty(fake.secondary_address().upper()),
    'Mailing Address Line 3': lambda: _empty(fake.secondary_address().upper()),
    'Mailing City': lambda: _empty(fake.city().upper()),
    'Mailing State': lambda: _empty(fake.state_abbr()),
    'Mailing Zipcode': lambda: _empty(fake.zipcode()),
    'Mailing Country': lambda: _empty(fake.state_abbr()),
    'Gender': lambda: _empty(random.choice(['F', 'M', 'U'])),
    'Race': lambda: random.choice(list(national_voter_file.us_states.fl.StateTransformer.florida_race_map.keys())),
    'Birth Date': lambda: _empty(fake.date(pattern='%m/%d/%Y')),
    'Registration Date': lambda: fake.date(pattern='%m/%d/%Y'),
    'Party Affiliation': lambda: random.choice(list(fl_transformer.FLTransformer.florida_party_map.keys())),
    'Precinct': lambda: str(randint(1, 100)),
    'Precinct Group': lambda: str(randint(1, 100)),
    'Precinct Split': lambda: '{0:.1f}'.format(random.uniform(1, 12)),
    'Precinct Suffix': lambda: ' ',
    'Voter Status': lambda: random.choice(['ACT', 'INA', 'PRE']),
    'Congressional District': lambda: str(randint(1, 27)),
    'House District': lambda: str(randint(1, 120)),
    'Senate District': lambda: str(randint(1, 120)),
    'County Commission District': lambda: str(randint(1, 100)),
    'School Board District': lambda: str(randint(1, 100)),
    'Daytime Area Code': lambda: _empty(fake.numerify(text='###')),
    'Daytime Phone Number': lambda: _empty(fake.numerify(text='#######')),
    'Daytime Phone Extension': lambda: _empty(str(randint(10, 9999))),
    'Email address': lambda: _empty(fake.email().upper())
}


NEW_YORK_FIELDS = [
    'LASTNAME',
    'FIRSTNAME',
    'MIDDLENAME',
    'NAMESUFFIX',
    'RADDNUMBER',
    'RHALFCODE',
    'RAPARTMENT',
    'RPREDIRECTION',
    'RSTREETNAME',
    'RPOSTDIRECTION',
    'RCITY',
    'RZIP5',
    'RZIP4',
    'MAILADD1',
    'MAILADD2',
    'MAILADD3',
    'MAILADD4',
    'DOB',
    'GENDER',
    'ENROLLMENT',
    'OTHERPARTY',
    'COUNTYCODE',
    'ED',
    'LD',
    'TOWNCITY',
    'WARD',
    'CD',
    'SD',
    'AD',
    'LASTVOTEDDATE',
    'PREVYEARVOTED',
    'PREVCOUNTY',
    'PREVADDRESS',
    'PREVNAME',
    'COUNTYVRNUMBER',
    'REGDATE',
    'VRSOURCE',
    'IDREQUIRED',
    'IDMET',
    'STATUS',
    'REASONCODE',
    'INACT_DATE',
    'PURGE_DATE',
    'SBOEID',
    'VoterHistory'
]

NEW_YORK_SCHEMA = {
    'LASTNAME': lambda: fake.last_name(),
    'FIRSTNAME': lambda: fake.first_name(),
    'MIDDLENAME': lambda: _empty(fake.first_name()),
    'NAMESUFFIX': lambda: _empty(fake.suffix()),
    'RADDNUMBER': lambda: fake.building_number(),
    'RHALFCODE': lambda: _empty(random.choice(['1/2', '1/3'])),
    'RAPARTMENT': lambda: _empty(random.choice([fake.numerify(text='###'), 'GRD'])),
    'RPREDIRECTION': lambda: _empty(random.choice(['N', 'S', 'E', 'W'])),
    'RSTREETNAME': lambda: fake.street_name(),
    'RPOSTDIRECTION': lambda: _empty(random.choice(['N', 'S', 'E', 'W'])),
    'RCITY': lambda: fake.city(),
    'RZIP5': lambda: fake.zipcode(),
    'RZIP4': lambda: _empty(fake.numerify(text='####')),
    'MAILADD1': lambda: _empty(fake.street_address()),
    'MAILADD2': lambda: _empty(fake.secondary_address()),
    'MAILADD3': lambda: _empty(fake.street_address()),
    'MAILADD4': lambda: _empty(fake.street_address()),
    'DOB': lambda: fake.date(pattern='%Y%m%d'),
    'GENDER': lambda: random.choice(['M', 'F']),
    'ENROLLMENT': lambda: random.choice(list(ny_transformer.NYTransformer.ny_party_map.keys())),
    'OTHERPARTY': lambda: _empty(random.choice(list(ny_transformer.NYTransformer.ny_other_party_map.keys()))),
    'COUNTYCODE': lambda: fake.numerify(text='##'),
    'ED': lambda: str(randint(1, 100)),
    'LD': lambda: str(randint(1, 100)),
    'TOWNCITY': lambda: fake.city(),
    'WARD': lambda: str(randint(1, 100)),
    'CD': lambda: str(randint(1, 27)),
    'SD': lambda: str(randint(1, 100)),
    'AD': lambda: str(randint(1, 100)),
    'LASTVOTEDDATE': lambda: _empty(fake.date(pattern='%Y%m%d')),
    'PREVYEARVOTED': lambda: _empty(fake.year()),
    'PREVCOUNTY': lambda: _empty(fake.city()),
    'PREVADDRESS': lambda: _empty(fake.street_address()),
    'PREVNAME': lambda: _empty(fake.name()),
    'COUNTYVRNUMBER': lambda: fake.numerify(text='#######'),
    'REGDATE': lambda: fake.date(pattern='%Y%m%d'),
    'VRSOURCE': lambda: random.choice(['AGCY', 'CBOE', 'DMV', 'LOCALREG', 'MAIL', 'SCHOOL']),
    'IDREQUIRED': lambda: random.choice(['Y', 'N']),
    'IDMET': lambda: random.choice(['Y', 'N']),
    'STATUS': lambda: random.choice(['A', 'AM', 'AF', 'AP', 'AU', 'I', 'P', '17']),
    'REASONCODE': lambda: random.choice(['ADJ-INCOMP', 'DEATH', 'DUPLICATE', 'FELON', 'MAIL-CHECK', 'MOVED', 'NCOA', 'NVRA', 'RETURN-MAIL', 'VOTER-REQ']),
    'INACT_DATE': lambda: _empty(fake.date(pattern='%Y%m%d')),
    'PURGE_DATE': lambda: _empty(fake.date(pattern='%Y%m%d')),
    'SBOEID': lambda: 'NY{}'.format(fake.numerify('#########').zfill(18)),
    'VoterHistory': lambda: _empty(random.choice(['2004;General Election', '2012']))
}


NORTH_CAROLINA_SCHEMA = {
    'county_id': lambda: str(randint(1, 90)),
    'county_desc': lambda: fake.city().upper(),
    'voter_reg_num': lambda: str(randint(10000, 999999999)),
    'status_cd': lambda: random.choice(['A', 'I']),
    'voter_status_desc': lambda: random.choice(['ACTIVE', 'INACTIVE']),
    'reason_cd': lambda: random.choice(['A1', 'A2', 'AL', 'AN', 'AP', 'AV', 'IN', 'IU']),
    'voter_status_reason_desc': lambda: random.choice(['CONFIRMATION NOT RETURNED', 'CONFIRMATION PENDING', 'CONFIRMATION RETURNED UNDELIVERABLE', 'LEGACY DATA', 'UNVERIFIED', 'UNVERIFIED NEW', 'VERIFICATION PENDING', 'VERIFIED']),
    'absent_ind': lambda: ' ',
    'name_prefx_cd': lambda: ' ',
    'last_name': lambda: fake.last_name().upper(),
    'first_name': lambda: fake.first_name().upper(),
    'middle_name': lambda: _empty(fake.first_name().upper()),
    'name_suffix_lbl': lambda: _empty(fake.suffix().upper()),
    'res_street_address': lambda: fake.street_address().upper(),
    'res_city_desc': lambda: fake.city().upper(),
    'state_cd': lambda: 'NC',
    'zip_code': lambda: fake.zipcode(),
    'mail_addr1': lambda: _empty(fake.street_address().upper()),
    'mail_addr2': lambda: _empty(fake.secondary_address().upper()),
    'mail_addr3': lambda: _empty(fake.street_address().upper()),
    'mail_addr4': lambda: _empty(fake.street_address().upper()),
    'mail_city': lambda: _empty(fake.city().upper()),
    'mail_state': lambda: _empty(fake.state_abbr()),
    'mail_zipcode': lambda: _empty(fake.zipcode()),
    'full_phone_number': lambda: _empty(fake.phone_number().replace('-', '')),
    'race_code': lambda: random.choice(['B', 'I', 'O', 'W', 'U', 'A', 'M']),
    'ethnic_code': lambda: random.choice(['HL', 'NL', 'UN']),
    'party_cd': lambda: random.choice(['DEM', 'REP', 'LIB', 'UNA']),
    'gender_code': lambda: random.choice(['F', 'M', 'U']),
    'birth_age': lambda: str(randint(18, 100)),
    'birth_state': lambda: fake.state_abbr(),
    'drivers_lic': lambda: random.choice(['Y', 'N']),
    'registr_dt': lambda: fake.date(pattern='%m/%d/%Y'),
    'precinct_abbrv': lambda: random.choice(['CAR', '08N', '1/7']),
    'precinct_desc': lambda: fake.city().upper(),
    'municipality_abbrv': lambda: _empty(fake.state_abbr()),
    'municipality_desc': lambda: _empty(fake.city().upper()),
    'ward_abbrv': lambda: _empty(random.choice(['7', '5', 'R-B'])),
    'ward_desc': lambda: _empty(random.choice(['RALEIGH MUNICIPAL DISTRICT B', 'SOUTHWEST WARD'])),
    'cong_dist_abbrv': lambda: _empty(str(randint(1, 13))),
    'super_court_abbrv': lambda: _empty(str(randint(1, 30)).zfill(2) + random.choice(['A', 'B'])),
    'judic_dis_abbrv': lambda: _empty(random.choice([str(randint(1, 30)), '20A'])),
    'nc_senate_abbrv': lambda: _empty(str(randint(1, 100))),
    'nc_house_abbrv': lambda: _empty(str(randint(1, 100))),
    'county_commiss_abbrv': lambda: _empty(random.choice(['CM03', '6', '4'])),
    'county_commiss_desc': lambda: _empty(random.choice(['COMMISSION #4', 'COMMISSION #7'])),
    'township_abbrv': lambda: _empty(random.choice(['1', '4' ,'5', 'G', 'GAST'])),
    'township_desc': lambda: _empty(random.choice(['DALLAS', 'IRONTON'])),
    'school_dist_abbrv': lambda: _empty(random.choice(['CH/CHAR', '4', 'S06', 'ROBE'])),
    'school_dist_desc': lambda: _empty(random.choice(['SCHOOL #3', 'CHAPEL HILL'])),
    'fire_dist_abbrv': lambda: _empty(random.choice(['NEFD', 'PC11', '15'])),
    'fire_dist_desc': lambda: _empty(random.choice(['NORTHEAST FIRE DISTRICT', 'PUMPKIN CENTER', 'NEWTON'])),
    'water_dist_abbrv': lambda: _empty(random.choice(['1', '8', 'CL/U', 'CLWA'])),
    'water_dist_desc': lambda: _empty(random.choice(['CENTRAL', 'CITY COUNCIL DIST 1', 'PINETOPS'])),
    'sewer_dist_abbrv': lambda: _empty(random.choice(['1', '2', 'EL'])),
    'sewer_dist_desc': lambda: _empty(random.choice(['DISTRICT 1', 'DISTRICT 2', 'EAST LINCOLN'])),
    'sanit_dist_abbrv': lambda: _empty(random.choice(['B P', 'EOSD', '26'])),
    'sanit_dist_desc': lambda: _empty(random.choice(['EASTERN WAYNE', 'EAST CRAVEN'])),
    'rescue_dist_abbrv': lambda: _empty(random.choice(['WHRD', 'NARD', '50'])),
    'rescue_dist_desc': lambda: _empty(random.choice(['GSO CITY COUNCIL 1', 'HOSPITAL DIST 50'])),
    'munic_dist_abbrv': lambda: _empty(fake.state_abbr()),
    'munic_dist_desc': lambda: _empty(fake.city().upper()),
    'dist_1_abbrv': lambda: _empty(random.choice(['20', '30', '29A'])),
    'dist_1_desc': lambda: _empty(random.choice(['26TH PROS DIST', '05 PROSECUTORIAL'])),
    'dist_2_abbrv': lambda: ' ',
    'dist_2_desc': lambda: ' ',
    'Confidential_ind': lambda: 'N',
    'age': lambda: str(randint(18, 100)),
    'ncid': lambda: '{}{}'.format(fake.lexify(text='??').upper(), fake.numerify(text='######')),
    'vtd_abbrv': lambda: random.choice(['CAR', '08N', '1/7']),
    'vtd_desc': lambda: random.choice(['CAR', '08N', '1/7'])
}

PENNSYLVANIA_SCHEMA = {
    'STATE_VOTER_REF': lambda: str(randint(1, 1000000)),
    'TITLE': lambda: fake.prefix(),
    'LAST_NAME': lambda: fake.last_name().upper(),
    'FIRST_NAME': lambda: _blank(fake.first_name().upper()),
    'MIDDLE_NAME': lambda: _blank(fake.first_name().upper()),
    'NAME_SUFFIX': lambda: _empty(fake.suffix()),
    'GENDER': lambda: random.choice(['M', 'F', 'U', '']),
    'BIRTHDATE': lambda: _blank(fake.date(pattern='%m/%d/%Y')),
    'REGISTRATION_DATE': lambda: _blank(fake.date(pattern='%m/%d/%Y')),
    'REGISTRATION_STATUS': lambda: random.choice(['I', 'A']),
    '_STATUS_CHANGE_DATE': lambda: _blank(fake.date(pattern='%m/%d/%Y')),
    '_PARTY_CODE': lambda: random.choice(['D', 'R', 'IND', "", "GR", "RANDOMOTHER"]),
    'ADDRESS_NUMBER': lambda: _blank(fake.building_number()),
    'ADDRESS_NUMBER_SUFFIX': lambda: _blank(fake.building_number()),
    'STREET_NAME': lambda: fake.street_name().upper(),
    '_ADDRESS_APARTMENT_NUM': lambda: _blank(fake.building_number()),
    '_ADDRESS_LINE2': lambda: _blank(fake.secondary_address().upper()),
    '_REGISTRATION_CITY': lambda: fake.city().upper(),
    'STATE_NAME': lambda: _blank(fake.state_abbr().upper()),
    'ZIP_CODE': lambda: _blank(fake.zipcode()),
    'MAIL_ADDRESS_LINE1': lambda: _blank(fake.street_address().upper()),
    'MAIL_ADDRESS_LINE2': lambda: _blank(fake.secondary_address().upper()),
    'MAIL_CITY': lambda: fake.city().upper(),
    'MAIL_STATE': lambda: _blank(fake.state_abbr().upper()),
    'MAIL_ZIP_CODE': lambda: _blank(fake.zipcode()),
    '_LASTVOTE': lambda: _blank(fake.date(pattern='%m/%d/%Y')),
    '_PRECINCT_CODE': lambda: str(randint(1, 1000000)),
    'PRECINCT_SPLIT': lambda: '%d-%d' % (randint(1, 1000000), randint(1,50)),
    '_LAST_CHANGE_DATE': lambda: _blank(fake.date(pattern='%m/%d/%Y')),
    '_LEGACY_SYSTEM_ID': lambda: str(randint(800000, 10000000)),
    'PHONE': lambda: _blank(fake.phone_number().replace('-', '')),
    'COUNTYCODE': lambda: fake.city().upper(),
    'MAIL_COUNTRY': lambda: _blank(fake.state_abbr()),
}

MICHIGAN_SCHEMA = {
    'LAST_NAME': lambda: fake.last_name().upper(),
    'FIRST_NAME': lambda: fake.first_name().upper(),
    'MIDDLE_NAME': lambda: _blank(fake.first_name().upper()),
    'NAME_SUFFIX': lambda: _empty(fake.suffix()),
    'BIRTH_YEAR': lambda: fake.year(),
    'GENDER': lambda: _blank(random.choice(['F', 'M', '1', '2'])),
    'DATE_OF_REGISTRATION': lambda: fake.date(pattern='%m%d%Y'),
    'HOUSE_NUM_CHARACTER': lambda: _empty(random.choice(['N', 'S', 'E', 'W'])),
    'RESIDENCE_STREET_NUMBER': lambda: _blank(fake.building_number()),
    'HOUSE_SUFFIX': lambda: _empty(random.choice(['1/2', '1/3'])),
    'PRE_DIRECTION': lambda: _empty(random.choice(['N', 'S', 'E', 'W'])),
    'STREET_NAME': lambda: fake.street_name().upper(),
    'STREET_TYPE': lambda: fake.street_suffix().upper(),
    'SUFFIX_DIRECTION': lambda: _empty(random.choice(['N', 'S', 'E', 'W'])),
    'RESIDENCE_EXTENSION': lambda: _empty(random.choice(['APT', 'LOT'])),
    'CITY': lambda: fake.city().upper(),
    'STATE': lambda: fake.state_abbr(),
    'ZIP': lambda: fake.zipcode(),
    'MAIL_ADDR_1': lambda: _blank(fake.street_address().upper()),
    'MAIL_ADDR_2': lambda: _blank(fake.secondary_address().upper()),
    'MAIL_ADDR_3': lambda: fake.city().upper(),
    'MAIL_ADDR_4': lambda: _blank(fake.state_abbr().upper()),
    'MAIL_ADDR_5': lambda: _blank(fake.zipcode()),
    'STATE_VOTER_REF': lambda: fake.numerify(text=('#'*13)),
    'COUNTYCODE': lambda: fake.numerify(text='##'),
    'JURISDICTION': lambda: fake.numerify(text='####'),
    'WARD_PRECINCT': lambda: fake.numerify(text='####'),
    'SCHOOL_CODE': lambda: fake.numerify(text='##'),
    'LOWER_HOUSE_DIST': lambda: fake.numerify(text='##'),
    'UPPER_HOUSE_DIST': lambda: fake.numerify(text='##'),
    'CONGRESSIONAL_DIST': lambda: str(randint(1, 16)),
    'COUNTY_BOARD_DIST': lambda: _empty(str(randint(1, 50))),
    'VILLAGE_CODE': lambda: _empty(fake.numerify(text='####')),
    'VILLAGE_PRECINCT': lambda: _empty(fake.numerify(text='###')),
    'SCHOOL_PRECINCT': lambda: _empty(fake.numerify(text='###')),
    'PERMANENT_ABSENTEE_IND': lambda: random.choice(['Y', 'N']),
    'REGISTRATION_STATUS': lambda: random.choice(['A', 'V', 'C', 'R', 'CH']),
    'UOCAVA_STATUS': lambda: random.choice(['M', 'C', 'N', 'O'])
}

WASHINGTON_SCHEMA = {
'StateVoterID': lambda:'WA{}'.format(str(randint(1000, 999999)).zfill(10)),
'CountyVoterID': lambda:  str(randint(1, 88)),
'Title': lambda: ' ',
'FName': lambda:  fake.first_name().upper(),
'MName': lambda:  fake.first_name().upper(),
'LName': lambda:  fake.last_name().upper(),
'NameSuffix': lambda:  _empty(fake.suffix().upper()),
'Birthdate': lambda:  _empty(fake.date(pattern='%m/%d/%Y')),
'Gender': lambda:  random.choice(['F', 'M', 'U']),
'RegStNum': lambda:  _empty(fake.building_number()),
'RegStFrac': lambda: _empty(str(randint(1, 13))) ,
'RegStName': lambda:  fake.street_name().upper(),
'RegStType': lambda:  fake.street_suffix(),
'RegUnitType': lambda:  _empty(random.choice(['APT', 'UNIT', 'FLOOR', "", ])),
'RegStPreDirection': lambda:  _empty(random.choice(['S', 'E', 'W', "", ])),
'RegStPostDirection': lambda:  _empty(random.choice(['S', 'E', 'W', "", ])),
'RegUnitNum': lambda:  _blank(fake.building_number()),
'RegCity': lambda:  fake.city().upper(),
'RegState': lambda:  _blank(fake.state_abbr().upper()),
'RegZipCode': lambda:  _blank(fake.zipcode()),
'CountyCode': lambda:  random.choice(['SN','CR','AS','PI']),
'PrecinctCode': lambda: str(randint(1, 999999)) ,
'PrecinctPart': lambda:  str(randint(1, 999999)) ,
'LegislativeDistrict': lambda:  _empty(str(randint(1, 100))),
'CongressionalDistrict': lambda:  _empty(str(randint(1, 100))),
'Mail1': lambda:  _blank(fake.street_address().upper()),
'Mail2': lambda:  _blank(fake.secondary_address().upper()),
'Mail3': lambda:  _blank(fake.secondary_address().upper()),
'Mail4': lambda:  _blank(fake.secondary_address().upper()),
'MailCity': lambda:  fake.city().upper(),
'MailZip': lambda:  _blank(fake.zipcode()),
'MailState': lambda:  _blank(fake.state_abbr().upper()),
'MailCountry': lambda:  ' ',
'Registrationdate': lambda:  _empty(fake.date(pattern='%m/%d/%Y')),
'AbsenteeType': lambda:  random.choice(['N', 'P', ' ', 'V']),
'LastVoted': lambda:  _empty(fake.date(pattern='%m/%d/%Y')),
'StatusCode': lambda:  random.choice(['A', 'I']),
'Dflag': lambda:  ' '
}


def fakePAdistrict():
    prefix = random.choice(['LG', 'SN', 'MN', 'CO', 'CN', 'SAN', randint(1,1000)])
    return '%s%s%d' % (prefix, random.choice(['', '-']), randint(1,100000))

for d in range(40):
    PENNSYLVANIA_SCHEMA['_DISTRICT%d' % (d+1)] = fakePAdistrict

for d in range(1,40):
    PENNSYLVANIA_SCHEMA['_VOTEHISTORY_%d' % (2*d)] = lambda: random.choice(['','AP','AB','P'])
    PENNSYLVANIA_SCHEMA['_VOTEHISTORY_%d' % (2*d+1)] = PENNSYLVANIA_SCHEMA['_PARTY_CODE']


def make_state_data(state_name, state_schema,
                    sep=',', has_header=True, input_fields=None):
    state_rows = []
    while len(state_rows) < NUM_ROWS:
        r  = {}
        for k in state_schema.keys():
            r[k] = state_schema[k]()
        state_rows.append(r)

    if input_fields is None:
        input_fields = state_rows[0].keys()

    with open(os.path.join(TEST_DATA_DIR, state_name + '.csv'), 'w') as f:
        w = csv.DictWriter(f, fieldnames=input_fields, delimiter=sep)
        if has_header:
            w.writeheader()
        w.writerows(state_rows)


if __name__ == '__main__':
    states = {'ohio': ([OHIO_SCHEMA],
                       {}),
              'florida': ([FLORIDA_SCHEMA],
                          {'sep': '\t',
                           'has_header': False,
                           'input_fields': FLORIDA_FIELDS}),
              'new_york': ([NEW_YORK_SCHEMA],
                           {'has_header': False,
                            'input_fields': NEW_YORK_FIELDS}),
              'north_carolina': ([NORTH_CAROLINA_SCHEMA],
                                 {'sep':'\t'}),
              'pennsylvania': ([PENNSYLVANIA_SCHEMA],
                               {'sep':'\t',
                                'has_header': False,
                                'input_fields': pa.StatePreparer.input_fields}),
              'michigan': ([MICHIGAN_SCHEMA],
                           {'has_header': False,
                            'input_fields': mi.StatePreparer.input_fields}),
              'washington': ([WASHINGTON_SCHEMA],
                                {'sep':'\t'}),
    }
    keys = states.keys()
    if len(sys.argv) > 1:
        keys = sys.argv[1:]
    for state in keys:
        args, kwargs = states[state]
        make_state_data(state, *args, **kwargs)
