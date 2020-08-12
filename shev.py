import streamlit as st
import pandas as pd
import altair as alt

#streamlit sidebar
st.sidebar.markdown("# This is a Sample Streamlit App")
raw = st.sidebar.file_uploader("Input a csv", type="csv")
if raw:
    source = pd.read_csv(raw)

    x_axis = st.sidebar.selectbox("x axis", source.columns)
    y_axis = st.sidebar.selectbox("y axis", source.columns)
    group_by = st.sidebar.selectbox("group", source.columns)

    filtered = st.sidebar.multiselect("Set a filter", list(set(source[group_by])), list(set(source[group_by])))

    st.title("this is a cool title")
    st.dataframe(source)

    #altair example interactive chart
    source = source[source[group_by].isin(filtered)]
    brush = alt.selection(type='interval')

    points = alt.Chart(source).mark_point().encode(
        x=x_axis,
        y=y_axis,
        color=alt.condition(brush, group_by, alt.value('lightgray'))
    ).add_selection(
        brush
    )

    bars = alt.Chart(source).mark_bar().encode(
        y=y_axis,
        color=group_by,
        x=f"count({group_by})"
    ).transform_filter(
        brush
    )

    points & bars
