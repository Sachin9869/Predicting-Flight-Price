import pickle
import pandas as pd
from flask import Flask, request, render_template



app = Flask(__name__)
random_forest_model = pickle.load(open("random_forest_model.pkl", "rb"))



@app.route("/")
def home():
    return render_template("index.html")




@app.route("/predict", methods = ["GET", "POST"])
def predict():
    if request.method == "POST":

        # Selected journey date
        date_departure = request.form["Dep_Time"]
        Journey_day = int(pd.to_datetime(date_departure, format="%Y-%m-%dT%H:%M").day)
        Journey_month = int(pd.to_datetime(date_departure, format ="%Y-%m-%dT%H:%M").month)
        # print("Journey Date : ",Journey_day, Journey_month)

        # Departure datetime
        Departure_hour = int(pd.to_datetime(date_departure, format ="%Y-%m-%dT%H:%M").hour)
        Departure_min = int(pd.to_datetime(date_departure, format ="%Y-%m-%dT%H:%M").minute)
        # print("Departure : ",Dep_hour, Dep_min)

        # Arrival datetime
        date_arrival = request.form["Arrival_Time"]
        Arrival_hour = int(pd.to_datetime(date_arrival, format ="%Y-%m-%dT%H:%M").hour)
        Arrival_min = int(pd.to_datetime(date_arrival, format ="%Y-%m-%dT%H:%M").minute)
        # print("Arrival : ", Arrival_hour, Arrival_min)

        # Duration in hour and minute
        duration_hour = abs(Arrival_hour - Departure_hour)
        duration_min = abs(Arrival_min - Departure_min)
        # print("Duration : ", dur_hour, dur_min)

        # number of stops in between
        no_stops = int(request.form["stops"])
        # print(Total_stops)

        # Airline        
        airline=request.form['airline']
        
        Jet_Airways = 0
        IndiGo = 0
        Air_India = 0
        Multiple_carriers = 0
        SpiceJet = 0
        Vistara = 0
        GoAir = 0
        Multiple_carriers_Premium_economy = 0
        Jet_Airways_Business = 0
        Vistara_Premium_economy = 0
        Trujet = 0 
        
        if(airline=='Jet Airways'):
            Jet_Airways = 1           

        elif (airline=='IndiGo'):
            IndiGo = 1

        elif (airline=='Air India'):
            Air_India = 1
            
        elif (airline=='Multiple carriers'):
            Multiple_carriers = 1
            
        elif (airline=='SpiceJet'):
            SpiceJet = 1
            
        elif (airline=='Vistara'):
            Vistara = 1

        elif (airline=='GoAir'):
            GoAir = 1

        elif (airline=='Multiple carriers Premium economy'):
            Multiple_carriers_Premium_economy = 1

        elif (airline=='Jet Airways Business'):
            Jet_Airways_Business = 1

        elif (airline=='Vistara Premium economy'):
            Vistara_Premium_economy = 1
            
        elif (airline=='Trujet'):
            Trujet = 1

        
        #Source
        source_Delhi = 0
        source_Kolkata = 0
        source_Mumbai = 0
        source_Chennai = 0
         
        Source = request.form["Source"]
        if (Source == 'Delhi'):
            source_Delhi = 1

        elif (Source == 'Kolkata'):
            source_Kolkata = 1

        elif (Source == 'Mumbai'):
            source_Mumbai = 1

        elif (Source == 'Chennai'):
            source_Chennai = 1

        
        Dest = request.form["Destination"]        
        dest_Cochin = 0
        dest_Delhi = 0
        dest_New_Delhi = 0
        dest_Hyderabad = 0
        dest_Kolkata = 0
            
        if (Dest == 'Cochin'):
            dest_Cochin = 1
        
        elif (Dest == 'Delhi'):
            dest_Delhi = 1

        elif (Dest == 'New_Delhi'):
            dest_New_Delhi = 1

        elif (Dest == 'Hyderabad'):
            dest_Hyderabad = 1

        elif (Dest == 'Kolkata'):
            dest_Kolkata = 1
        
        cost_pred=random_forest_model.predict([[
            no_stops,
            Journey_day,
            Journey_month,
            Departure_hour,
            Departure_min,
            Arrival_hour,
            Arrival_min,
            duration_hour,
            duration_min,
            Air_India,
            GoAir,
            IndiGo,
            Jet_Airways,
            Jet_Airways_Business,
            Multiple_carriers,
            Multiple_carriers_Premium_economy,
            SpiceJet,
            Trujet,
            Vistara,
            Vistara_Premium_economy,
            source_Chennai,
            source_Delhi,
            source_Kolkata,
            source_Mumbai,
            dest_Cochin,
            dest_Delhi,
            dest_Hyderabad,
            dest_Kolkata,
            dest_New_Delhi
        ]])

        result=round(cost_pred[0],3)

        return render_template('index.html',prediction_text="The predicted cost (INR) is Rs. {}".format(result))


    return render_template("index.html")




if __name__ == "__main__":
    app.run(debug=True)
