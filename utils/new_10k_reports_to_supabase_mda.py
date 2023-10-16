import pandas as pd


def new_10k_reports_to_supabase_mda(all_parsed_data_list, Client):
    try:
        # Convert the parsed data list to a DataFrame
        parsed_data_df = pd.DataFrame(all_parsed_data_list)

        # Fetch the existing reports from Supabase
        existing_reports_in_supabase = Client.table("reports_10k").select("*").execute()

        # Check if data exists and get the accession numbers
        if existing_reports_in_supabase.data:
            existing_accession_numbers = [
                record["accession_number"]
                for record in existing_reports_in_supabase.data
            ]
        else:
            existing_accession_numbers = []

        # Filter out the reports that are already in the database
        filtered_reports_df = parsed_data_df[
            ~parsed_data_df["accession_number"].isin(existing_accession_numbers)
        ]
        formatted_filtered_reports = filtered_reports_df.to_dict(orient="records")

        # Insert the new data into the reports_10k table
        if formatted_filtered_reports:
            data_reports = (
                Client.table("reports_10k").insert(formatted_filtered_reports).execute()
            )

            # Handle any errors during the insertion process
            if data_reports.error:
                print(f"Supabase Error: {data_reports.error}")

            assert len(data_reports.data) > 0, "No reports were embedded successfully."
            return data_reports.data

        else:
            print("No new reports to add.")
            return []

    except Exception as e:
        print(f"An error occurred during embedding: {e}")
        return []
