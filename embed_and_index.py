from transformers import AutoTokenizer, AutoModel
import torch
import numpy as np
from llama_index.core.node_parser import SentenceSplitter
from llama_index.core import VectorStoreIndex, load_index_from_storage
from llama_index.core.storage.storage_context import StorageContext
from llama_index.core.settings import Settings
from llama_index.embeddings.openai.base import BaseEmbedding
from typing import Optional
from llama_index.vector_stores.postgres import PGVectorStore
from postgres_loader import get_postgres_data
from config import SUPABASE_DB_HOST, SUPABASE_DB_NAME, SUPABASE_DB_USER, SUPABASE_DB_PASSWORD, SUPABASE_DB_PORT

class E5SmallV2Embedding(BaseEmbedding):
    model_name: str = "intfloat/e5-small-v2"
    _tokenizer: Optional[AutoTokenizer] = None
    _model: Optional[AutoModel] = None

    def __init__(self, model_name="intfloat/e5-small-v2"):
        super().__init__(model_name=model_name)
        print(f"Loading embedding model: {model_name} on CPU")
        self._tokenizer = AutoTokenizer.from_pretrained(model_name)
        self._model = AutoModel.from_pretrained(model_name)
        self._model.eval()  # Evaluation mode (no gradients)

    def _mean_pooling(self, model_output, attention_mask):
        token_embeddings = model_output[0]  # First element is last hidden state
        input_mask_expanded = attention_mask.unsqueeze(-1).expand(token_embeddings.size()).float()
        return (token_embeddings * input_mask_expanded).sum(1) / input_mask_expanded.sum(1)

    def _get_embedding(self, text: str) -> np.ndarray:
        encoded_input = self._tokenizer(text, padding=True, truncation=True, return_tensors="pt")
        encoded_input = {k: v.to("cpu") for k, v in encoded_input.items()}
        with torch.no_grad():
            model_output = self._model(**encoded_input)
        embedding = self._mean_pooling(model_output, encoded_input['attention_mask'])
        embedding = torch.nn.functional.normalize(embedding, p=2, dim=1)
        return embedding[0].cpu().numpy()

    def _get_text_embedding(self, text: str) -> np.ndarray:
        return self._get_embedding(text)

    def _get_query_embedding(self, query: str) -> np.ndarray:
        return self._get_embedding(query)

    async def _aget_query_embedding(self, query: str) -> np.ndarray:
        return self._get_embedding(query)


def build_index():
    print("Fetching data from Supabase Postgres...")
    documents = get_postgres_data()

    embed_model = E5SmallV2Embedding()
    Settings.embed_model = embed_model

    vector_store = PGVectorStore.from_params(
        database=SUPABASE_DB_NAME,
        host=SUPABASE_DB_HOST,
        password=SUPABASE_DB_PASSWORD,
        user=SUPABASE_DB_USER,
        port=SUPABASE_DB_PORT,
        table_name="documents",
        embed_dim=384
    )

    index = VectorStoreIndex.from_documents(
        documents,
        vector_store=vector_store
    )

    return index