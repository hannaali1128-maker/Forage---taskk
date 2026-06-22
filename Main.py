import json
import unittest
import datetime

# Load the JSON files (Ensure these files exist in the same directory)
try:
    with open('./data-1.json', 'r') as f:
        jsonData1 = json.load(f)
    with open('./data-2.json', 'r') as f:
        jsonData2 = json.load(f)
    with open('./data-result.json', 'r') as f:
        jsonExpectedResult = json.load(f)
except FileNotFoundError as e:
    print(f"Warning: Missing mock data file. {e}")
    jsonData1, jsonData2, jsonExpectedResult = {}, {}, {}

def convertFromFormat1(jsonObject):
    locationParts = jsonObject['location'].split('/')

    return {
        'deviceID': jsonObject['deviceID'],
        'deviceType': jsonObject['deviceType'],
        'timestamp': jsonObject['timestamp'],
        'location': {
            'country': locationParts[0],
            'city': locationParts[1],
            'area': locationParts[2],
            'factory': locationParts[3],
            'section': locationParts[4]
        },
        'data': {
            'status': jsonObject['operationStatus'],
            'temperature': jsonObject['temp']
        }
    }

def convertFromFormat2(jsonObject):
    dt = datetime.datetime.strptime(
        jsonObject['timestamp'], "%Y-%m-%dT%H:%M:%S.%fZ"
    )
    timestamp = int(dt.timestamp() * 1000)

    return {
        'deviceID': jsonObject['device']['id'],
        'deviceType': jsonObject['device']['type'],
        'timestamp': timestamp,
        'location': {
            'country': jsonObject['country'],
            'city': jsonObject['city'],
            'area': jsonObject['area'],
            'factory': jsonObject['factory'],
            'section': jsonObject['section']
        },
        'data': {
            'status': jsonObject['data']['status'],
            'temperature': jsonObject['data']['temperature']
        }
    }

def main(jsonObject):
    # Differentiate between format 1 and format 2 based on the 'device' key
    if jsonObject.get('device') is None:
        return convertFromFormat1(jsonObject)
    else:
        return convertFromFormat2(jsonObject)

class TestSolution(unittest.TestCase):

    def test_sanity(self):
        result = json.loads(json.dumps(jsonExpectedResult))
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType1(self):
        if not jsonData1:
            self.skipTest("data-1.json not found")
        result = main(jsonData1)
        self.assertEqual(result, jsonExpectedResult)

    def test_dataType2(self):
        if not jsonData2:
            self.skipTest("data-2.json not found")
        result = main(jsonData2)
        self.assertEqual(result, jsonExpectedResult)

if __name__ == '__main__':
    unittest.main()
