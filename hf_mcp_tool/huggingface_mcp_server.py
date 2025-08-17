from flask import Flask, request, jsonify
from huggingface_hub import HfApi, hf_hub_url
import json

app = Flask(__name__)
api = HfApi()

def get_tool_metadata():
    return {
        "mcp_version": "0.1",
        "tools": [
            {
                "name": "model_search",
                "description": "Find Machine Learning models hosted on Hugging Face.",
                "parameters": [
                    {"name": "query", "type": "string", "description": "Search term."},
                    {"name": "author", "type": "string", "description": "Organization or user who created the model."},
                    {"name": "task", "type": "string", "description": "Model task type."},
                    {"name": "sort", "type": "string", "description": "Sort order: downloads, likes, lastModified."},
                    {"name": "limit", "type": "number", "description": "Maximum number of results to return."}
                ]
            },
            {
                "name": "dataset_search",
                "description": "Find Datasets hosted on the Hugging Face hub.",
                "parameters": [
                    {"name": "query", "type": "string", "description": "Search term."},
                    {"name": "author", "type": "string", "description": "Organization or user who created the dataset."},
                    {"name": "sort", "type": "string", "description": "Sort order: downloads, likes, lastModified."},
                    {"name": "limit", "type": "number", "description": "Maximum number of results to return."}
                ]
            },
            {
                "name": "space_search",
                "description": "Find Hugging Face Spaces using semantic search.",
                "parameters": [
                    {"name": "query", "type": "string", "description": "Semantic Search Query."},
                    {"name": "limit", "type": "number", "description": "Number of results to return."}
                ]
            }
        ]
    }

@app.route('/mcp', methods=['GET'])
def mcp_schema():
    return jsonify(get_tool_metadata())

@app.route('/mcp/<tool_name>', methods=['POST'])
def execute_tool(tool_name):
    params = request.get_json()
    try:
        if tool_name == "model_search":
            result = api.list_models(
                search=params.get("query"),
                author=params.get("author"),
                task=params.get("task"),
                sort=params.get("sort"),
                limit=int(params.get("limit", 10))
            )
            # Convert model objects to dicts for JSON serialization
            result = [vars(model) for model in result]
        elif tool_name == "dataset_search":
            result = api.list_datasets(
                search=params.get("query"),
                author=params.get("author"),
                sort=params.get("sort"),
                limit=int(params.get("limit", 10))
            )
            result = [vars(dataset) for dataset in result]
        elif tool_name == "space_search":
             result = api.list_spaces(
                search=params.get("query"),
                limit=int(params.get("limit", 10))
            )
             result = [vars(space) for space in result]
        else:
            return jsonify({"error": "Tool not found"}), 404

        # Clean up non-serializable fields if any
        # A simple way is to convert everything to string, but a more robust solution is needed for production
        return jsonify(json.loads(json.dumps(result, default=str)))

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
