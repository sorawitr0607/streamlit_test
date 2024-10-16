# Import Streamlit and Pandas
import streamlit as st
import pandas as pd

# Import for API calls
import requests

# Import for dyanmic tagging
from streamlit_tags import st_tags

#######################################################
# The code below is to control the layout width of the app.
# if "widen" not in st.session_state:
#     layout = "centered"
# else:
#     layout = "wide" if st.session_state.widen else "centered"
#######################################################

# The code below is for the title and logo.
st.set_page_config(layout='wide', page_title="Zero-Shot Text Classifier", page_icon="😎")

#######################################################
# Set up session state so app interactions don't reset the app.
if not "valid_inputs_received" in st.session_state:
    st.session_state["valid_inputs_received"] = False
    
if not "disabled" in st.session_state:
    st.session_state["disabled"] = False
    
# if not "re_button" in st.session_state:
#     st.session_state["re_button"] = True
    
if not "disabled_button" in st.session_state:
    st.session_state["disabled_button"] = True

#######################################################

# The block of code below is to display the title, logos and introduce the app.

c1, c2 = st.columns([4,0.1])

with c1:

    st.title("🔠 Zero-Shot Text Classifier")

with c2:

    st.write('')


st.subheader(
    """
Classify keyphrases with this app. No ML training needed! 
Create classifying labels (e.g. `Positive`, `Negative` and `Neutral`), paste your keyphrases!  
"""
)
# st.checkbox(
#     "Widen layout",
#     key="widen",
#     help="Tick this box to toggle the layout to 'Wide' mode",
# )
# Sidebar
# with stylable_container(
#     key='logo_image',
#     css_styles="""
#     div[data-testid="stImageContainer"] img {
#     background: #e9ecef;
#     border-radius: 10px;
#     border: thick;
#     border-style: inset;
#     border-color: black;
#     }
#     """
#     ):
st.sidebar.image('logo.png') 
st.markdown("""
<style>
    div[data-testid="stSidebarUserContent"] img {
        background: #ffffff;
        border-radius: 20px;
        border: thick;
        border-style: inset;
        border-color: black;
    }
</style>
""", unsafe_allow_html=True)


#st.sidebar.image(r'C:\Users\Sorawitr\Desktop\streamlit\logo.png',width=180)
st.sidebar.header("About")

st.sidebar.markdown(
    """

App using 🎈[Streamlit](https://streamlit.io/) and [HuggingFace](https://huggingface.co/inference-api)'s [Distilbart-mnli-12-3](https://huggingface.co/valhalla/distilbart-mnli-12-3) model.

""")

st.sidebar.markdown(
    "[Streamlit](https://streamlit.io) is a Python library that allows the creation of interactive, data-driven web applications in Python."
)
st.sidebar.divider()

st.sidebar.header("Resources")
st.sidebar.markdown(
    """
- [Streamlit Documentation](https://docs.streamlit.io/)
- [Cheat sheet](https://docs.streamlit.io/library/cheatsheet)
- [Book](https://www.amazon.com/dp/180056550X) (Getting Started with Streamlit for Data Science)
- [Blog](https://blog.streamlit.io/how-to-master-streamlit-for-data-science/) (How to master Streamlit for data science)
"""
)
#######################################################


def main():
    st.caption("")
def disable(b):
    st.session_state["disabled"] = b
    if st.session_state.get("but_a", False):
        st.session_state["disabled_button"] = True
    else:
        st.session_state["disabled_button"] = False


API_KEY = st.secrets["API_KEY"]

API_URL = (
    "https://api-inference.huggingface.co/models/valhalla/distilbart-mnli-12-3"
)

headers = {"Authorization": f"Bearer {API_KEY}"}

with st.form(key="my_form"):

    multiselectComponent = st_tags(
        label="",
        text="Add labels - 3 max",
        value=["Positive", "Negative", "Neutral"],
        suggestions=[
            "Informational",
            "Transactional",
            "Navigational",
            "Positive",
            "Negative",
            "Neutral",
        ],
        maxtags=3,
    )
    new_line = "\n"
    nums = [
        "I want to buy something in this store",
        "How to ask a question about a product",
        "I have a problem with my product that needs to be resolved asap!",
        "Can I have the link to the product?",
        "Hugging Face is awesome!"
    ]

    sample = f"{new_line.join(map(str, nums))}"
    linesDeduped2 = []

    MAX_LINES = 5
    text = st.text_area(
        "Enter keyphrases to classify",
        sample,
        height=200,
        key="2",
        help="At least two keyphrases for the classifier to work, one per line, "
        + str(MAX_LINES)
        + " keyphrases max as part of the demo",
    )
    lines = text.split("\n")  # A list of lines
    linesList = []
    for x in lines:
        linesList.append(x)
    linesList = list(dict.fromkeys(linesList))  # Remove dupes
    linesList = list(filter(None, linesList))  # Remove empty
    if len(linesList) > MAX_LINES:

        st.info(
            "Only the first "
            + str(MAX_LINES)
            + " keyprases will be reviewed"
        )

    linesList = linesList[:MAX_LINES]

    submit_button = st.form_submit_button(label="Submit", on_click=disable, args=(True,), disabled=st.session_state.disabled)
    
    
button_a = st.button('New Keyphrases', key='but_a', on_click=disable, args=(False,), disabled=st.session_state.disabled_button)
if not submit_button and not st.session_state.valid_inputs_received:
    st.stop()
    
elif submit_button and not text:
    st.warning("There is no keyphrases to classify")
    st.session_state.valid_inputs_received = False
    st.stop()
    
elif submit_button and not multiselectComponent:
    st.warning("❄️ You have not added any labels, please add some! ")
    st.session_state.valid_inputs_received = False
    st.stop()

elif submit_button and len(multiselectComponent) == 1:
    st.warning("❄️ Please make sure to add at least two labels for classification")
    st.session_state.valid_inputs_received = False
    st.stop()
elif (submit_button or st.session_state.valid_inputs_received) and st.session_state["disabled"]:

    if submit_button:
        st.session_state.valid_inputs_received = True


    def query(payload):
        response = requests.post(API_URL, headers=headers, json=payload)
        # Unhash to check status codes from the API response
        # st.write(response.status_code)
        return response.json()
    my_bar = st.progress(0)
    percent_complete =0
   
    listToAppend = []
    n_progress = 1/len(linesList)
    for row in linesList:
        output2 = query(
            {
                "inputs": row,
                "parameters": {"candidate_labels": multiselectComponent},
                "options": {"wait_for_model": True},
            }
        )

        listToAppend.append(output2)

        df = pd.DataFrame.from_dict(output2)
        percent_complete+=n_progress
        my_bar.progress(percent_complete)
        


    st.success("✅ Done!")
    df = pd.DataFrame.from_dict(listToAppend)
    st.session_state.re_button = False
    st.caption("")
    st.markdown("### Check classifier results")
    st.caption("")
    st.caption("")

    # This is a list comprehension to convert the decimals to percentages
    f = [[f"{x:.2%}" for x in row] for row in df["scores"]]

    # This code is for re-integrating the labels back into the dataframe
    df["classification scores"] = f
    df.drop("scores", inplace=True, axis=1)

    # This code is to rename the columns
    df.rename(columns={"sequence": "keyphrase"}, inplace=True)

    # The code below is for Ag-grid

        
    # gb = GridOptionsBuilder.from_dataframe(df)
    # # enables pivoting on all columns
    # gb.configure_default_column(
    #     enablePivot=True, enableValue=True, enableRowGroup=True
    # )
    # gb.configure_selection(selection_mode="multiple", use_checkbox=True)
    # gb.configure_side_bar()
    # gridOptions = gb.build()

    # response = AgGrid(
    #     df,
    #     gridOptions=gridOptions,
    #     enable_enterprise_modules=True,
    #     update_mode=GridUpdateMode.MODEL_CHANGED,
    #     data_return_mode=DataReturnMode.FILTERED_AND_SORTED,
    #     height=300,
    #     fit_columns_on_grid_load=False,
    #     configure_side_bar=True,
    # )
    
    columns = {}
    
    # Iterate over the rows of the DataFrame
    for index, row in df.iterrows():
        for label, score in zip(row['labels'], row['classification scores']):
            column_name = f'{label}_Labels_Score'
            if column_name not in columns:
                columns[column_name] = []
            columns[column_name].append(score)
    
    # Add the new columns to the DataFrame
    for col_name, col_values in columns.items():
        df[col_name] = col_values
    
    # Drop the original 'labels' and 'classification scores' columns
    df = df.drop(columns=['labels', 'classification scores'])


    st.dataframe(df,hide_index=True,width=1500)
    # The code below is for the download button

    cs, c1 = st.columns([2, 2])

    with cs:

        @st.cache_data
        def convert_df(df):
            # IMPORTANT: Cache the conversion to prevent computation on every rerun
            return df.to_csv().encode("utf-8")

        csv = convert_df(df)  #

        st.download_button(
            label="Download results as CSV",
            data=csv,
            file_name="results.csv",
            mime="text/csv")


if __name__ == "__main__":
    main()



