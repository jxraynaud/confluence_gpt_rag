import os
import yaml
from langchain.vectorstores import FAISS
from langchain.embeddings import OpenAIEmbeddings

def load_all_faiss() -> FAISS:
    """
    Load and merge all Faiss indexes from the orchestrations directory.

    Returns:
        FAISS: Merged Faiss index containing all the indexes of all the orchestrations
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    config_path = os.path.join(script_dir, '..', 'config.yaml')

    with open(config_path, 'r') as config_file:
        config = yaml.safe_load(config_file)
    orchestration_dir = config['faiss_data_dir']
    merged_index = None

    # Iterate over all files and directories in the orchestration directory
    for item in os.listdir(orchestration_dir):
        item_path = os.path.join(orchestration_dir, item)

        # Check if the item is a directory
        if os.path.isdir(item_path):
            # Load the Faiss index from the directory
            if os.path.exists(item_path):
                faiss_index = FAISS.load_local(item_path, OpenAIEmbeddings())

                # Merge the index with the previously loaded indexes
                if merged_index is None:
                    merged_index = faiss_index
                else:
                    merged_index.merge_from(faiss_index)

    return merged_index