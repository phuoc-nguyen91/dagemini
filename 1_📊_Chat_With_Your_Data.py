import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from dotenv import load_dotenv

from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent,AgentType
#from langchain.agents import create_pandas_dataframe_agent, AgentType
from langchain_google_genai import chat_models
from langchain_google_vertexai import VertexAI
from langchain_google_genai import ChatGoogleGenerativeAI


from src.logger.base import BaseLogger
from src.models.llms import load_llm
from src.utils import *

import logging

# load environment varibles
load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

#MODEL_NAME = "openai-api"
MODEL_NAME = "gemini-1.5-pro-002"
def process_query(da_agent, query):

    try:
        response = da_agent(query)

        action = response["intermediate_steps"][-1][0].tool_input

        #   Loại bỏ dấu ``` ở đầu và cuối
        action = action.strip().strip('`')
        # Loại bỏ "python" ở đầu nếu có
        action = action.lstrip('python').strip()
        to_display_string = ""
       

        if "plt" in action:
            st.write(response["output"])

            fig = execute_plt_code(action, df=st.session_state.df)
            if fig:
                st.pyplot(fig)

            st.write("**Executed code:**")
            st.code(action)

            to_display_string = response["output"] + "\n" + f"```python\n{action}\n```"
            st.session_state.history.append((query, to_display_string))

        else:
            # action = action.lstrip('print').strip()
            
            # result = execute_df_code(action, df=st.session_state.df)
            # logger.info(f" ### result from  execute_df_code {result} ! ###")
            # st.write("**Executed code:**")
            # st.code(action)
            # if result is not None:
            #     st.write(result)
            #     to_display_string = str(result) + "\n" + f"```python\n{action}\n```"
            #     st.session_state.history.append((query, to_display_string))
            # else:
                st.write(response["output"])
                st.session_state.history.append((query, response["output"]))
    except Exception as e:
        logger.exception(f"Error in process_query: {str(e)}")
        st.error(f"An error occurred: {str(e)}")

def display_chat_history():
    st.markdown("## Chat History: ")
    for i, (q, r) in enumerate(st.session_state.history):
        st.markdown(f"**Query: {i+1}:** {q}")
        st.markdown(f"**Response: {i+1}:** {r}")
        st.markdown("---")

def main():
    # Set up streamlit interface
    st.set_page_config(page_title="📊 Smart Data Analysis Tool", page_icon="📊", layout="centered")
    st.header("📊 Smart Data Analysis Tool")
    st.write(
        "### Welcome to our data analysis tool. This tools can assist your daily data analysis tasks. Please enjoy !"
    )

    # Load llms model
    llm =  load_llm(model_name = MODEL_NAME)
    logger.info(f" ### Successfully loaded {MODEL_NAME} ! ###")
    st.write("### LLM Configuration:")
    st.write(f"Model Name: {MODEL_NAME}")
    st.write(f"LLM Type: {type(llm)}")
    if hasattr(llm, 'client'):
        st.write(f"Client Type: {type(llm.client)}")

    # Upload csv file
    with st.sidebar:
        uploaded_file = st.file_uploader("Upload your csv file here", type="csv")

    # Initial chat history 
    if "history" not in st.session_state:
        st.session_state.history = []

    # Read csv file
    if uploaded_file is not None:
        st.session_state.df = pd.read_csv(uploaded_file)
        st.write("### Your uploaded data: ", st.session_state.df.head())

        try:
            
            # Create data analysis agent to query with our data
            da_agent = create_pandas_dataframe_agent(
                llm=llm,
                df=st.session_state.df,
                #agent_type="tool-calling",
                #agent_type=AgentType.ZERO_SHOT_REACT_DESCRIPTION,  # Thêm dòng này
                allow_dangerous_code=True,
                verbose=True,
                return_intermediate_steps=True,
                handle_parsing_errors=True  # Thêm dòng này
            )

            logging.info("### Successfully loaded data analysis agent! ###")
            print(da_agent)

            # Input query and process query
            query = st.text_input("Enter your questions: ")

            if st.button("Run query"):
                with st.spinner("Processing..."):
                    process_query(da_agent, query)
        except Exception as e:
            st.error(f"Error creating or using the agent: {str(e)}")
            logging.exception(f"Error in main function: {str(e)}")


    # Display chat history
    st.divider()
    display_chat_history()



if __name__ == "__main__":
    main()


# import matplotlib.pyplot as plt
# import pandas as pd
# import streamlit as st
# from dotenv import load_dotenv
# from langchain_experimental.agents.agent_toolkits.pandas.base import create_pandas_dataframe_agent
# from langchain_openai import ChatOpenAI

# from src.logger.base import BaseLogger
# from src.models.llms import load_llm
# from src.utils import execute_plt_code

# # load environment varibles
# load_dotenv()
# logger = BaseLogger()
# MODEL_NAME = "gpt-3.5-turbo"


# def process_query(da_agent, query):

#     response = da_agent(query)

#     action = response["intermediate_steps"][-1][0].tool_input["query"]

#     if "plt" in action:
#         st.write(response["output"])

#         fig = execute_plt_code(action, df=st.session_state.df)
#         if fig:
#             st.pyplot(fig)

#         st.write("**Executed code:**")
#         st.code(action)

#         to_display_string = response["output"] + "\n" + f"```python\n{action}\n```"
#         st.session_state.history.append((query, to_display_string))

#     else:
#         st.write(response["output"])
#         st.session_state.history.append((query, response["output"]))


# def display_chat_history():
#     st.markdown("## Chat History: ")
#     for i, (q, r) in enumerate(st.session_state.history):
#         st.markdown(f"**Query: {i+1}:** {q}")
#         st.markdown(f"**Response: {i+1}:** {r}")
#         st.markdown("---")


# def main():

#     # Set up streamlit interface
#     st.set_page_config(page_title="📊 Smart Data Analysis Tool", page_icon="📊", layout="centered")
#     st.header("📊 Smart Data Analysis Tool")
#     st.write(
#         "### Welcome to our data analysis tool. This tools can assist your daily data analysis tasks. Please enjoy !"
#     )

#     # Load llms model
#     llm = load_llm(model_name=MODEL_NAME)
#     logger.info(f"### Successfully loaded {MODEL_NAME} !###")

#     # Upload csv file
#     with st.sidebar:
#         uploaded_file = st.file_uploader("Upload your csv file here", type="csv")

#     # Initial chat history
#     if "history" not in st.session_state:
#         st.session_state.history = []

#     # Read csv file
#     if uploaded_file is not None:
#         st.session_state.df = pd.read_csv(uploaded_file)
#         st.write("### Your uploaded data: ", st.session_state.df.head())

#         # Create data analysis agent to query with our data
#         da_agent = create_pandas_dataframe_agent(
#             llm=llm,
#             df=st.session_state.df,
#             agent_type="tool-calling",
#             allow_dangerous_code=True,
#             verbose=True,
#             return_intermediate_steps=True,
#         )
#         logger.info("### Sucessfully loaded data analysis agent !###")

#         # Input query and process query
#         query = st.text_input("Enter your questions: ")

#         if st.button("Run query"):
#             with st.spinner("Processing..."):
#                 process_query(da_agent, query)

#     # Display chat history
#     st.divider()
#     display_chat_history()


# if __name__ == "__main__":
#     main()