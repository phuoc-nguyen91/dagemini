import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import streamlit as st


def execute_plt_code(code: str, df: pd.DataFrame):
    """Execute the passing code to plot figure

    Args:
        code (str): action string (containing plt code)
        df (pd.DataFrame): our dataframe

    Returns:
        _type_: plt figure
    """

    try:
        local_vars = {"plt": plt, "df": df}
        compiled_code = compile(code, "<string>", "exec")
        exec(compiled_code, globals(), local_vars)

        return plt.gcf()

    except Exception as e:
        st.error(f"Error excuting plt code: {e}")
        return None
    


def execute_df_code(code: str, df: pd.DataFrame):
    """Execute the passing code to manipulate dataframe

    Args:
        code (str): action string (containing pandas code)
        df (pd.DataFrame): our dataframe

    Returns:
        pd.DataFrame: result of the executed code
    """

    try:
        local_vars = {"df": df, "np": np, "pd": pd}
        compiled_code = compile(code, "<string>", "eval")
        result = eval(compiled_code, globals(), local_vars)

        return result

    except Exception as e:
        st.error(f"Error executing pandas code: {e}")
        return None

