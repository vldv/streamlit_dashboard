import streamlit as st

def main():
    st.header('FAQ')
    st.subheader('what')

    st.write("click pas [ici](https://discuss.streamlit.io/t/hyperlink-in-streamlit-without-markdown/7046/2)")

    with st.expander("foo"):
        i=1
        cols = st.columns(4)
        cols[0].write(f'{i}')
        cols[1].write(f'{i * i}')
        cols[2].write(f'{i * i * i}')
        cols[3].write('x' * i)
    with st.expander("bar"):
        i=1
        cols = st.columns(3)
        cols[0].write(f'{i}')
        cols[1].write(f'{i * i}')
        cols[2].write(f'{i * i * i}')
