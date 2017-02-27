import csv
import os
import re
import sys

from national_voter_file.transformers.base import (DATA_DIR,
                                                   BasePreparer,
                                                   BaseTransformer)
import usaddress

__all__ = ['default_file', 'StatePreparer', 'StateTransformer']

default_file = '201605_VRDB_ExtractSAMPLE.txt'

class StatePreparer(BasePreparer):
    state_path = 'wa'
    state_name = 'Washington'
    sep = "\t"

    def __init__(self, input_path, *args):
        super(StatePreparer, self).__init__(input_path, *args)

        if not self.transformer:
            self.transformer = StateTransformer()

    def process(self):
        reader = self.dict_iterator(self.open(self.input_path))
        for row in reader:
            yield row

class StateTransformer(BaseTransformer):
    date_format = "%m/%d/%Y"
    input_fields = None

    #### Contact methods #######################################################

    def extract_name(self, input_dict):
        return {
            'TITLE': input_dict['Title'],
            'FIRST_NAME': self.flag_empty_field(input_dict['FName']),
            'MIDDLE_NAME': input_dict['MName'],
            'LAST_NAME': self.flag_empty_field(input_dict['LName']),
            'NAME_SUFFIX': input_dict['NameSuffix'],
        }

    def extract_email(self, input_dict):
        return {'EMAIL': None}

    def extract_phone_number(self, input_dict):
        return {'PHONE': None}

    def extract_do_not_call_status(self, input_dict):
        return {'DO_NOT_CALL_STATUS': None}

    #### Demographics methods ##################################################

    def extract_gender(self, input_dict):
        gender = input_dict['Gender']
        gender = gender if gender == 'M' or gender == 'F' else 'U'
        return {'GENDER': gender}

    def extract_race(self, input_dict):
        return {'RACE': None}

    def extract_birth_state(self, input_dict):
        return {'BIRTH_STATE': None}

    def extract_birthdate(self, input_dict):
        if input_dict['Birthdate']:
            date = self.convert_date(input_dict['Birthdate'])
        else:
            date = None

        return {
            'BIRTHDATE': date,
            'BIRTHDATE_IS_ESTIMATE': 'N'
        }


    def extract_language_choice(self, input_dict):
        return {'LANGUAGE_CHOICE': None}

    #### Address methods #######################################################

    def extract_registration_address(self, input_dict):
        """

        Washington state data is beautifully parsed into the same fields
        that we require, so an easy mapping.
        Inputs:
            input_dict: dictionary of form {colname: value} from raw data
        Outputs:
            Dictionary with following keys
                'ADDRESS_NUMBER'
                'ADDRESS_NUMBER_PREFIX'
                'ADDRESS_NUMBER_SUFFIX'
                'BUILDING_NAME'
                'CORNER_OF'
                'INTERSECTION_SEPARATOR'
                'LANDMARK_NAME'
                'NOT_ADDRESS'
                'OCCUPANCY_TYPE'
                'OCCUPANCY_IDENTIFIER'
                'PLACE_NAME'
                'STATE_NAME'
                'STREET_NAME'
                'STREET_NAME_PRE_DIRECTIONAL'
                'STREET_NAME_PRE_MODIFIER'
                'STREET_NAME_PRE_TYPE'
                'STREET_NAME_POST_DIRECTIONAL'
                'STREET_NAME_POST_MODIFIER'
                'STREET_NAME_POST_TYPE'
                'SUBADDRESS_IDENTIFIER'
                'SUBADDRESS_TYPE'
                'USPS_BOX_GROUP_ID'
                'USPS_BOX_GROUP_TYPE'
                'USPS_BOX_ID'
                'USPS_BOX_TYPE'
                'ZIP_CODE'
        """
        output_dict = {
            'ADDRESS_NUMBER': input_dict['RegStNum'],
            'ADDRESS_NUMBER_PREFIX': None,
            'ADDRESS_NUMBER_SUFFIX': input_dict['RegStFrac'],
            'BUILDING_NAME': None,
            'CORNER_OF': None,
            'INTERSECTION_SEPARATOR': None,
            'LANDMARK_NAME': None,
            'NOT_ADDRESS': None,
            'OCCUPANCY_TYPE': input_dict['RegUnitType'],
            'OCCUPANCY_IDENTIFIER': input_dict['RegUnitNum'],
            'PLACE_NAME': input_dict['RegCity'],
            'STATE_NAME': input_dict['RegState'],
            'STREET_NAME': input_dict['RegStName'],
            'STREET_NAME_PRE_DIRECTIONAL': input_dict['RegStPreDirection'],
            'STREET_NAME_PRE_MODIFIER': None,
            'STREET_NAME_PRE_TYPE': None,
            'STREET_NAME_POST_DIRECTIONAL': input_dict['RegStPostDirection'],
            'STREET_NAME_POST_MODIFIER': None,
            'STREET_NAME_POST_TYPE': input_dict['RegStType'],
            'SUBADDRESS_IDENTIFIER': None,
            'SUBADDRESS_TYPE': None,
            'USPS_BOX_GROUP_ID': None,
            'USPS_BOX_GROUP_TYPE': None,
            'USPS_BOX_ID': None,
            'USPS_BOX_TYPE': None,
            'ZIP_CODE': input_dict['RegZipCode'],
            'RAW_ADDR1': self.construct_val(input_dict, [
                'RegStNum', 'RegStFrac', 'RegStPreDirection',
                'RegStName', 'RegStType', 'RegStPostDirection'
            ]),
            'RAW_ADDR2': self.construct_val(input_dict, ['RegUnitType', 'RegUnitNum']),
            'RAW_CITY': input_dict['RegCity'],
            'RAW_ZIP': input_dict['RegZipCode'],
            'VALIDATION_STATUS': "2"

        }
        return output_dict

    def extract_county_code(self, input_dict):
        return {'COUNTYCODE': input_dict['CountyCode']}

    def extract_mailing_address(self, input_dict):
        """
        Relies on the usaddress package.

        We provide template code.

        Inputs:
            input_dict: dictionary of form {colname: value} from raw data
        Outputs:
            Dictionary with following keys
                'MAIL_ADDRESS_LINE1'
                'MAIL_ADDRESS_LINE2'
                'MAIL_CITY'
                'MAIL_STATE'
                'MAIL_ZIP_CODE'
                'MAIL_COUNTRY'
        """

        if input_dict['Mail1'].strip() and input_dict['MailCity'].strip():
            return {
                'MAIL_ADDRESS_LINE1': input_dict['Mail1'],
                'MAIL_ADDRESS_LINE2': " ".join([input_dict['Mail2'], input_dict['Mail3'], input_dict['Mail4']]),
                'MAIL_CITY': input_dict['MailCity'],
                'MAIL_STATE': input_dict['MailState'],
                'MAIL_ZIP_CODE': input_dict['MailZip'],
                'MAIL_COUNTRY': input_dict['MailCountry'] if input_dict['MailCountry'] else "USA"
            }
        else:
            return {}

    #### Political methods #####################################################

    def extract_state_voter_ref(self, input_dict):
        return {'STATE_VOTER_REF': input_dict['StateVoterID']}

    def extract_county_voter_ref(self, input_dict):
        return {'COUNTY_VOTER_REF': input_dict['CountyVoterID']}

    def extract_registration_date(self, input_dict):
        if input_dict['Registrationdate']:
            date = self.convert_date(input_dict['Registrationdate'])
        else:
            date = None
        return {'REGISTRATION_DATE': date}

    def extract_registration_status(self, input_dict):
        return {'REGISTRATION_STATUS': input_dict['StatusCode']}

    def extract_absentee_type(self, input_dict):
        return {'ABSENTEE_TYPE': input_dict['AbsenteeType']}

    def extract_party(self, input_dict):
        return {'PARTY': None}

    def extract_congressional_dist(self, input_dict):
        return {'CONGRESSIONAL_DIST': input_dict['CongressionalDistrict']}

    def extract_upper_house_dist(self, input_dict):
        return {'UPPER_HOUSE_DIST': None}

    def extract_lower_house_dist(self, input_dict):
        return {'LOWER_HOUSE_DIST': input_dict['LegislativeDistrict']}

    def extract_precinct(self, input_dict):
        return {'PRECINCT': input_dict['PrecinctCode']}

    def extract_county_board_dist(self, input_dict):
        return {'COUNTY_BOARD_DIST': None}

    def extract_school_board_dist(self, input_dict):
        return {'SCHOOL_BOARD_DIST': None}

    def extract_precinct_split(self, input_dict):
        # Found some precincts that don't follow this standard
        try:
            precinct_split = "%04d/%02d"%(int(input_dict['PrecinctCode']), int(input_dict['PrecinctPart']))
        except ValueError:
            precinct_split = input_dict['PrecinctCode'] + "/" +input_dict['PrecinctPart']

        return {'PRECINCT_SPLIT':precinct_split}

if __name__ == '__main__':
    preparer = StatePreparer(*sys.argv[1:])
    preparer.process()
