#DEFINING CONSTANTS
gearingratio= 11.82
wheel_mass_kg= 0.104
rolling_radius_m = 0.042
drivetrain_efficiency = 0.95
kv_rating = 3500
voltage = 7.2
max_current = 65.0
rollingresistance = 0.05
mass_kg = 3
g=9.81
motor_mass = 0.260


max_rpm = voltage*kv_rating
max_power = voltage*max_current
enginetorque = (9550*(max_power/1000))/max_rpm
overalltorque = (enginetorque*gearingratio)

force = overalltorque/rolling_radius_m
f_drivetrain_drag = force*(1-drivetrain_efficiency)
f_rollingresistance = (rollingresistance*mass_kg*g)
force = force - f_drivetrain_drag 
force = force - f_rollingresistance

momentofinertia_wheel = 0.5*(wheel_mass_kg**2)
masseqwheels = (momentofinertia_wheel*4)/(rolling_radius_m**2)
masseqmotors = (0.5*(motor_mass**2)*(gearingratio**2)/0.001)/(0.009**2)
masseq = masseqwheels+masseqwheels
equivalent_mass = mass_kg + mass_kg*(masseq)

print(equivalent_mass)

print(force)