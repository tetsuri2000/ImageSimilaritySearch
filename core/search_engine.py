class SearchEngine:
    @staticmethod
    def distance_to_similarity(distance):
        return round(max(0.0, 100.0 - (distance / 5.0)), 2)

    @staticmethod
    def search(index, paths, query_feature, min_similarity):
        D, I = index.search(query_feature.reshape(1, -1), len(paths))
        results = []
        for d, idx in zip(D[0], I[0]):
            sim = SearchEngine.distance_to_similarity(d)
            path = paths[idx]
            if sim >= min_similarity:
                results.append((sim, path))
        return results