import streamlit as st
import requests
import pandas as pd
import io


# API Base URL
API_BASE_URL = "http://localhost:8000/purchase"


def main():

    st.title("Customer Purchase Management System")

 
    tab1, tab2 = st.tabs(["Upload", "Analyse"])

  
    with tab1:
        st.header("Upload Purchases")

       
        st.subheader("Add a Single Purchase")
        customer_name = st.text_input("Customer Name")
        country = st.text_input("Country")
        amount = st.number_input("Amount", min_value=0.0, format="%.2f")
        purchase_date = st.date_input("Purchase Date")


        if st.button("Submit Purchase"):
            purchase_data = {
            "customer_name": customer_name,
            "country": country, 
            "amount": amount, 
            "purchase_date": purchase_date.isoformat()  
        }
            response = requests.post(f"{API_BASE_URL}", json=purchase_data)

            if response.status_code == 200:
                st.success("Purchase added successfully!")
                print(response)
            else:
                st.error(f"Error: {response.text}")


        st.subheader("Bulk Upload Purchases")
        uploaded_file = st.file_uploader("Upload CSV", type=["csv"])
        if uploaded_file is not None:
            if st.button("Upload CSV"):
                files = {"file": (uploaded_file.name, uploaded_file, "text/csv")}
                response = requests.post(f"{API_BASE_URL}/bulk/", files=files)

                if response.status_code == 200:
                    st.success("CSV uploaded successfully!")
                else:
                    st.error(f"Error: {response.text}")



    with tab2:
        st.header("Analyse Purchases")


        st.subheader("Filter by Date and Country")
        start_date = st.date_input("Start Date")
        country_filter = st.text_input("Country (optional)")


        params = {}

        if st.button("Fetch Filtered Data"):

         if start_date:
                params["start_date"] = start_date.isoformat()
         if country_filter:
            params["country"] = country_filter

    
            if params:
             response = requests.get(f"{API_BASE_URL}/purchases/", params=params)
             if response.status_code == 200:
                filtered_data = response.json()
                if filtered_data:
                    df = pd.DataFrame(filtered_data)
                    st.write("Filtered Purchases:")
                    st.dataframe(df)

         
                    total_purchases = len(filtered_data)
                    total_amount = sum([item['amount'] for item in filtered_data])
                    average_amount = total_amount / total_purchases if total_purchases else 0

                    st.subheader("KPIs")
                    st.write(f"Total Purchases: {total_purchases}")
                    st.write(f"Total Amount: {total_amount:.2f}")
                    st.write(f"Average Purchase Amount: {average_amount:.2f}")
                else:
                    st.info("No data found for the selected filters.")
            else:
                st.error(f"Error: {response.text}")
         else:
                st.error("Please provide valid filter values before submitting.")


       
if __name__ == "__main__":
    main()


