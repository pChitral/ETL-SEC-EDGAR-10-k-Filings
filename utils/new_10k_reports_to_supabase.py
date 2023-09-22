import pandas as pd


# Function to insert parsed data into Supabase
def new_10k_reports_to_supabase(all_parsed_data_list, Client):
    try:
        parsed_data_df = pd.DataFrame(all_parsed_data_list)
        existing_reports_in_supabase = Client.table("reports_10k").select("*").execute()

        if existing_reports_in_supabase.data:
            existing_accession_numbers = [
                record["accession_number"]
                for record in existing_reports_in_supabase.data
            ]
        else:
            existing_accession_numbers = []

        filtered_reports_df = parsed_data_df[
            ~parsed_data_df["accession_number"].isin(existing_accession_numbers)
        ]
        formatted_filtered_reports = filtered_reports_df.to_dict(orient="records")

        # Inserting the data into the reports_10k table
        data_reports = (
            Client.table("reports_10k").insert(formatted_filtered_reports).execute()
        )

        assert len(data_reports.data) > 0, "No reports were embedded successfully."
        return data_reports.data

    except Exception as e:
        return f"An error occurred during embedding: {e}"
