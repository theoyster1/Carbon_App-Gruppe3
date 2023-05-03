from flask import render_template, Blueprint, request, redirect, url_for, flash
from capp.models import Transport
from capp import db
from datetime import timedelta, datetime
from flask_login import login_required, current_user
from capp.carbon_app.forms import GenForm
from statistics import mean
import json
import requests


carbon_app=Blueprint('carbon_app',__name__)

#Emissions factor per transport in kg per passemger km
efco2={'Bus':{'Diesel':0.0244130363170317,'CNG':0.019608750602746,'Petrol':0.10231,'Electric':0.00837053571428571},
    'Car':{'Petrol':0.131045333333333,'Diesel':0.132428717948718,'Electric':0},
    'Plane':{'Jet fuel':0.0969207895857439},
    'Ferry':{'Diesel':2.22612334653623},
    'Motorbike':{'Gasoline':0.0853866666666667},
    'Scooter':{'No Fossil Fuel':0},
    'Bicycle':{'No Fossil Fuel':0},
    'Walking':{'No Fossil Fuel':0},
    'Train':{'Diesel':0.039955611, 'Electric':0.009601554}}
efch4={'Bus':{'Diesel':2e-5,'CNG':2.5e-3,'Petrol':2e-5,'Electric':0},
    'Car':{'Petrol':3.1e-4,'Diesel':3e-6,'Electric':0},
    'Plane':{'Jet fuel':1.1e-4},
    'Ferry':{'Diesel':3e-5, 'CNG':3e-5,'Electric':0},
    'Motorbike':{'Gasoline':2.1e-3,'Electric':0},
    'Bicycle':{'No Fossil Fuel':0},
    'Walking':{'No Fossil Fuel':0},
       'Train':{'Diesel':0.039955611, 'Electric':0.009601554}}
      
    
#Carbon app, main page
@carbon_app.route('/carbon_app', methods=['GET','POST'])
@login_required
def carbon_app_home():
    form = GenForm()
    if form.validate_on_submit():
        kms = form.kms.data
        fuel = form.fuel_type.data
        transport = form.transport.data
        math(kms, fuel, transport)
        return redirect(url_for('carbon_app.your_data'))
    msg = request.args.get('msg')
    return render_template('carbon_app/carbon_app.html', title='Carbon App', form = form, msg = msg)



# Your data
@carbon_app.route("/carbon_app/your_data")
@login_required
def your_data():
    if len(Transport.query.all()) < 1:
        return redirect(url_for('carbon_app.carbon_app_home'))

    # Table
    entries = (
        Transport.query.filter_by(author=current_user)
        .filter(Transport.date > (datetime.now() - timedelta(days=5)))
        .order_by(Transport.date.desc())
        .order_by(Transport.transport.asc())
        .all()
    )

    # Emissions by category
    emissions_by_transport = (
        db.session.query(db.func.sum(Transport.total), Transport.transport)
        .filter(Transport.date > (datetime.now() - timedelta(days=5)))
        .filter_by(author=current_user)
        .group_by(Transport.transport)
        .order_by(Transport.transport.asc())
        .all()
    )
    emission_transport = [0, 0, 0, 0, 0, 0, 0, 0]
    first_tuple_elements = []
    second_tuple_elements = []
    for a_tuple in emissions_by_transport:
        first_tuple_elements.append(a_tuple[0])
        second_tuple_elements.append(a_tuple[1])

    if "Bus" in second_tuple_elements:
        index_bus = second_tuple_elements.index("Bus")
        emission_transport[1] = first_tuple_elements[index_bus]
    else:
        emission_transport[1]

    if "Car" in second_tuple_elements:
        index_car = second_tuple_elements.index("Car")
        emission_transport[2] = first_tuple_elements[index_car]
    else:
        emission_transport[2]

    if "Ferry" in second_tuple_elements:
        index_ferry = second_tuple_elements.index("Ferry")
        emission_transport[3] = first_tuple_elements[index_ferry]
    else:
        emission_transport[3]

    if "Motorbike" in second_tuple_elements:
        index_motorbike = second_tuple_elements.index("Motorbike")
        emission_transport[4] = first_tuple_elements[index_motorbike]
    else:
        emission_transport[4]

    if "Plane" in second_tuple_elements:
        index_plane = second_tuple_elements.index("Plane")
        emission_transport[5] = first_tuple_elements[index_plane]
    else:
        emission_transport[5]
        
    if "Train" in second_tuple_elements:
        index_train = second_tuple_elements.index("Train")
        emission_transport[7] = first_tuple_elements[index_train]
    else:
        emission_transport[7]

    # Kilometers by category
    kms_by_transport = (
        db.session.query(db.func.sum(Transport.kms), Transport.transport)
        .filter(Transport.date > (datetime.now() - timedelta(days=5)))
        .filter_by(author=current_user)
        .group_by(Transport.transport)
        .order_by(Transport.transport.asc())
        .all()
    )

    kms_transport = [0, 0, 0, 0, 0, 0, 0, 0]
    first_tuple_elements = []
    second_tuple_elements = []
    for a_tuple in kms_by_transport:
        first_tuple_elements.append(a_tuple[0])
        second_tuple_elements.append(a_tuple[1])
    if "Bicycle" in second_tuple_elements:
        index_bicycle = second_tuple_elements.index("Bicycle")
        kms_transport[0] = first_tuple_elements[index_bicycle]
    else:
        kms_transport[0]

    if "Bus" in second_tuple_elements:
        index_bus = second_tuple_elements.index("Bus")
        kms_transport[1] = first_tuple_elements[index_bus]
    else:
        kms_transport[1]

    if "Car" in second_tuple_elements:
        index_car = second_tuple_elements.index("Car")
        kms_transport[2] = first_tuple_elements[index_car]
    else:
        kms_transport[2]

    if "Ferry" in second_tuple_elements:
        index_ferry = second_tuple_elements.index("Ferry")
        kms_transport[3] = first_tuple_elements[index_ferry]
    else:
        kms_transport[3]

    if "Motorbike" in second_tuple_elements:
        index_motorbike = second_tuple_elements.index("Motorbike")
        kms_transport[4] = first_tuple_elements[index_motorbike]
    else:
        kms_transport[4]

    if "Plane" in second_tuple_elements:
        index_plane = second_tuple_elements.index("Plane")
        kms_transport[5] = first_tuple_elements[index_plane]
    else:
        kms_transport[5]

    if "Walking" in second_tuple_elements:
        index_walk = second_tuple_elements.index("Walk")
        kms_transport[6] = first_tuple_elements[index_walk]
    else:
        kms_transport[6]
        
    if "Train" in second_tuple_elements:
        index_train = second_tuple_elements.index("Train")
        kms_transport[7] = first_tuple_elements[index_train]
    else:
        kms_transport[7]  
    
    # Emissions by date (individual)
    emissions_by_date = (
        db.session.query(db.func.sum(Transport.total), Transport.date)
        .filter(Transport.date > (datetime.now() - timedelta(days=5)))
        .filter_by(author=current_user)
        .group_by(Transport.date)
        .order_by(Transport.date.asc())
        .all()
    )
    over_time_emissions = []
    dates_label = []
    for total, date in emissions_by_date:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_emissions.append(total)

    # Kms by date (individual)
    kms_by_date = (
        db.session.query(db.func.sum(Transport.kms), Transport.date)
        .filter(Transport.date > (datetime.now() - timedelta(days=5)))
        .filter_by(author=current_user)
        .group_by(Transport.date)
        .order_by(Transport.date.asc())
        .all()
    )
    over_time_kms = []
    dates_label = []
    for total, date in kms_by_date:
        dates_label.append(date.strftime("%m-%d-%y"))
        over_time_kms.append(total)

    # Total emissions regardless of date, transport
    total_emissions = (
        db.session.query(db.func.sum(Transport.total))
        .filter_by(author=current_user)
        .all()
    )
    sum_total_emissions = []
    for total in total_emissions:
        sum_total_emissions.append(total)

    # Carbon offset
    TREE_OFFSET_LOWER = 21.77
    TREE_OFFSET_UPPER = 31.5
    carbon_offset_lower_bound = round(sum_total_emissions[0][0] / TREE_OFFSET_UPPER)
    carbon_offset_upper_bound = round(sum_total_emissions[0][0] / TREE_OFFSET_LOWER)
    CARBON_OFFSET_PRICE_PER_1000LBS = 7.99
    CARBON_OFFSET_PRICE_PER_1000KG = round(CARBON_OFFSET_PRICE_PER_1000LBS / 2.205, 2)
    user_carbon_offset_price = round(
        (CARBON_OFFSET_PRICE_PER_1000KG / 1000) * sum_total_emissions[0][0], 4
    )
    sum_total_emissions_ton = round(sum_total_emissions[0][0] / 1000, 4)

    # World mean temperature
    url = "https://global-temperature.p.rapidapi.com/api/temperature-api"

    headers = {
        "content-type": "application/octet-stream",
        "X-RapidAPI-Key": "3bede588c1mshf7e2c981e749cb5p1a3963jsncbac8fd70f21",
        "X-RapidAPI-Host": "global-temperature.p.rapidapi.com",
    }

    response = requests.get(url, headers=headers)
    data = response.json()

    # Extract the data for each year
    years = []
    temperatures = []
    for d in data["result"]:
        if d["time"] > "1920":
            year = int(float(d["time"]))
            temperature = mean([float(d["station"]), float(d["land"])])
            years.append(year)
            temperatures.append(temperature)

    # Calculate the average temperature
    # average_temperature = mean(temperatures)

    return render_template(
        "carbon_app/your_data.html",
        title="your_data",
        entries=entries,
        emissions_by_transport_python_dic=emissions_by_transport,
        emission_transport_python_list=emission_transport,
        emissions_by_transport=json.dumps(emission_transport),
        kms_by_transport=json.dumps(kms_transport),
        over_time_emissions=json.dumps(over_time_emissions),
        over_time_kms=json.dumps(over_time_kms),
        dates_label=json.dumps(dates_label),
        sum_total_emissions=(sum_total_emissions),
        sum_total_emissions_ton=sum_total_emissions_ton,
        carbon_offset_lower_bound=carbon_offset_lower_bound,
        carbon_offset_upper_bound=carbon_offset_upper_bound,
        user_carbon_offset_price=user_carbon_offset_price,
        CARBON_OFFSET_PRICE_PER_1000KG=CARBON_OFFSET_PRICE_PER_1000KG,
        ###
        average_temperature=json.dumps(temperatures),
        yearLabels=json.dumps(years),
    )




#Delete emission
@carbon_app.route('/carbon_app/delete-emission/<int:entry_id>')
def delete_emission(entry_id):
    entry = Transport.query.get_or_404(int(entry_id))
    db.session.delete(entry)
    db.session.commit()
    flash("Entry deleted", "success")
    if len(Transport.query.all()) > 0:
        return redirect(url_for('carbon_app.your_data'))
    else: 
        return redirect(url_for('carbon_app.carbon_app_home' , msg = 'All Entries Deleted'))

#Delete all 
@carbon_app.route('/carbon_app/delete-all-emission')
def delete_all_emission():
    db.session.query(Transport).delete()
    db.session.commit()
    flash("Entry deleted", "success")
    return redirect(url_for('carbon_app.carbon_app_home', msg = 'All Entries Deleted'))



def math(kms, fuel, transport):
    co2 = float(kms) * efco2[transport][fuel]
    ch4 = float(kms) * efch4[transport][fuel]
    total = co2+ch4

    co2 = float("{:.2f}".format(co2))
    ch4 = float("{:.2f}".format(ch4))
    total = float("{:.2f}".format(total))

    emissions = Transport(kms=kms, transport=transport, fuel=fuel, co2=co2, ch4=ch4, total=total, author=current_user)
    db.session.add(emissions)
    db.session.commit()


