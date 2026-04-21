import faiss
import pickle
import numpy as np

class IndexManager:
    @staticmethod
    def build_index(features, index_path, paths_path, valid_paths):
        arr = np.array(features).astype("float32")
        index = faiss.IndexFlatL2(arr.shape[1])
        index.add(arr)
        faiss.write_index(index, index_path)
        with open(paths_path, "wb") as f:
            pickle.dump(valid_paths, f)

    @staticmethod
    def load_index(index_path, paths_path):
        index = faiss.read_index(index_path)
        with open(paths_path, "rb") as f:
            paths = pickle.load(f)
        return index, paths