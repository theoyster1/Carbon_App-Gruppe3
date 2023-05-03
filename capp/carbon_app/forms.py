from flask_wtf import FlaskForm
from wtforms import  SubmitField,  SelectField,  FloatField
from wtforms.validators import InputRequired



class GenForm(FlaskForm):
    transport = SelectField('Mean of conveyance', [InputRequired()],
                            choices=[('Bus', 'Bus'), ('Car', 'Car'), ('Plane', 'Plane'), ('Boat', 'Boat'), 
                                     ('Motorbike', 'Motorbike'),
                                      ('Bicycle', 'Bicycle'), ('Walking', 'Walking'), ('Train', 'Train')])
    kms = FloatField('Kilometers', [InputRequired()])
    fuel_type = SelectField('Type of Fuel', [InputRequired()], 
                                choices=[('Petrol', 'Petrol'), ('Diesel', 'Diesel'), ('No Fossil Fuel', 'No Fossil Fuel'), 
                                         ('Gasoline','Gasoline'), ('Electric', 'Electric'), ('Jet fuel', 'Jet fuel'),
                                         ('CNG', 'CNG')])
    submit = SubmitField('Calculate')
