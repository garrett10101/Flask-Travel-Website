import pytest
from unittest.mock import patch
from FlaskCode.flight_prices import flightPrices, search_airport

@patch('requests.get')
def test_flightPrices(mock_get):
    mock_response = {'data': [
        {
            'price': {'amount': '100.00'},
            'legs': [
                {
                    'origin': {'name': 'Los Angeles'},
                    'destination': {'name': 'New York'},
                    'departure': '2023-05-01T08:00:00Z',
                    'arrival': '2023-05-01T16:00:00Z',
                    'duration': 480,
                    'carriers': [{'name': 'Delta'}],
                    'stop_count': 0
                }
            ]
        }
    ]}

    mock_get.return_value.json.return_value = mock_response

    results = flightPrices('LAX', 'JFK', '2023-05-01', '2023-05-05', 2, 1, 0, 'economy', 'price')

    assert len(results) == 1
    assert results[0]['Price'] == '100.00'
    assert results[0]['Origin'] == 'Los Angeles'
    assert results[0]['Destination'] == 'New York'
    assert results[0]['Departure'] == '2023-05-01T08:00:00Z'
    assert results[0]['Arrival'] == '2023-05-01T16:00:00Z'
    assert results[0]['Duration'] == 480
    assert results[0]['Carrier'] == 'Delta'
    assert results[0]['Stops'] == 0


@patch('requests.request')
def test_search_airport(mock_request):
    mock_response = {'data': [
        {'PlaceId': 'NYCA-sky'},
        {'PlaceId': 'JFK-sky'},
        {'PlaceId': 'EWR-sky'}
    ]}

    mock_request.return_value.json.return_value = mock_response

    airport_dict = search_airport('New York City')

    assert airport_dict == {'PlaceId': 'JFK-sky'}
