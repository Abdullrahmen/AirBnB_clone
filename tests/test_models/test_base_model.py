#!/usr/bin/python3
"""
Contains BaseModel class tests
"""

import unittest
from datetime import datetime
from models.base_model import BaseModel
from uuid import UUID


class TestBaseModel(unittest.TestCase):
    """Tests for BaseModel class"""

    def test_init(self):
        """Test init method"""
        bs = BaseModel()
        self.assertIsInstance(bs.created_at, datetime)
        self.assertIsInstance(bs.updated_at, datetime)
        self.assertIsInstance(bs.id, str)

    def test_init_from_kwargs(self):
        """Test init method with kwargs"""
        bs = BaseModel()
        bs2 = BaseModel(**bs.to_dict())
        self.assertEqual(bs.__dict__, bs2.__dict__)

    def test_str(self):
        """Test __str__ method"""
        bs = BaseModel()
        self.assertEqual(bs.__str__(),
                         f"[BaseModel] ({bs.id}) <{bs.__dict__}>")

    def test_save(self):
        """test save method"""
        bs = BaseModel()
        t1 = bs.updated_at
        bs.save()
        self.assertNotEqual(bs.updated_at, t1)

    def test_to_dict(self):
        """Test to_dict method"""
        bs = BaseModel()
        before = bs.__dict__.copy()
        dict_ = bs.to_dict()
        self.assertIsInstance(dict_, dict)
        self.assertEqual(dict_["__class__"], "BaseModel")
        self.assertEqual(dict_["created_at"], bs.created_at.isoformat())
        self.assertEqual(dict_["updated_at"], bs.updated_at.isoformat())
        self.assertEqual(before, bs.__dict__)


if __name__ == '__main__':
    unittest.main()
