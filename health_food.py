import pandas as pd
import streamlit as st

# Load dataset
df = pd.read_csv('healthy_foods_dataset_final2.csv')

def recommend_foods_halfkg_always_3sets(budget, categories, top_n=3):
    filtered = df[df['Category'].isin(categories)].copy()
    price_column = 'Price_HalfKG (₹/kg)'
    filtered['nutrient_score'] = (filtered['Protein (g)'] + filtered['Fiber (g)']) / filtered[price_column]
    filtered = filtered.sort_values(by='nutrient_score', ascending=False)

    recommendations = []
    remaining = filtered.copy()

    for _ in range(top_n):
        selected_rows = []
        total_cost = 0
        total_protein = 0
        total_fiber = 0

        for idx, row in remaining.iterrows():
            cost = row[price_column]
            if total_cost + cost <= budget:
                selected_rows.append(row)
                total_cost += cost
                total_protein += row['Protein (g)'] / 2  # half kg nutrition
                total_fiber += row['Fiber (g)'] / 2

        recommended_df = pd.DataFrame(selected_rows)
        recommendations.append({
            'dataframe': recommended_df,
            'total_cost': total_cost,
            'total_protein': total_protein,
            'total_fiber': total_fiber
        })

        selected_items = recommended_df['Food Item'].tolist()
        remaining = remaining[~remaining['Food Item'].isin(selected_items)]

        # If no items left, reset remaining to full filtered to allow repeats
        if remaining.empty:
            remaining = filtered.copy()

    return recommendations

# Streamlit UI

st.title('Healthy Food Recommendation Based on Budget')

st.markdown("""
Hey guys! This app helps you find healthy food sets within your budget using half-kilogram pricing.
Select your preferred food categories and budget to see optimized nutritious sets.
""")

budget = st.number_input('Enter your budget (₹)', min_value=1, value=500)
categories = st.multiselect('Select Food Categories', options=df['Category'].unique())

if st.button('Get Recommendations'):
    if not categories:
        st.warning('Please select at least one food category.')
    else:
        recs = recommend_foods_halfkg_always_3sets(budget, categories)
        for i, rec in enumerate(recs, 1):
            st.subheader(f'Set {i} (Approx 0.5 kg per item)')
            if not rec['dataframe'].empty:
                col1, col2, col3 = st.columns(3)
                col1.metric("Total Cost (₹)", f"{rec['total_cost']:.2f}")
                col2.metric("Total Protein (g)", f"{rec['total_protein']:.2f}")
                col3.metric("Total Fiber (g)", f"{rec['total_fiber']:.2f}")

                st.dataframe(rec['dataframe'][['Food Item', 'Category', 'Price_HalfKG (₹/kg)', 'Protein (g)', 'Fiber (g)', 'Calories']].style.format({
                    'Price_HalfKG (₹/kg)': '₹{:.2f}',
                    'Protein (g)': '{:.2f}',
                    'Fiber (g)': '{:.2f}',
                    'Calories': '{:.0f}'
                }))
            else:
                st.info('No foods found within budget.')
