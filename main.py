"""This file is main file."""
# import relation package.

# import project package.
from src.app.pipeline_app import PipelineAPP

if __name__ == '__main__':
    pipeline_app = PipelineAPP()
    pipeline_app.all_pipeline()