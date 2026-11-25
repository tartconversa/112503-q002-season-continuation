"""读取合成业务交接资料并核对表间关联。"""
import csv
import unittest
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "samples"

HEADERS = {'episodes.csv': ['edition', 'segment', 'story_episode', 'begin', 'end', 'min_complete_seconds'], 'windows.csv': ['window', 'region', 'tier', 'story_episode', 'start', 'stop', 'revision'], 'memberships.csv': ['household', 'region', 'tier', 'start', 'stop'], 'views.csv': ['view', 'household', 'edition', 'segment', 'started_on', 'begin', 'end'], 'promises.csv': ['notice', 'household', 'window', 'public_date', 'promised_day', 'state'], 'returns.csv': ['plan', 'region', 'edition', 'release_day', 'translation_job', 'provider', 'capacity_units', 'available_units'], 'observation.csv': ['cut', 'as_of', 'data_received', 'license_rev']}
REFERENCES = [('views.csv', 'household', 'memberships.csv', 'household'), ('views.csv', 'edition', 'episodes.csv', 'edition'), ('promises.csv', 'window', 'windows.csv', 'window'), ('promises.csv', 'household', 'memberships.csv', 'household'), ('returns.csv', 'edition', 'episodes.csv', 'edition')]
OBSERVED_VALUES = [('views.csv', 'household', 'H3', 2), ('windows.csv', 'window', 'W6', 2), ('returns.csv', 'provider', 'T1', 3)]

class SampleContract(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.sources = {}
        for name in HEADERS:
            with (DATA / name).open(encoding="utf-8", newline="") as source:
                reader = csv.DictReader(source, strict=True)
                if reader.fieldnames != HEADERS[name]:
                    raise ValueError(f"字段不一致：{name}")
                cls.sources[name] = list(reader)

    def test_tabular_structure(self):
        for name, rows in self.sources.items():
            with self.subTest(source=name):
                self.assertTrue(rows)
                self.assertTrue(all(None not in row and None not in row.values() for row in rows))

    def test_related_source_keys(self):
        for left, column, right, target in REFERENCES:
            with self.subTest(source=left, field=column):
                actual = {row[column] for row in self.sources[left] if row[column]}
                allowed = {row[target] for row in self.sources[right] if row[target]}
                self.assertTrue(actual)
                self.assertEqual(actual - allowed, set())

    def test_shared_or_revised_facts_have_source_rows(self):
        for name, column, value, minimum in OBSERVED_VALUES:
            with self.subTest(source=name, field=column, value=value):
                self.assertGreaterEqual(sum(row[column] == value for row in self.sources[name]), minimum)
