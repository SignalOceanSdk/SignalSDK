from datetime import datetime, timezone
from typing import Tuple
from unittest.mock import MagicMock
from urllib.parse import urljoin

import requests

from signal_ocean import Connection
from signal_ocean.companies import Company, CompaniesAPI

__mock_company_response = {'ID': 1926, 'CompanyName': 'Signal Maritime',
                           'Website': 'http://signalmaritime.com/',
                           'FleetList': 'http://signalmaritime.com/',
                           'CommercialOperatorVesselTypes': ['Tanker', 'Dry'],
                           'UpdatedDate': '2016-12-23T17:55:50'}

__mock_company = Company(id=1926, company_name='Signal Maritime',
                         website='http://signalmaritime.com/',
                         fleet_list='http://signalmaritime.com/',
                         commercial_operator_vessel_types=('Tanker', 'Dry'),
                         updated_date=datetime.fromisoformat(
                             '2016-12-23T17:55:50').replace(
                             tzinfo=timezone.utc))

__mock_company_response_2 = {'ID': 1, 'CompanyName': 'Signal Ocean',
                             'Website': 'http://signalocean.com/',
                             'FleetList': 'http://signalocean.com/',
                             'CommercialOperatorVesselTypes': [],
                             'UpdatedDate': '2020-09-01T01:01:01'}

__mock_company_2 = Company(id=1, company_name='Signal Ocean',
                           website='http://signalocean.com/',
                           fleet_list='http://signalocean.com/',
                           commercial_operator_vessel_types=(),
                           updated_date=datetime.fromisoformat(
                               '2020-09-01T01:01:01').replace(
                             tzinfo=timezone.utc))

__mock_companies_response = (__mock_company_response,
                             __mock_company_response_2)


def create_companies_api(response: requests.Response) \
        -> Tuple[CompaniesAPI, MagicMock]:
    connection = Connection('', '')
    mocked_make_request = MagicMock(return_value=response)
    connection._make_get_request = mocked_make_request
    api = CompaniesAPI(connection)
    return api, mocked_make_request


def test_returns_none_if_company_does_not_exist():
    response = MagicMock()
    response.status_code = requests.codes.not_found
    api, _ = create_companies_api(response)
    company = api.get_company(company_id=1)
    assert company is None


def test_requests_company_by_id():
    response = MagicMock()
    response.json.return_value = __mock_company_response
    api, mocked_make_request = create_companies_api(response)
    _ = api.get_company(company_id=__mock_company.id)
    url = urljoin(CompaniesAPI.relative_url, f'companies/{__mock_company.id}')
    mocked_make_request.assert_called_with(url)


def test_returns_company_by_id():
    response = MagicMock()
    response.json.return_value = __mock_company_response
    api, _ = create_companies_api(response)
    vessel = api.get_company(company_id=__mock_company.id)
    assert vessel == __mock_company


def test_requests_all_companies():
    response = MagicMock()
    response.json.return_value = __mock_companies_response
    api, mocked_make_request = create_companies_api(response)
    _ = api.get_companies()
    mocked_make_request.assert_called_with(
        urljoin(CompaniesAPI.relative_url, 'companies/all'))


def test_response_all_companies():
    response = MagicMock()
    response.json.return_value = __mock_companies_response
    api, _ = create_companies_api(response)
    companies = api.get_companies()
    assert companies == (__mock_company, __mock_company_2)


def test_requests_search_companies():
    response = MagicMock()
    response.json.return_value = __mock_companies_response
    api, mocked_make_request = create_companies_api(response)
    _ = api.get_companies('signal')
    mocked_make_request.assert_called_with(
        urljoin(CompaniesAPI.relative_url, 'companies/searchByName/signal'))
