import streamlit as st
import pandas as pd
import pymysql

# Database configuration
db_config = {
    'user': "root",
    'host': "localhost",
    'password': "Nrnaidu@1",
    'database': "redbus"
}

def get_db_connection():
    return pymysql.connect(**db_config)

def home():
    st.title("Welcome to Red Bus.com, India's No. 1 Online Bus Ticket Booking Site")
    st.image('C:/Users/Narasimmaraj/Downloads/redbus.jpg', width=200)
    st.write("Find the best buses for your journey.")
    file_url = "https://www.redbus.in"
    href = f'<a href="{file_url}" download>Download The Red Bus App</a>'
    st.markdown(href, unsafe_allow_html=True)

def search():
    st.title("Search Buses")

    # Create a database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # Display actual column names for debugging
    cursor.execute("DESCRIBE redbus.bus_routes")
    columns = cursor.fetchall()
    column_names = [col[0] for col in columns]
    # st.write("Columns available in the dataset:", column_names)

    # Fetch unique values for 'routename' from the database
    if 'routename' in column_names:
        cursor.execute("SELECT DISTINCT `routename` FROM redbus.bus_routes")
        routenames = [row[0] for row in cursor.fetchall()]

        # Create select box for 'routename'
        selected_routename = st.selectbox("Select Route Name", routenames)

        # Add date selection and other filters
        departing_time = st.text_input("Select Departing Time")
        reaching_time = st.text_input("Select Reaching Time")
        
        star_price = st.text_input("Select Price")
        star_rating = st.text_input("Star Rating")
        # st.slider("Price",min_value=0,max_value=5000)
        
        # Query to filter buses based on provided criteria
        query = """
            SELECT * 
            FROM redbus.bus_routes 
            WHERE `routename` = %s
            AND `Departing Time` = %s
            AND `Star Rating` = %s
            AND `Price` = %s
        """
        # Execute query with all required parameters
        cursor.execute(query, (selected_routename, departing_time, star_rating, star_price))
        filtered_result = cursor.fetchall()

        # Create DataFrame
        column_names = [desc[0] for desc in cursor.description]
        df = pd.DataFrame(filtered_result, columns=column_names)

        # Display DataFrame
        st.write(f"Available Buses for route '{selected_routename}' on {departing_time}:")
        st.dataframe(df)
    else:
        st.error("Required column 'routename' is missing from the database schema.")

    # Close the database connection
    cursor.close()
    conn.close()

def booking():
    st.title("Book Your Bus Ticket")

    # Sample input fields
    name = st.text_input("Enter Your Name")
    email = st.text_input("Enter Your Email")
    seat_number = st.number_input("Enter Seat Number", min_value=1)

    if st.button("Confirm Booking"):
        # Create a database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Example SQL query to insert booking data into a table
        query = """
            INSERT INTO redbus.bookings (name, email, seat_number)
            VALUES (%s, %s, %s)
        """
        cursor.execute(query, (name, email, seat_number))
        conn.commit()  # Commit the transaction

        st.write(f"Booking confirmed for {name} with seat number {seat_number}.")

        # Close the database connection
        cursor.close()
        conn.close()

def main():
    st.sidebar.title("Welcome to Red Bus.com, India's No. 1 Online Bus Ticket Booking Site")
    selection = st.sidebar.radio("Go to", ["Home", "Search Buses", "Book Ticket"])
    
    if selection == "Home":
        home()
    elif selection == "Search Buses":
        search()
    elif selection == "Book Ticket":
        booking()

if __name__ == "__main__":
    main()