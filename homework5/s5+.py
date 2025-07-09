print("hi dear user this code is prepared for the situation we donot want to use hard_coding: ")

def main():
    patients = []

    num_patients = int(input("enter number of patients: "))
    
    for i in range(num_patients):
        print(f"\n patients information {i+1} ")
        name = input("patient's name: ")
        age = int(input("patient's age: "))
        weight = float(input("patients weight: "))
        
        dosages = []
        num_dosages = int(input("enter number of specified dosage: "))
        
        for j in range(num_dosages):
            print(f" number of dosage {j+1}:")
            time = input("(for example: 08:00): ")
            dose = float(input("Dosage (mg): "))
            dosages.append({'time': time, 'dose': dose})
        
        patients.append({
            'name': name,
            'age': age,
            'weight': weight,
            'dosages': dosages
        })
    
    print("\n sumery off the results: ")
    for patient in patients:
        name = patient['name']
        age = patient['age']
        weight = patient['weight']
        
        if age >= 18:
            min_dose = weight * 0.1
            max_dose = weight * 0.5
            #min_dose=int(min_dose)
        else:
            min_dose = weight * 0.05
            max_dose = weight * 0.3
        
        print(f"\n{name} (age: {age} years old , weight: {weight} kg , safe rate: {int(min_dose)} & {int(max_dose)} mg)")
        
        valid_doses = 0
        for dosage in patient['dosages']:
            dose_val = dosage['dose']
            time = dosage['time']
            
            if dose_val < 0:
                print(f"  {time}: dose={dose_val} it canno be nagative value")
            else:
                valid_doses += 1
                if min_dose <= dose_val <= max_dose:
                    status = "safe"
                else:
                    status = "unsafe"
                print(f"  {time}: does={dose_val} mg & {status}")
        
        print(f" {valid_doses}")

main()