import pandas as pd
import streamlit as st

# Load dataset
df = pd.read_csv('healthy_foods_dataset_final.csv')

def recommend_foods(budget, categories, top_n=3):
    filtered = df[df['Category'].isin(categories)].copy()
    filtered['nutrient_score'] = (filtered['Protein (g)'] + filtered['Fiber (g)']) / filtered['Price (₹/kg)']
    filtered = filtered.sort_values(by='nutrient_score', ascending=False)
    
    recommendations = []
    for _ in range(top_n):
        selected = []
        total_cost = 0
        for _, row in filtered.iterrows():
            if total_cost + row['Price (₹/kg)'] <= budget:
                selected.append(f"{row['Food Item']} (₹{row['Price (₹/kg)']})")
                total_cost += row['Price (₹/kg)']
        recommendations.append(selected)
    
    return recommendations

# Streamlit UI
st.title('Healthy Food Recommendation Based on Budget')

budget = st.number_input('Enter your budget (₹)', min_value=1)
categories = st.multiselect('Select Food Categories', options=df['Category'].unique())

if st.button('Get Recommendations'):
    if not categories:
        st.warning('Please select at least one food category.')
    else:
        recs = recommend_foods(budget, categories)
        for i, rec in enumerate(recs, 1):
            st.subheader(f'Set {i}')
            if rec:
                for item in rec:
                    st.write(item)
            else:
                st.write('No foods found within budget.')
