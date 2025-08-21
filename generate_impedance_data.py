import pandas as pd
import numpy as np

# Define parameters
frequencies = [1.0, 2.0, 6.78] # MHz
facial_areas = ['Forehead', 'Cheek_Left', 'Cheek_Right', 'Jawline_Left', 'Jawline_Right']

# Volunteer distribution
volunteer_specs = {
    'Female': {'40s': 2, '30s': 2, '20s': 1},
    'Male': {'50s': 2, '30s': 2, '20s': 1}
}

data = []
volunteer_id_counter = 1

# Base impedance ranges (Ohms)
base_real_impedance_range = (100, 400)
base_imaginary_impedance_range = (-150, 50) # Typically capacitive for skin

# Generate data for each volunteer
for gender, age_groups in volunteer_specs.items():
    for age_group, count in age_groups.items():
        for _ in range(count):
            volunteer_id = f"V{volunteer_id_counter:02d}"
            volunteer_id_counter += 1

            # Introduce slight variations based on age/gender for realism
            real_impedance_offset = 0
            imaginary_impedance_offset = 0
            if gender == 'Female':
                real_impedance_offset += 10
                imaginary_impedance_offset -= 5
            else: # Male
                real_impedance_offset -= 10
                imaginary_impedance_offset += 5

            if age_group == '20s':
                real_impedance_offset -= 20
                imaginary_impedance_offset += 10
            elif age_group == '30s':
                real_impedance_offset -= 10
                imaginary_impedance_offset += 5
            elif age_group == '40s':
                real_impedance_offset += 0
                imaginary_impedance_offset += 0
            elif age_group == '50s':
                real_impedance_offset += 20
                imaginary_impedance_offset -= 10

            for freq in frequencies:
                for area in facial_areas:
                    # Further variations based on facial area
                    area_real_offset = 0
                    area_imaginary_offset = 0
                    if 'Cheek' in area:
                        area_real_offset += 15
                        area_imaginary_offset -= 10
                    elif 'Jawline' in area:
                        area_real_offset -= 10
                        area_imaginary_offset += 5
                    elif 'Forehead' in area:
                        area_real_offset += 5
                        area_imaginary_offset -= 5

                    # Generate impedance values with noise
                    real_impedance = np.random.uniform(
                        base_real_impedance_range[0] + real_impedance_offset + area_real_offset,
                        base_real_impedance_range[1] + real_impedance_offset + area_real_offset
                    )
                    imaginary_impedance = np.random.uniform(
                        base_imaginary_impedance_range[0] + imaginary_impedance_offset + area_imaginary_offset,
                        base_imaginary_impedance_range[1] + imaginary_impedance_offset + area_imaginary_offset
                    )

                    # Ensure impedance values are within reasonable bounds after offsets
                    real_impedance = max(50, min(500, real_impedance))
                    imaginary_impedance = max(-200, min(100, imaginary_impedance))

                    # Calculate output efficiency (simplified model for demonstration)
                    # Assume optimal real impedance around 250 Ohms, imaginary around -50 Ohms
                    # Efficiency decreases as impedance deviates from optimal
                    optimal_real = 250
                    optimal_imaginary = -50
                    
                    # Distance from optimal point in a 2D impedance space
                    impedance_distance = np.sqrt(
                        ((real_impedance - optimal_real) / 100)**2 + # Normalize by a typical range
                        ((imaginary_impedance - optimal_imaginary) / 100)**2
                    )

                    # Simple inverse relationship with some scaling and noise
                    # Max efficiency around 95%, min around 50%
                    efficiency = 95 - (impedance_distance * 10) + np.random.normal(0, 3) # Add some noise
                    efficiency = max(50, min(95, efficiency)) # Clamp efficiency between 50% and 95%

                    data.append([
                        volunteer_id, gender, age_group, freq, area,
                        real_impedance, imaginary_impedance, efficiency
                    ])

# Create DataFrame
df = pd.DataFrame(data, columns=[
    'Volunteer_ID', 'Gender', 'Age_Group', 'Frequency_MHz', 'Facial_Area',
    'Real_Impedance_Ohms', 'Imaginary_Impedance_Ohms', 'Output_Efficiency_Percentage'
])

# Save to CSV
output_csv_path = 'C:/projects/impedance/rf_impedance_data.csv'
df.to_csv(output_csv_path, index=False)

print(f"Dummy data generated and saved to {output_csv_path}")
print(df.head())
print(df.describe())
