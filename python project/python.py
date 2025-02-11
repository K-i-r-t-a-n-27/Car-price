# Note: If you see an error like "streamlit: The term 'streamlit' is not recognized..."
# please ensure that Streamlit is installed and use the command:
# python -m streamlit run app.py

import joblib
import pandas as pd
import streamlit as st

# Load Model
model_lr = joblib.load('lr.sav')

st.title('Car Price Prediction 🚗💵')
st.markdown(
    """
    <div style="background-color:#000000; padding:10px; border-radius:5px">
        <h4 style="color:#faf7f7;">This app predicts the price of a car based on its features, such as model, age, mileage, and other specifications 🚀. Enter the details and get an estimated price instantly!</h4>
    </div>
    """,
    unsafe_allow_html=True
)
st.image("design.jpg", use_container_width=True)

list_Cars = ['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
             'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
             'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
             'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
             'Ambassador', 'Ashok', 'Isuzu', 'Opel']

fuel_types = ['Diesel', 'Petrol', 'LPG', 'CNG']

owner_types = ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car']

seller_types = ['Individual', 'Dealer', 'Trustmark Dealer']

transmission_types = ['Manual', 'Automatic']

seats_types = [2, 4, 5, 6, 7, 8, 9, 10, 14]

with st.container():
    st.header('Enter Car Details')
    col1, col2 = st.columns(2)
    with col1:
        st.write("### Brand of Car")
        name = st.selectbox("You selected:", list_Cars)

        st.write("### Type of Owner")
        owner = st.selectbox("You selected:", owner_types)

        st.write("### Type of Transmission")
        transmission = st.selectbox("You selected:", transmission_types)

        st.write("### Type of Fuel ⛽")
        fuel = st.selectbox("You selected:", fuel_types)

        st.write("### Type of Sellers")
        seller_type = st.selectbox("You selected:", seller_types)
    with col2:
        st.write("### KM Driven of Car")
        km_driven = st.text_input(label="Enter KM Driven:")

        st.write("### Mileage of Car")
        mileage = st.slider("Select Mileage:", 0, 40, 20)

        st.write("### Age of Car")
        age = st.slider("Select Age:", 0, 40, 3)

        st.write("### Engine of Car (CC)")
        engine = st.slider("Select Engine CC:", 0, 4000, 1200)

        st.write("### Max Power of Car (hp)")
        max_power = st.slider("Select Max Power (hp):", 0, 1000, 120)

    st.write("### Number of Seats 💺")
    seats = st.selectbox("You selected:", seats_types)

# Encoding dictionaries
name_to_encode = ['Maruti', 'Skoda', 'Honda', 'Hyundai', 'Toyota', 'Ford', 'Renault',
                  'Mahindra', 'Tata', 'Chevrolet', 'Datsun', 'Jeep', 'Mercedes-Benz',
                  'Mitsubishi', 'Audi', 'Volkswagen', 'BMW', 'Nissan', 'Lexus',
                  'Jaguar', 'Land', 'MG', 'Volvo', 'Daewoo', 'Kia', 'Fiat', 'Force',
                  'Ambassador', 'Ashok', 'Isuzu', 'Opel']
encoded_name = [20, 26, 10, 11, 28, 9, 25, 19, 27, 4, 6, 14, 21, 22, 2, 29, 3, 23, 17, 13, 16, 18, 30, 5, 15, 7, 8, 0, 1, 12, 24]
convert_name = dict(zip(name_to_encode, encoded_name))

fuel_to_encode = ['Diesel', 'Petrol', 'LPG', 'CNG']
encoded_fuel = [1, 3, 2, 0]
convert_fuel = dict(zip(fuel_to_encode, encoded_fuel))

seller_to_encode = ['Individual', 'Dealer', 'Trustmark Dealer']
encoded_seller = [1, 0, 2]
convert_seller = dict(zip(seller_to_encode, encoded_seller))

transmission_to_encode = ['Manual', 'Automatic']
encoded_transmission = [1, 0]
convert_transmission = dict(zip(transmission_to_encode, encoded_transmission))

owner_to_encode = ['First Owner', 'Second Owner', 'Third Owner', 'Fourth & Above Owner', 'Test Drive Car']
encoded_owner = [0, 2, 4, 1, 3]
convert_owner = dict(zip(owner_to_encode, encoded_owner))

# Build the input DataFrame
try:
    df = pd.DataFrame({
        'name': [convert_name[name]],
        'age': [age],
        'km_driven': [float(km_driven)],
        'fuel': [convert_fuel[fuel]],
        'seller_type': [convert_seller[seller_type]],
        'transmission': [convert_transmission[transmission]],
        'owner': [convert_owner[owner]],
        'mileage': [mileage],
        'engine': [engine],
        'max_power': [max_power],
        'seats': [seats]
    })
except ValueError:
    st.error("Please ensure all numerical fields are correctly filled! ❌")
    df = None

# Sidebar for Prediction
if df is not None:
    with st.sidebar:
        st.write("# Prediction Price of Car")
        st.info("The prediction is based on 97% accuracy ✔️")
        if st.button("Predict Price"):
            st.markdown("---")
            price = model_lr.predict(df)
            price = price[0]
            formatted_price = f"{price:,.2f}" 
            st.write(f"## The Predicted Price is {formatted_price}")
