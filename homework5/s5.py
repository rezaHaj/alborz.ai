patients = [
    {
        'name': 'Alice',
        'age': 36,
        'weight': 60,
        'dosages': [
            {'time': '08:00', 'dose': 10},
            {'time': '12:00', 'dose': 40}
        ]
    },
    {
        'name': 'Bob',
        'age': 16,
        'weight': 40,
        'dosages': [
            {'time': '08:00', 'dose': 5},
            {'time': '12:00', 'dose': -5}
        ]
    }
]

for patient in patients:
    name = patient['name']
    age = patient['age']
    weight = patient['weight']
    
    if age >= 18:
        min_dose = weight * 0.1
        max_dose = weight * 0.5
    else:
        min_dose = weight * 0.05
        max_dose = weight * 0.3
        
    print(f"{name} (Age: {age}, Weight: {weight} kg, Safe Range: {min_dose:.1f}-{max_dose:.1f} mg)")
    
    valid_doses = 0
    for dosage in patient['dosages']:
        dose_val = dosage['dose']
        time = dosage['time']
        
        if dose_val < 0:
            print(f"Invalid dose at {time}: Dose must be positive")
        else:
            valid_doses += 1
            if min_dose <= dose_val <= max_dose:
                status = "Safe"
            else:
                status = "Unsafe"
            print(f"{time}: Dose={dose_val} mg & {status}")
            
    print(f"Total valid doses: {valid_doses}")
