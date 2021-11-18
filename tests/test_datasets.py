"""This module contains the tests for the DatasetsClient."""
import os
import unittest
from .helpers import get_random_name
from axiom import Client, DatasetCreateRequest, DatasetUpdateRequest


class TestDatasets(unittest.TestCase):

    dataset_name = get_random_name()

    def setUp(self):
        self.client = Client(
            os.getenv("AXIOM_DEPLOYMENT_URL"),
            os.getenv("AXIOM_TOKEN"),
            os.getenv("AXIOM_ORG_ID"),
        )
        print(f"generated database name is: {self.dataset_name}")

    def test_create(self):
        """Tests create dataset endpoint"""
        req = DatasetCreateRequest(
            name=self.dataset_name,
            description="create a dataset to test the python client",
        )
        res = self.client.datasets.create(req)
        print(res)
        assert res.name == self.dataset_name

    def test_ingest(self):
        """Tests the ingest endpoint"""
        res = self.client.datasets.ingest(
            self.dataset_name, [{"foo": "bar"}, {"bar": "baz"}]
        )
        print(res)

        assert (
            res.ingested == 2
        ), f"expected ingested count to equal 2, found {res.ingested}"

    def test_get(self):
        """Tests get dataset endpoint"""
        dataset = self.client.datasets.get(self.dataset_name)
        print(dataset)

        assert dataset.name == self.dataset_name

    def test_list(self):
        """Tests list datasets endpoint"""
        datasets = self.client.datasets.get_list()
        print(datasets)

        assert len(datasets) > 0

    def test_update(self):
        """Tests update dataset endpoint"""
        updateReq = DatasetUpdateRequest("updated name through test")
        ds = self.client.datasets.update(self.dataset_name, updateReq)

        assert ds.description == updateReq.description
