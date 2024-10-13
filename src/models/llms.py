# import os
# from google.auth.exceptions import DefaultCredentialsError
# from google.cloud import aiplatform
# from langchain_google_vertexai import ChatVertexAI
# from langchain_google_genai import ChatGoogleGenerativeAI
# from google.auth import default
# from google.auth.transport.requests import Request

# def load_llm(model_name):
#     project_id = "lateral-pathway-435802-i3"
#     #location = "us-central1"
#     location = "asia-east2"
    
#     # Set Google Cloud credentials environment variable
#     os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "C:/Users/LENOVO/AppData/Roaming/gcloud/application_default_credentials.json"

#     try:
#         # Initialize Vertex AI
#         aiplatform.init(project=project_id, location=location)

#         if model_name == "gemini-1.5-flash-002":
#             return ChatVertexAI(
#                 model_name=model_name,
#                 project=project_id,
#                 location=location,
#                 max_output_tokens=8192,
#                 temperature=0.0,
#                 #top_k=40,
#                 #top_p=0.95,
#             )
#         elif model_name == "gemini-1.5-pro-002":
#             return ChatVertexAI(
#                 model_name=model_name,
#                 project=project_id,
#                 location=location,
#                 max_output_tokens=8192,
#                 temperature=0.0,
#                 #top_k=40,
#                 #top_p=0.95,
#             )
#         elif model_name == "gpt-3.5-turbo":
#             # Use GPT-3.5-turbo through Vertex AI
#             return ChatVertexAI(
#                 model_name="chat-bison",  # This is the Vertex AI name for GPT-3.5-turbo
#                 project=project_id,
#                 location=location,
#                 max_output_tokens=1000,
#                 temperature=0.0,
#             )
#         else:
#             raise ValueError("Unknown model. Choose from ['gemini-1.5-pro-002', 'gemini-1.5-002', 'gpt-3.5-turbo']")
#     except DefaultCredentialsError:
#         print("Unable to find default credentials. Make sure you have set up your Google Cloud credentials correctly.")
#         return None
#     except Exception as e:
#         print(f"An error occurred: {str(e)}")
#         return None

from langchain_google_genai import ChatGoogleGenerativeAI


def load_llm(model_name):
    """Load Large Language Model.

    Args:
        model_name (str): The name of the model to load.

    Raises:
        ValueError: If the model_name is not recognized.

    Returns:
        ChatGoogleGenerativeAI: An instance of ChatGoogleGenerativeAI configured for the specified model.
    """

    if model_name == "gemini-1.5-flash-002":
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.0,
            max_tokens=1000,
        )
    elif model_name == "gemini-1.5-pro-002":
        return ChatGoogleGenerativeAI(
            model=model_name,
            temperature=0.0,
            max_tokens=1000,
        )
    elif model_name == "gemini-pro":
        # Import Gemini and Return Gemini mode
        pass
    else:
        raise ValueError(
            "Unknown model.\
                Please choose from ['gemini-1.5-pro-002','gemini-1.5-flash-002', ...]"
        )


