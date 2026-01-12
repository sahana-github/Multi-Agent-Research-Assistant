def get_initial_context(user_input, modality="text"):
    return {
        "version": "1.0",
        "context": {
            "user_query": user_input,
            "modality": modality,
            "search_results": [],
            "summary": "",
            "metadata": {}
        }
    }
