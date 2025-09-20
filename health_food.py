import pandas as pd
import streamlit as st

# Load dataset
df = pd.read_csv('healthy_foods_dataset_final.csv')

def recommend_foods_varied(budget, categories, top_n=3):
    filtered = df[df['Category'].isin(categories)].copy()
    filtered['nutrient_score'] = (filtered['Protein (g)'] + filtered['Fiber (g)']) / filtered['Price (₹/kg)']
    filtered = filtered.sort_values(by='nutrient_score', ascending=False)
    
    recommendations = []
    remaining = filtered.copy()
    
    for _ in range(top_n):
        selected = []
        total_cost = 0
        for idx, row in remaining.iterrows():
            if total_cost + row['Price (₹/kg)'] <= budget:
                selected.append(f"{row['Food Item']} (₹{row['Price (₹/kg)']})")
                total_cost += row['Price (₹/kg)']
        recommendations.append(selected)
        # Remove selected items from remaining for next set
        remaining = remaining[~remaining['Food Item'].isin([x.split(' (')[0] for x in selected])]
        if len(remaining) == 0:
            break
    return recommendations

# Streamlit UI
st.title('Healthy Food Recommendation Based on Budget')

budget = st.number_input('Enter your budget (₹)', min_value=1)
categories = st.multiselect('Select Food Categories', options=df['Category'].unique())

if st.button('Get Recommendations'):
    if not categories:
        st.warning('Please select at least one food category.')
    else:
        recs = recommend_foods_varied(budget, categories)
        for i, rec in enumerate(recs, 1):
            st.subheader(f'Set {i}')
            if rec:
                for item in rec:
                    st.write(item)
            else:
                st.write('No foods found within budget.')
