from typing import List, Optional, Union
import pandas
from pydantic import BaseModel, validator

class cliCredentialModel(BaseModel):
    description: str
    username: str
    password: str
    enablePassword: str

    @validator('description')
    def descriptionValidator(cls, x):
        chars = set('?!')
        if any((c in chars) for c in x):
            raise ValueError('Use letters, numbers, spaces and -_. characters')
        return x.title()

    @validator('username', 'password', 'enablePassword')
    def username_password_enablePasswordValidator(cls, x):
        chars = set('<> ')
        if any((c in chars) for c in x):
            raise ValueError('<> and spaces are not allowed')
        return x.title()


class snmpV2cReadCredentialsModel(BaseModel):
    description: str
    readCommunity: str

    @validator('description')
    def descriptionValidator(cls, x):
        chars = set('?!')
        if any((c in chars) for c in x):
            raise ValueError('Use letters, numbers, spaces and -_. characters')
        return x.title()

    @validator('readCommunity')
    def readCommunityValidator(cls, x):
        chars = set('<> ')
        if any((c in chars) for c in x):
            raise ValueError('<> and spaces are not allowed')
        return x.title()

class snmpV2cWriteCredentialsModel(BaseModel):
    description: str
    writeCommunity: str

    @validator('description')
    def descriptionValidator(cls, x):
        chars = set('?!')
        if any((c in chars) for c in x):
            raise ValueError('Use letters, numbers, spaces and -_. characters')
        return x.title()

    @validator('writeCommunity')
    def writeCommunityValidator(cls, x):
        chars = set('<> ')
        if any((c in chars) for c in x):
            raise ValueError('<> and spaces are not allowed')
        return x.title()

class snmpV3CredentialsModel(BaseModel):
    description: str
    username: str
    privacyType: str
    privacyPassword: str
    authType: str
    authPassword: str
    snmpMode: str
    
    @validator('description')
    def descriptionValidator(cls, x):
        chars = set('?!')
        if any((c in chars) for c in x):
            raise ValueError('Use letters, numbers, spaces and -_. characters')
        return x.title()

    @validator('username')
    def usernameValidator(cls, x):
        chars = set('?! ')
        if any((c in chars) for c in x):
            raise ValueError('Use letters, numbers, and -_.@ characters')
        return x.title()

    @validator('privacyPassword', 'authPassword')
    def privacyPassword_authPasswordValidator(cls, x):
        chars = set('<> ')
        if (any((c in chars) for c in x)):
            raise ValueError('<> and spaces are not allowed')
        elif len(x) < 8:
            raise ValueError('Minimum 8 characters')
        return x.title()

class httpsCredentialsModel(BaseModel):
    name: str
    username: str
    password: str
    port: int

class settingsModel(BaseModel):
    cliCredential: Optional[List[cliCredentialModel]]
    snmpV2cRead: Optional[List[snmpV2cReadCredentialsModel]]
    snmpV2cWrite: Optional[List[snmpV2cWriteCredentialsModel]]
    snmpV3: Optional[List[snmpV3CredentialsModel]]
    httpsRead: Optional[List[httpsCredentialsModel]]
    httpsWrite: Optional[List[httpsCredentialsModel]]

class credentialsModel(BaseModel):
   settings: settingsModel 

def create_credentials(credentials_loc, api):
        
    cli_df = pandas.read_excel(credentials_loc, sheet_name="CLI")
    cli = (cli_df.rename(columns={"Description": "description", "Username": "username", "Password": "password", "Enable Password": "enablePassword"})).to_dict('records')

    snmpv2c_df = pandas.read_excel(credentials_loc, sheet_name="SNMPV2C")
    snmpv2cRead = (((snmpv2c_df.loc[snmpv2c_df["Type"] == "SNMPv2C Read"]).drop(columns="Type")).rename(columns={"Description": "description", "Community": "readCommunity"})).to_dict('records')
    snmpv2cWrite = (((snmpv2c_df.loc[snmpv2c_df["Type"] == "SNMPv2C Write"]).drop(columns="Type")).rename(columns={"Description": "description", "Community": "writeCommunity"})).to_dict('records')

    snmpv3_df = pandas.read_excel(credentials_loc, sheet_name="SNMPV3")
    snmpv3_df = snmpv3_df.replace({"Authentication and Privacy": "AUTHPRIV"})
    snmpv3 = ((snmpv3_df).rename(columns={"SNMP Mode": "snmpMode", "Description": "description", "Username": "username", "Privacy Type": "privacyType", "Privacy Password": "privacyPassword", "Auth Type": "authType", "Auth Password": "authPassword"})).to_dict('records')
    
    https_df = pandas.read_excel(credentials_loc, sheet_name="HTTPS")
    httpsRead = (((https_df.loc[https_df["Type"] == "HTTPS Read"]).drop(columns="Type")).rename(columns={"Description": "name", "Username": "username", "Password": "password", "Port": "port"})).to_dict('records')
    httpsWrite = (((https_df.loc[https_df["Type"] == "HTTPS Write"]).drop(columns="Type")).rename(columns={"Description": "name", "Username": "username", "Password": "password", "Port": "port"})).to_dict('records')

    
    settings = settingsModel(cliCredential = cli, snmpV2cRead = snmpv2cRead, snmpV2cWrite = snmpv2cWrite, snmpV3 = snmpv3, httpsRead = httpsRead, httpsWrite = httpsWrite)
    credentialSettings = credentialsModel(settings = settings)

    print(credentialSettings.json())
    api.network_settings.create_device_credentials(payload=credentialSettings.dict())