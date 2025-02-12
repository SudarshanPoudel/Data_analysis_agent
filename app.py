import os
import streamlit as st

from src.utils.graph import get_graph_app
from src.tools.summary import get_summary_from_db, delete_summary_from_db
from src.utils.app_handlers import process_question, display_markdown_with_images


app = get_graph_app()


def main():
    st.set_page_config(page_title="Data Analysis Agent", page_icon="📊")

    st.title("📄 Data Analysis Agent")

    # Ensure session state key exists
    if "show_popup" not in st.session_state:
        st.session_state["show_popup"] = False

    def set_popup():
        st.session_state["show_popup"] = True

    uploaded_file = st.file_uploader(
        "Upload a file", type=["xlsx", "csv", "json", "xml"], on_change=set_popup
    )

    if uploaded_file:
        save_path = os.path.join("data", uploaded_file.name)
        cached_summary = get_summary_from_db(save_path)

        if cached_summary and st.session_state["show_popup"]:

            @st.dialog("Warning")
            def confirm_overwrite():
                st.write(
                    f"⚠️ Cached information for **{uploaded_file.name}** already exists.\n\n"
                    "Make sure to delete it if you had made any changes in data."
                )
                col1, col2, col3 = st.columns([1, 1, 3])  # Two buttons in a row

                with col1:
                    if st.button("Delete", type="primary"):
                        delete_summary_from_db(save_path)
                        st.session_state["show_popup"] = False
                        st.rerun()

                with col2:
                    if st.button("Cancel"):
                        st.session_state["show_popup"] = False
                        st.rerun()

            confirm_overwrite()
        else:
            with open(save_path, "wb") as f:
                f.write(uploaded_file.getbuffer())
            st.success("File uploaded successfully!")

        tab_query, tab_report = st.tabs(["Queries", "Report"])

        with tab_query:
            st.header("Ask Questions")
            question = st.text_input("Ask a question:", key="query_input")

            if st.button("Ask"):
                with st.spinner("Processing..."):
                    response = process_question(
                        app, file=uploaded_file.name, query=question
                    )
                st.markdown(response["answer"])
                for chart in response["charts"]:
                    st.image(image=chart)

        with tab_report:
            st.header("Generate Report")

            if st.button("Generate Report"):
                with st.spinner("Generating report..."):
                    response = process_question(app, uploaded_file.name, report="yes")

                pdf_file = response.get("report_path")
                if pdf_file and os.path.exists(pdf_file):
                    with open(pdf_file, "rb") as f:
                        st.download_button(
                            "📥 Download PDF",
                            f,
                            file_name=os.path.basename(pdf_file),
                            mime="application/pdf",
                        )

                display_markdown_with_images(response.get("markdown", ""), st)


if __name__ == "__main__":
    main()
