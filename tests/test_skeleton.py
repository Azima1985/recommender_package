#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
from my_project import recommender

__author__ = "Azima1985"
__copyright__ = "Azima1985"
__license__ = "mit"


def test_recommender():
    assert len(recommender.recommend('shrek'))>=1
    #assert len(recommender.recommendations)>=1
    #assert recommender.final_recommendations != recommender.good_movies
    #with pytest.raises(AssertionError):
     #   fib(-10)
