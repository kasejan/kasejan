from dnacentersdk import DNACenterAPI



from env import DNA_CENTER_USERNAME, DNA_CENTER_PASSWORD, DNA_CENTER_BASE_URL, DNA_CENTER_VERSION, DNA_CENTER_VERIFY
from Design.Network_Settings import Device_Credentials




api = DNACenterAPI(DNA_CENTER_USERNAME, DNA_CENTER_PASSWORD, base_url=DNA_CENTER_BASE_URL, version=DNA_CENTER_VERSION, verify=DNA_CENTER_VERIFY)

Device_Credentials.create_credentials("Credentials.xlsx", api)






