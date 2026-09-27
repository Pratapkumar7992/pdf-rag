import numpy as np
from django.test import SimpleTestCase

from rag.services.vector_store import create_vector_store


class VectorStoreTests(SimpleTestCase):
    def test_create_vector_store_handles_single_chunk_embedding(self):
        embedding = np.array([[0.1, 0.2, 0.3]], dtype='float32')
        index = create_vector_store(embedding, ['chunk one'])
        self.assertIsNotNone(index)

    def test_create_vector_store_handles_empty_chunks(self):
        index = create_vector_store(np.empty((0,), dtype='float32'), [])
        self.assertIsNone(index)
